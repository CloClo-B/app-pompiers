import {FontAwesome} from "@expo/vector-icons";
import * as Location from "expo-location";
import React, {useEffect, useRef, useState, useMemo, useCallback} from "react";
import {ActivityIndicator, StyleSheet, TouchableOpacity, View, Linking, Platform, Modal, Text, Alert} from "react-native";
import { Marker } from "react-native-maps";
import MapView from "react-native-map-clustering"; 
import { useRouter } from 'expo-router';
import HautPage from "@/app/hautPage";
import { getAllPointEauLight, getPointEauByID } from "@/service/pointEauService";
import { getToken } from "@/service/infosStocker";
import ButtonLog from '@/components/ButtonLog';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Définit toutes les infos qu'un point possède
type PointEau = {
  id: number;
  numero_pei: string;
  nom: string | null;
  statut: string;
  type_nature: string;
  press_deb: number | null;
  debit_1_bar: number | null;
  vol_eau_mil: number | null;
  latitude: number;
  longitude: number;
};

// Définit les infos minimum qu'un point possède (Optimisation)
type PointEauLight = {
  id: number;
  numero_pei: string;
  latitude: number;
  longitude: number;
};

export default function HomeScreen() {
  const [localisation, setLocalisation] = useState<Location.LocationObject | null>(null);
  const [pointsEau, setPointsEau] = useState<PointEauLight[]>([]);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedPEI, setSelectedPEI] = useState<PointEau | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const router = useRouter();

  const referenceCarte = useRef<any>(null);

  // Fonction pour charger les points d'eau avec cache
  const fetchPointsEau = async () => {
    try {
      const raw = await AsyncStorage.getItem('points_eau_cache');
      if (raw) {
        setPointsEau(JSON.parse(raw));
        setLoading(false);
        return;
      }
      const response = await getAllPointEauLight();
      const pointsRaw = Array.isArray(response) ? response : response.points_eau;
      setPointsEau(pointsRaw);
      await AsyncStorage.setItem('points_eau_cache', JSON.stringify(pointsRaw));
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // Rafraîchir via le logo
  const handleRefresh = async () => {
    setIsRefreshing(true);
    await AsyncStorage.removeItem('points_eau_cache');
    await fetchPointsEau();
    setIsRefreshing(false);
  };

  const getData = async () => {
    const value = await getToken();
    if(value) setToken(value);
  }

  useEffect(() => {
    let watchAbonnement: Location.LocationSubscription | null = null;
    getData();

    const getLocation = async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") return;
      const loc = await Location.getCurrentPositionAsync({});
      setLocalisation(loc);
      setLocation({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });

      watchAbonnement = await Location.watchPositionAsync(
        { accuracy: Location.Accuracy.High, timeInterval: 5000, distanceInterval: 10 },
        (nouvelleLocalisation) => {
          setLocalisation(nouvelleLocalisation);
          setLocation({ latitude: nouvelleLocalisation.coords.latitude, longitude: nouvelleLocalisation.coords.longitude });
        }
      );
    };

    fetchPointsEau();
    getLocation();
    return () => { if (watchAbonnement) watchAbonnement.remove(); };
  }, []);

  const allerPosition = () => {
    if (referenceCarte.current && localisation?.coords) {
      referenceCarte.current.animateToRegion({
        latitude: localisation.coords.latitude,
        longitude: localisation.coords.longitude,
        latitudeDelta: 0.01,
        longitudeDelta: 0.01,
      }, 1000);
    }
  };

  // Récupération des détails complets au clic (useCallback)
  const infoPointEau = useCallback(async (point: PointEauLight) => {
    setSelectedPEI(null);
    setModalVisible(true);
    setLoadingDetails(true);
    try {
      const details = await getPointEauByID(token ?? '', point.numero_pei);
      setSelectedPEI(details);
    } catch (error) {
      Alert.alert("Erreur", "Impossible de charger les détails.");
      setModalVisible(false);
    } finally {
      setLoadingDetails(false);
    }
  }, [token]);

  const markers = useMemo(() => {
    return pointsEau.map((point) => (
      <Marker
        key={point.id}
        coordinate={{ latitude: point.latitude, longitude: point.longitude }}
        title={`Numero PEI : ${point.numero_pei}`}
        onCalloutPress={() => infoPointEau(point)}
      />
    ));
  }, [pointsEau, infoPointEau]);

  if (loading || !location) {
    return <View style={styles.loader}><ActivityIndicator size="large" color="#1976D2" /></View>;
  }

  return (
    <View style={styles.container}>
      <HautPage title="Carte des points d’eau" onLogoPress={handleRefresh} isRefreshing={isRefreshing} />

      <MapView
        ref={referenceCarte}
        style={styles.map}
        initialRegion={{ latitude: location.latitude, longitude: location.longitude, latitudeDelta: 0.2, longitudeDelta: 0.2 }}
        showsUserLocation
        clusterColor="#007AFF"
      >
        {markers}
      </MapView>

      <TouchableOpacity style={styles.boutonLocalisation} onPress={allerPosition}>
        <FontAwesome name="location-arrow" size={24} color="#FFF" />
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={styles.boutonAjout} 
        onPress={() => location && router.push({ pathname: '/creerPropositionAjout', params: { latitude: location.latitude, longitude: location.longitude}})}
      >
        <FontAwesome name="plus" size={24} color="#FFF" />
      </TouchableOpacity>

      <Modal transparent animationType="fade" visible={modalVisible}>
        <View style={styles.overlay}>
          <View style={styles.alertBox}>
            {loadingDetails ? (
              <ActivityIndicator size="large" color="#1976D2" />
            ) : (
              <>
                <Text style={styles.title}>Numero PEI : {selectedPEI?.numero_pei}</Text>
                <Text style={styles.message}>
                  Statut : {selectedPEI?.statut}{"\n"}
                  Type : {selectedPEI?.type_nature ?? "N/A"}{"\n"}
                  Pression : {selectedPEI?.press_deb ?? "N/A"} bar{"\n"}
                  Débit : {selectedPEI?.debit_1_bar ?? "N/A"} m3/h{"\n"}
                  Volume : {selectedPEI?.vol_eau_mil ?? "N/A"}
                </Text>

                <ButtonLog
                  label="Itinéraire"
                  onPress={() => {
                    if (!selectedPEI) return;
                    const url = Platform.OS === "ios"
                      ? `maps://maps.apple.com/?daddr=${selectedPEI.latitude},${selectedPEI.longitude}`
                      : `https://www.google.com/maps/dir/?api=1&destination=${selectedPEI.latitude},${selectedPEI.longitude}`;
                    Linking.openURL(url);
                  }}
                  type="itineraire" width={'100%'} height={45}
                />

                <ButtonLog
                  label="Signaler"
                  onPress={() => {
                    if (selectedPEI) router.push({ pathname: '/creerSignalement', params: {idPoint: selectedPEI.numero_pei.toString()} });
                    setModalVisible(false);
                  }}
                  type="signalement" width={'100%'} height={45}
                />
              </>
            )}
            <TouchableOpacity onPress={() => setModalVisible(false)}>
              <Text style={styles.cancelText}>Fermer</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1 
  },
  map: { 
    flex: 1 
  },
  boutonLocalisation: {
    position: "absolute",
    bottom: 20,
    right: 20,
    backgroundColor: "#007AFF",
    borderRadius: 30,
    width: 60,
    height: 60,
    justifyContent: "center",
    alignItems: "center",
    elevation: 5,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  boutonAjout: {
    position: "absolute",
    bottom: 20,
    left: 20,
    backgroundColor: "#28a745",
    borderRadius: 30,
    width: 60,
    height: 60,
    justifyContent: "center",
    alignItems: "center",
    elevation: 5,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  loader: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5F5F5",
  },
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "center",
    alignItems: "center",
  },
  alertBox: {
    width: "85%",
    backgroundColor: "white",
    borderRadius: 20,
    padding: 20,
    elevation: 10,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.34,
    shadowRadius: 6.27,
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 15,
    textAlign: "center",
    color: "#251f20",
  },
  message: {
    fontSize: 16,
    marginBottom: 20,
    lineHeight: 24,
    color: "#444",
  },
  cancelText: {
    color: "#007AFF",
    textAlign: "center",
    fontWeight: "700",
    marginTop: 15,
    fontSize: 16,
    paddingVertical: 5,
  },
});
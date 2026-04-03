import {FontAwesome} from "@expo/vector-icons";
import * as Location from "expo-location";
import React, {useEffect, useRef, useState, useMemo, useCallback} from "react";
import {ActivityIndicator, StyleSheet, TouchableOpacity, View, Linking, Platform, Modal, Text, Alert} from "react-native";
import { Marker } from "react-native-maps";
import MapView from "react-native-map-clustering";
import { useRouter } from 'expo-router';
import HautPage from "@/app/hautPage";
import { getPointEauByID, getAllPointEauLight } from "@/service/pointEauService";
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

// Page Accueil (Commandement) carte interactive qui localisation / affiche les points d'eau incendie / itinéraire ou signaler un problème sur les points d'eau
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

  // Référence pour piloter la carte
  const referenceCarte = useRef<any>(null);

  // Fonction pour charger les points d'eau
  const fetchPointsEau = async () => {
    try {
      const raw = await AsyncStorage.getItem('points_eau_cache');
      if (raw) {
        setPointsEau(JSON.parse(raw)); // Charge depuis le cache
        setLoading(false);
        return;
      }

      const response = await getAllPointEauLight();
      const pointsRaw = Array.isArray(response) ? response : response.points_eau;
      setPointsEau(pointsRaw);
      await AsyncStorage.setItem('points_eau_cache', JSON.stringify(pointsRaw));

    } catch (error) {
      console.error('Erreur chargement points :', error);
    } finally {
      setLoading(false);
    }
  };

  // Actualiser les points d'eau depuis le logo SDIS
  const handleRefresh = async () => {
    setIsRefreshing(true);
    await AsyncStorage.removeItem('points_eau_cache');
    await fetchPointsEau();
    setIsRefreshing(false);
  };

  // récupérer le token
  const getData = async () => {
    try {
      const value = await getToken();
      if(value !== null) {
        setToken(value);
      }
    } catch(e) {
      console.log("erreur token creation point eau");
    }
  }

  // Charge les points d'eau et active le GPS
  useEffect(() => {
    let watchAbonnement: Location.LocationSubscription | null = null;
    getData();

    // Demande l'accès au GPS et suit la position de l'utilisateur
    const getLocation = async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") return;

      const loc = await Location.getCurrentPositionAsync({});
      setLocalisation(loc);
      setLocation({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });

      // Met à jour la position automatiquement
      watchAbonnement = await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          timeInterval: 5000,
          distanceInterval: 10,
        },
        (nouvelleLocalisation) => {
          setLocalisation(nouvelleLocalisation);
          setLocation({
            latitude: nouvelleLocalisation.coords.latitude,
            longitude: nouvelleLocalisation.coords.longitude,
          });
        }
      );
    };

    const initializeApp = async () => {
      await fetchPointsEau();
      setLoading(false);
    };

    initializeApp();
    getLocation();

    return () => {
      if (watchAbonnement) watchAbonnement.remove();
    };
  }, []);

  // Recentre la carte sur la position de l'utilisateur
  const allerPosition = () => {
    if (referenceCarte.current && localisation?.coords) {
      referenceCarte.current.animateToRegion(
        {
          latitude: localisation.coords.latitude,
          longitude: localisation.coords.longitude,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        },
        1000
      );
    }
  };

  // Description des points d'eaux
  const infoPointEau = useCallback(async (point: PointEauLight) => {
    setSelectedPEI(null);
    setModalVisible(true);
    setLoadingDetails(true);

    try {
      const details = await getPointEauByID(token ?? '', point.numero_pei);
      setSelectedPEI(details);
    } catch (error) {
      console.error('Erreur chargement détails :', error);
      Alert.alert("Erreur", "Impossible de charger les détails de ce point.");
      setModalVisible(false);
    } finally {
      setLoadingDetails(false);
    }
  }, [token]);

  // Mémoire pour éviter le recalcule des markers
  const markers = useMemo(() => {
    return pointsEau.map((point) => (
      <Marker
        key={point.id}
        coordinate={{ latitude: point.latitude, longitude: point.longitude }}
        title={`Numero PEI : ${point.numero_pei}`}
        description="Cliquez ici pour avoir plus d'infos"
        onCalloutPress={() => infoPointEau(point)}
      />
    ));
  }, [pointsEau, infoPointEau]);


  if (loading || !location) {
    return (
      <View style={styles.loader}>
        <ActivityIndicator size="large" color="#1976D2" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <HautPage title="Carte des points d'eau" onLogoPress={handleRefresh} isRefreshing={isRefreshing} />

      {/* Carte */}
      <MapView
        ref={referenceCarte}
        style={styles.map}
        initialRegion={{
          latitude: location.latitude,
          longitude: location.longitude,
          latitudeDelta: 0.2,
          longitudeDelta: 0.2,
        }}
        showsUserLocation // Affiche le point bleu Localisation

        // Réglage des bulles de regroupement
        clusterColor="#007AFF"
        clusterTextColor="#FFFFFF"
        radius={50}
        extent={512}
      >
        {/* Affichage de la mémoire des markers */}
        {markers}
      </MapView>
      

      {/* Bouton retour a la Positions */}
      <TouchableOpacity style={styles.boutonLocalisation} onPress={allerPosition}>
        <FontAwesome name="location-arrow" size={24} color="#FFF" />
      </TouchableOpacity>
      
      {/* bouton de crétation d'une proposition d'ajout de point */}
      <TouchableOpacity 
        style={styles.boutonAjout} 
        onPress={() => {
          if (location) {
            router.push({ pathname: '/creerPropositionAjout', params: { latitude: location.latitude, longitude: location.longitude}});
          }
        }}
      >
        <FontAwesome name="plus" size={24} color="#FFF" />
      </TouchableOpacity>


      {/* Description des points d'eau */}
      <Modal transparent animationType="fade" visible={modalVisible}>
        <View style={styles.overlay}>
          <View style={styles.alertBox}>
            <Text style={styles.title} numberOfLines={2} ellipsizeMode="tail">
              Numero PEI : {selectedPEI?.numero_pei}
            </Text>

            {loadingDetails ? (
              <ActivityIndicator size="small" color="#1976D2" style={{ marginBottom: 20 }} />
            ) : (
              <Text style={styles.message}>
                Statut : {selectedPEI?.statut}{"\n"}
                Type : {selectedPEI?.type_nature ?? "N/A"}{"\n"}
                Pression : {selectedPEI?.press_deb ?? "N/A"} bar{"\n"}
                Débit : {selectedPEI?.debit_1_bar ?? "N/A"} m3/h{"\n"}
                Volume d'eau : {selectedPEI?.vol_eau_mil ?? "N/A"}
              </Text>
            )}

            {/* Itinéraire pour aller au point d'eau */}
            <ButtonLog
              label="Itinéraire"
              onPress={() => {
                if (!selectedPEI) return;
                const url = Platform.OS === "ios"
                  ? `maps://maps.apple.com/?daddr=${selectedPEI.latitude},${selectedPEI.longitude}`
                  : `https://www.google.com/maps/dir/?api=1&destination=${selectedPEI.latitude},${selectedPEI.longitude}`;
                Linking.openURL(url);
              }}
              type="itineraire"
              width={'100%'}
              height={45}
            />

            {/* Créer une mission */}
            <ButtonLog
              label="Créer une mission"
              onPress={() => {
                if (selectedPEI) {
                  router.push({ 
                    pathname: '/creerMissionCarte', 
                    params: {idPoint: selectedPEI.numero_pei.toString()} 
                  });
                };
                setModalVisible(false);
              }}
              type="mission"
              width={'100%'}
              height={45}
            />
  
            {/* Signaler le point d'eau */}
            <ButtonLog
              label="Signaler"
              onPress={() => {
                if (selectedPEI) {
                  router.push({ pathname: '/creerSignalement', params: {idPoint: selectedPEI.numero_pei.toString()} });
                };
                setModalVisible(false);
              }}
              type="signalement"
              width={'100%'}
              height={45}
            />
            
            
            <TouchableOpacity onPress={() => setModalVisible(false)}>
              <Text style={styles.cancelText}>Fermer</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}


// Styles
const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { flex: 1 },

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
  },

  loader: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },

  overlay: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    alignItems: "center",
  },
  alertBox: {
    width: "85%",
    backgroundColor: "white",
    borderRadius: 14,
    padding: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 10,
    textAlign: "center",
  },
  message: {
    fontSize: 15,
    marginBottom: 20,
    lineHeight: 22,
  },
  cancelText: {
    color: "#007AFF",
    textAlign: "center",
    fontWeight: "600",
    marginTop: 10,
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
  },
});
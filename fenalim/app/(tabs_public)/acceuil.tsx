import {FontAwesome} from "@expo/vector-icons";
import * as Location from "expo-location";
import React, {useEffect, useRef, useState} from "react";
import {ActivityIndicator, StyleSheet, TouchableOpacity, View, Linking, Platform, Modal, Text} from "react-native";
import MapView, { Marker } from "react-native-maps";
import { useRouter } from 'expo-router';
import HautPage from "@/app/hautPage";
import proj4 from "proj4";
import { getAllPointEau } from "@/service/pointEauService";
import ButtonLog from '@/components/ButtonLog';

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

// Page Accueil (Public) carte interactive qui localisation / affiche les points d'eau incendie / itinéraire ou signaler un problème sur les points d'eau
export default function HomeScreen() {
  const [localisation, setLocalisation] = useState<Location.LocationObject | null>(null);
  const [pointsEau, setPointsEau] = useState<PointEau[]>([]);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedPEI, setSelectedPEI] = useState<PointEau | null>(null);
  const router = useRouter();

  // Référence pour piloter la carte
  const referenceCarte = useRef<MapView>(null);

  // Charge les points d'eau et active le GPS
  useEffect(() => {
    let watchAbonnement: Location.LocationSubscription | null = null;

    const fetchPointsEau = async () => {
      try {
        const response = await getAllPointEau();

        // Conversion du format (Lambert93) vers le format GPS (WGS84)
        const lambert93 = "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs";
        const wgs84 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

        const pointsRaw = Array.isArray(response) ? response : response.points_eau;

        const pointsEauWGS84 = pointsRaw.map((p: any) => {
          const [lon, lat] = proj4(lambert93, wgs84, [p.longitude, p.latitude]);
          return { ...p, latitude: lat, longitude: lon };
        });

        setPointsEau(pointsEauWGS84);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

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

    fetchPointsEau();
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
  const infoPointEau = (point: PointEau) => {
    setSelectedPEI(point);
    setModalVisible(true);
  };

  if (loading || !location) {
    return (
      <View style={styles.loader}>
        <ActivityIndicator size="large" color="#1976D2" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <HautPage title="Carte des points d’eau" />

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
        showsUserLocation // Affiche le point bleu
      >
        {pointsEau.slice(0, 100).map((point) => (
          <Marker
            key={point.id}
            coordinate={{ latitude: point.latitude, longitude: point.longitude }}
            title={`Numero PEI : ${point.numero_pei}`}
            description="Cliquez ici pour avoir plus d'infos"
            onCalloutPress={() => infoPointEau(point)}
          />
        ))}
      </MapView>

      {/* Bouton retour a la Positions */}
      <TouchableOpacity style={styles.boutonLocalisation} onPress={allerPosition}>
        <FontAwesome name="location-arrow" size={24} color="#FFF" />
      </TouchableOpacity>
      
      {/* Description des points d'eau */}
      <Modal transparent animationType="fade" visible={modalVisible}>
        <View style={styles.overlay}>
          <View style={styles.alertBox}>
            <Text style={styles.title}>
              Numero PEI : {selectedPEI?.numero_pei}
            </Text>

            <Text style={styles.message}>
              Statut : {selectedPEI?.statut}{"\n"}
              Type : {selectedPEI?.type_nature ?? "N/A"}{"\n"}
              Pression : {selectedPEI?.press_deb ?? "N/A"} bar{"\n"}
              Débit : {selectedPEI?.debit_1_bar ?? "N/A"} m3/h{"\n"}
              Volume d'eau : {selectedPEI?.vol_eau_mil ?? "N/A"}
            </Text>

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
});

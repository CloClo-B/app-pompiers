import axios from "axios";
import { FontAwesome } from '@expo/vector-icons';
import * as Location from 'expo-location';
import React, { useEffect, useRef, useState } from 'react';
import { Alert, ActivityIndicator, StyleSheet, TouchableOpacity, View } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import HautPage from '../hautPage';
import proj4 from "proj4";

const API_URL = "http://192.168.1.178:8000/points-eau/";

// valentin : 172.20.10.2 | 192.168.1.184

type PointEau = {
  id: number;
  numero_pei: string;
  nom: string | null;
  statut: string;
  latitude: number;
  longitude: number;
  press_deb: number | null;
  debit_1_bar: number | null;
};

export default function HomeScreen() {
  const [localisation, setLocalisation] = useState<Location.LocationObject | null>(null);
  const [pointsEau, setPointsEau] = useState<PointEau[]>([]);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const referenceCarte = useRef<MapView>(null);

  useEffect(() => {
    let watchAbonnement: Location.LocationSubscription | null = null;

    const fetchPointsEau = async () => {
      try {
        const response = await axios.get(API_URL);
        // affichage des données
        // console.log("Données reçues:", response.data);

        const lambert93 =
          "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs";
        const wgs84 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

        const pointsRaw = Array.isArray(response.data) ? response.data : response.data.points_eau;

        if (!pointsRaw) {
          console.error("Impossible de récupérer les points d'eau :", response.data);
          setLoading(false);
          return;
        }

        const pointsEauWGS84 = pointsRaw.map((p: any) => {
          const [lon, lat] = proj4(lambert93, wgs84, [p.longitude, p.latitude]);
          return { ...p, latitude: lat, longitude: lon };
        });

        setPointsEau(pointsEauWGS84);
      } catch (error) {
        console.error("Erreur lors du chargement des points d'eau :", error);
        Alert.alert("Erreur", "Impossible de récupérer les points d’eau.");
      } finally {
        setLoading(false);
      }
    };

    const getLocation = async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        Alert.alert("Permission refusée", "Impossible d'accéder à la localisation.");
        return;
      }

      const loc = await Location.getCurrentPositionAsync({});
      setLocalisation(loc);
      setLocation({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });

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

      <MapView
        ref={referenceCarte}
        style={styles.map}
        initialRegion={{
          latitude: location.latitude,
          longitude: location.longitude,
          latitudeDelta: 0.2,
          longitudeDelta: 0.2,
        }}
        showsUserLocation
        showsMyLocationButton = {true}
      >
        {pointsEau.map((point) => (
          <Marker
            key={point.id}
            coordinate={{ latitude: point.latitude, longitude: point.longitude }}
            title={point.numero_pei}
            description={`Pression: ${point.press_deb ?? "-"} bars | Débit: ${point.debit_1_bar ?? "-"} L/min`}
            pinColor="red"
          />

        ))}
      </MapView>

      <TouchableOpacity style={styles.boutonLocalisation} onPress={allerPosition}>
        <FontAwesome name="location-arrow" size={24} color="#FFF" />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  boutonLocalisation: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    backgroundColor: '#007AFF',
    borderRadius: 30,
    width: 60,
    height: 60,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    elevation: 5,
  },
  loader: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});



// exemple format:
// {"id": 11362, "latitude": 6788543, "longitude": 225566, "nom": "", "numero_pei": "562100009", "statut": "PUBLIC"}
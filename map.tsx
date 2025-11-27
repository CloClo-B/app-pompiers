import axios from "axios";
import * as Location from "expo-location";
import proj4 from "proj4";
import { useEffect, useState } from "react";
import { ActivityIndicator, Alert, StyleSheet, View } from "react-native";
import MapView, { Marker } from "react-native-maps";

const API_URL = "http://192.168.1.132:8000/points_eau";

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

export default function App() {
  const [pointsEau, setPointsEau] = useState<PointEau[]>([]);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);

  useEffect(() => {
    const fetchPointsEau = async () => {
      try {
        const response = await axios.get(API_URL);

        // Projection Lambert 93 → WGS84
        const lambert93 =
          "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs";
        const wgs84 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

        const pointsEauWGS84 = response.data.points_eau.map((p: any) => {
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
      setLocation({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });
    };

    fetchPointsEau();
    getLocation();
  }, []);

  if (loading || !location) {
    return (
      <View style={styles.loader}>
        <ActivityIndicator size="large" color="#1976D2" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: location.latitude,
          longitude: location.longitude,
          latitudeDelta: 0.2,
          longitudeDelta: 0.2,
        }}
        showsUserLocation
        showsMyLocationButton
      >
        {pointsEau.map((point) => (
          <Marker
            key={point.id}
            coordinate={{ latitude: point.latitude, longitude: point.longitude }}
            title={point.numero_pei}
            description={`Pression: ${point.press_deb ?? "-"} bars | Débit: ${point.debit_1_bar ?? "-"} L/min`}
            pinColor="red" // flèche rouge sans image
          />
        ))}
      </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { flex: 1 },
  loader: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});

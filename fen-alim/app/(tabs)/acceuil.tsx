import { FontAwesome } from '@expo/vector-icons';
import * as Location from 'expo-location';
import React, { useEffect, useRef, useState } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';
import MapView from 'react-native-maps';
import HautPage from '../hautPage';

export default function HomeScreen() {
  const [localisation, setLocalisation] = useState<Location.LocationObject | null>(null);
  const referenceCarte = useRef<MapView>(null);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        return;
      }

      const abonnement = await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.High,
          timeInterval: 5000,
          distanceInterval: 10,
        },
        (nouvelleLocalisation) => {
          setLocalisation(nouvelleLocalisation);
        }
      );

      return () => {
        if (abonnement) abonnement.remove();
      };
    })();
  }, []);

  const allerPosition = () => {
    if (referenceCarte.current && localisation) {
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

  return (
    <View style={styles.container}>
      <HautPage title="Carte des points d’eau" />

      {localisation && (
        <MapView
          ref={referenceCarte}
          style={styles.map}
          initialRegion={{
            latitude: localisation.coords.latitude,
            longitude: localisation.coords.longitude,
            latitudeDelta: 0.01,
            longitudeDelta: 0.01,
          }}
          showsUserLocation={true}
        />
      )}

      {localisation && (
        <TouchableOpacity style={styles.boutonLocalisation} onPress={allerPosition}>
          <FontAwesome name="location-arrow" size={24} color="#FFF" />
        </TouchableOpacity>
      )}
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
});

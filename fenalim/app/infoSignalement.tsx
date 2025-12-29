import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Button, TouchableOpacity, Alert, Image, ScrollView, Platform, Linking } from "react-native";
import HautPage from './hautPage';
import axios from "axios";
import { router, useLocalSearchParams} from 'expo-router';
import proj4 from "proj4";
import AsyncStorage from '@react-native-async-storage/async-storage';


type Signale = {
  id: string;
  id_point: string;
  probleme: string;
  photo: string;
  id_utilisateur: string;
  date_creation: string;
};
type lePoint = {
  latitude: number;
  longitude: number;
};

export default function UserDetails() {
  const [token, setToken] = useState<string | null>(null);
  
  // récupérer le token 
  useEffect(() => {
    getData();
  }, []);
  const getData = async () => {
    try {
      const value = await AsyncStorage.getItem('@token')
      if(value !== null) {
        setToken(value);
        infoSignalementSelect(value);
      }
    } catch(e) {
      console.log("erreur token affichage utilisateur");
    }
  }

  const [chargement, setChargement] = useState(true);
  const [signalement, setSignalement] = useState<Signale | null>(null);
  const [pointSignale, setPointSignale] = useState<lePoint | null>(null);

  const params = useLocalSearchParams();
  const id_s = params.id_s as string

  
  const infoSignalementSelect = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible d'afficher les missions en cours");
      return;
    }
    try {
      console.log("iddddd", id_s)
      const response = await axios.get(`http://192.168.1.178:8000/signaler/id_s/${id_s}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      // affichage des données
      console.log("Données reçues:", response.data);
      
      setSignalement({
        id: String(response.data.id),
        id_point: response.data.id_point,
        probleme: response.data.probleme,
        photo: response.data.photo,
        id_utilisateur: String(response.data.id_utilisateur),
        date_creation: String(response.data.date_creation),
      });
      fetchPointsEau(response.data.id_point);

  } catch (error) {
    console.error("Erreur lors du chargement du signalement :", error);
    Alert.alert("Erreur", "Impossible de récupérer le signalement.");
  } finally {
      setChargement(false);
    }
  };

  const fetchPointsEau = async (id_point: string) => {
    try {
      // affichage des données
      // console.log("Données reçues:", response.data);
      
      const response = await axios.get(`http://192.168.1.178:8000/points-eau/${id_point}`);
      const point = response.data; 
      if (point) {
        const lambert93 = "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs";
        const wgs84 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";
        const [longitude, latitude] = proj4(lambert93, wgs84, [point.longitude, point.latitude]);

        setPointSignale({
          latitude,
          longitude,
        });
      } 
    } 
    catch (error) {
      console.error("Erreur lors du chargement du points d'eau :", error);
      Alert.alert("Erreur", "Impossible de récupérer le point d'eau.");
    } 
    finally {
      setChargement(false);
    }
  };


  return (

    <>

      <View>
        <HautPage title="point signalé" />
      </View>
      
      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
        <View style={styles.container}>
            <TouchableOpacity style={[{width: 150, height: 45, alignSelf: 'flex-start' }]} onPress={() => router.navigate('/point_eau')}>
                <Text style={{color:'#000', fontWeight:'bold', fontSize:22}}>&lt; Retour</Text>
            </TouchableOpacity>

          <View style={styles.card}>
            <Text style={styles.titre}>Signalement</Text>
              

            {/* Infos */}
            <View style={{ gap: 10 }}>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID signalement : </Text>{signalement?.id}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID du point signaler : </Text> {signalement?.id_point}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date du signalement : </Text> {signalement?.date_creation ? new Date(signalement.date_creation).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Heure du signalement : </Text> {signalement?.date_creation ? new Date(signalement.date_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Signaler par : </Text> {signalement?.id_utilisateur}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Problème : </Text> {signalement?.probleme}</Text>
              {signalement?.photo && (
                <Image
                  source={{ uri: `http://192.168.1.178:8000/${signalement.photo}` }}
                  style={{ width: 300, height: 250, borderRadius: 10, marginTop: 10, marginBottom:10 }}
                  resizeMode="cover"
                />
              )}
            </View>

            
            {/* BOUTONS */}
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 10 }}>
                <TouchableOpacity
                  style={[styles.boutton ,{ backgroundColor: '#457B9D', width: 150, height: 45 }]}
                  onPress={() => {
                    const latitude = pointSignale?.latitude;
                    const longitude = pointSignale?.longitude;
                
                    let url = "";
                    if (Platform.OS === "ios") {
                      // Apple Maps
                      url = `http://maps.apple.com/?daddr=${latitude},${longitude}&dirflg=d`;
                    } else {
                      // Android / Google Maps
                      url = `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`;
                    }
                
                    Linking.openURL(url).catch((err) =>
                      console.error("Impossible d'ouvrir l'application de navigation", err)
                    );
                  }}
                >
                  <Text style={{ color: '#FFF'}}>Itinéraire</Text>
                </TouchableOpacity>

              <TouchableOpacity style={[styles.boutton, { backgroundColor: '#457B9D', width: 150, height: 45 }]} onPress={() => router.push({ pathname: '/marquerResolu', params: { id_s: id_s } })}>
                <Text style={{color:'#ffffff'}}>Marquer resolu</Text>
              </TouchableOpacity>
            </View>


          </View>
        </View>
        </ScrollView>
    </>
  );
}


const styles = StyleSheet.create({
  contenue: {
    marginTop: 40,
    
    alignItems: 'center',
    justifyContent: 'center',
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  },
  card: {
    width: '90%',      
    height: '100%',      
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,     
    justifyContent: 'space-between'
  },

  titre: {
    textAlign: "center",
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 15
  },
  infoBloc: {
    gap: 13,
  },
  btnRow: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 15
  },
  btn: {
    flex: 1
  },
  tout:{
    alignSelf: 'center',
    alignItems: "center",
    marginTop: 20,
  },
  boutton:{
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
  },
  titre2: {
    textAlign: 'center',
    color: '#1D3557',
    fontSize: 25,
    marginBottom: 30,
  }
});

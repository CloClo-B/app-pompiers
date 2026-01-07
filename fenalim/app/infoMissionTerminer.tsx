import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Alert, Image, ScrollView, Platform, Linking } from "react-native";
import HautPage from './hautPage';
import axios from "axios";
import {useLocalSearchParams} from 'expo-router';
import proj4 from "proj4";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { getData } from '@/config/recupRole'; 
import { naviguerMission } from '@/config/navigation';
import { API_ENDPOINTS } from '@/config/api';


type Mission = {
  id_mission: string;
  nom_mission: string;
  commentaire: string;
  address:string;
  id_utilisateur: string;
  date_creation: string;
  date_fin: string;
};
type lePoint = {
  latitude: number;
  longitude: number;
};
 
export default function MissionDetails() {
  const [mission, setMission] = useState<Mission | null>(null);
  const [pointMission, setPointMission] = useState<lePoint | null>(null);


  const [token, setToken] = useState<string | null>(null);
  const [userRole, setUserRole] = useState<string | null>(null);
    
  useEffect(() => {
    const chargerRoleEtToken = async () => {
      try {
        // recup role et token
        const tokenValue = await AsyncStorage.getItem('@token');
        const roleValue = await getData();
        if (tokenValue){
          setToken(tokenValue);
        }
        if (roleValue){
          setUserRole(roleValue);
        }
        // afficher info
        if (tokenValue) {
          infoMissionSelect(tokenValue); 
        }
      } 
      catch (e) {
        console.log("erreur récupération token ou rôle");
      }
    };

    chargerRoleEtToken();
  }, []);

  // recuperer l'id de la mission 
  const params = useLocalSearchParams();
  const id_m = Number(params.id_m);


  // calculer la durée total de la mission
  const calculerDuree = (dateDebut: string, dateFin: string) => {
    const debut = new Date(dateDebut).getTime();
    const fin = new Date(dateFin).getTime();

    const diffMs = fin - debut;
    const diffHeures = Math.floor(diffMs / (1000 * 60 * 60));
    const jours = Math.floor(diffHeures / 24);
    const heures = diffHeures % 24;

    if (jours > 0) {
      return `${jours} j ${heures} h`;
    }
    return `${heures} h`;
  };


  
  // recuperer la mission
  const infoMissionSelect = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible d'afficher la missions séléctionne");
      return;
    }
    try {
      console.log("iddddd", id_m)
      const responseMission = await axios.get(API_ENDPOINTS.MISSION_BY_ID(id_m), {
        headers: { Authorization: `Bearer ${token}` },
      });

      // affichage des données
      console.log("Données reçues :", responseMission.data);
      
      setMission({
        id_mission: String(responseMission.data.id_mission),
        nom_mission: responseMission.data.nom_mission,
        commentaire: responseMission.data.commentaire,
        address: responseMission.data.itineraire,
        id_utilisateur: String(responseMission.data.id_utilisateur),
        date_creation: String(responseMission.data.date_creation),
        date_fin: String(responseMission.data.date_fin)
      });

      fetchPointsEau(responseMission.data.id_point);

    }  
    catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            console.error("Erreur Axios:", err.response?.data || err.message);
            Alert.alert("Erreur", "Impossible de récupérer la mission");
        } 
        else {
            console.error("Erreur inconnue:", err);
            Alert.alert("Erreur", "Impossible de récupérer la mission");
        }
    };
  }


  // recuperer localisation du point d'eau   
  const fetchPointsEau = async (id_point: string) => {
    try {
      // affichage des données
      // console.log("Données reçues:", response.data);
      
      const response = await axios.get(API_ENDPOINTS.POINT_EAU_BY_ID(id_point));
      const point = response.data; 
      if (point) {
        const lambert93 = "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs";
        const wgs84 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";
        const [longitude, latitude] = proj4(lambert93, wgs84, [point.longitude, point.latitude]);

        setPointMission({
          latitude,
          longitude, 
        });
      } 
    } 
    catch (error) {
      console.error("Erreur lors du chargement du points d'eau :", error);
      Alert.alert("Erreur", "Impossible de récupérer le point d'eau.");
    } 
  };


  return (

    <>

      <View>
        <HautPage title="Information mission terminer" />
      </View>
      
      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
        <View style={styles.container}>
          <View style={styles.card}>
           {/* nom de la mission */}
            <Text style={styles.titre}>{mission?.nom_mission}</Text>
              

            {/* Infos de la mission*/}
            <View style={{ gap: 10 }}>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Détails de la mission : </Text> {mission?.commentaire}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Adresse : </Text> {mission?.address}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date de début : </Text> {mission?.date_creation ? new Date(mission.date_creation).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date de fin : </Text> {mission?.date_fin ? new Date(mission.date_fin).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Durée : </Text>{mission?.date_fin ? calculerDuree(mission.date_creation, mission.date_fin): ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID de l'utilisateur qui à créer la mission : </Text> {mission?.id_utilisateur}</Text>
            </View>

            
            {/* BOUTONS */}
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 10 }}>
              <TouchableOpacity style={[styles.boutton, { backgroundColor: '#457B9D', width: 150, height: 45 }]} onPress={() => {if (userRole) naviguerMission(userRole); else alert("Rôle utilisateur introuvable"); } }>
                <Text style={{color:'#ffffff'}}>Fermer</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.boutton ,{ backgroundColor: '#457B9D', width: 150, height: 45 }]}
                onPress={() => {
                    const latitude = pointMission?.latitude;
                    const longitude = pointMission?.longitude;
                    
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
                    <Text style={{ color: '#FFF'}}>Afficher le point</Text>
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

  boutton:{
    marginTop: 15,
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
  },
});

import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Alert, Image, ScrollView, Platform, Linking } from "react-native";
import HautPage from '@/app/hautPage';
import axios from "axios";
import {useLocalSearchParams} from 'expo-router';
import proj4 from "proj4";
import { naviguerMission } from '@/config/navigation';
import { getMissionById } from "@/service/MissionService";
import { getPointEauByID } from "@/service/pointEauService";
import { getRole, getToken } from "@/service/infosStocker";
import ButtonLog from '@/components/ButtonLog';

// Donnée de la Mission
type Mission = {
  id_mission: string;
  nom_mission: string;
  commentaire: string;
  address:string;
  mail_utilisateur: string;
  date_creation: string;
  date_fin: string;
};
type lePoint = {
  latitude: number;
  longitude: number;
};

// Permet de consulter l'historique d'une intervention
export default function MissionDetails() {
  const [mission, setMission] = useState<Mission | null>(null);
  const [pointMission, setPointMission] = useState<lePoint | null>(null);

  const [userRole, setUserRole] = useState<string | null>(null);
    
  useEffect(() => {
    const chargerRoleEtToken = async () => {
      try {
        // recup role et token
        const tokenValue =  await getToken();
        const roleValue = await getRole();

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
      Alert.alert("Erreur" +"impossible d'afficher la mission séléctionnée");
      return;
    }
    try {
      console.log("iddddd", id_m)

      // apelle du fichier missionService pour la recuperer les données
      const reponseMission = await getMissionById(token, id_m);

      // affichage des données
      console.log("Données reçues :", reponseMission);
      
      setMission({
        id_mission: String(reponseMission.id_mission),
        nom_mission: reponseMission.nom_mission,
        commentaire: reponseMission.commentaire,
        address: reponseMission.itineraire,
        mail_utilisateur: String(reponseMission.mail_utilisateur),
        date_creation: String(reponseMission.date_creation),
        date_fin: String(reponseMission.date_fin)
      });

      fetchPointsEau(reponseMission.id_point, token);

    }  
    catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            console.error("Erreur Axios:", err.response);
            Alert.alert("Erreur", "Impossible de récupérer la mission");
        } 
        else {
            console.error("Erreur inconnue:", err);
            Alert.alert("Erreur", "Impossible de récupérer la mission");
        }
    };
  }


  // recuperer localisation du point d'eau   
  const fetchPointsEau = async (id_point: string, token: string) => {
    if (!token) {
      Alert.alert("Erreur" +"impossible d'afficher la mission séléctionnée");
      return;
    }
    try {
      // apelle du fichier pointEauSercice pour la envoyer la requete de recuperation par id Point
      const point = await getPointEauByID(token, id_point);      
      
      // affichage des données
      // console.log("Données reçues:", reponse);
      
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
      console.error("Erreur lors du chargement du point d'eau :", error);
      Alert.alert("Erreur", "Impossible de récupérer le point d'eau.");
    } 
  };


  return (

    <>

      <View>
        <HautPage title="Information mission terminée" />
      </View>
      
      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
        <View style={styles.container}>
          <View style={styles.card}>
           {/* nom de la mission */}
            <Text style={styles.titre}>{mission?.nom_mission}</Text>
              

            {/* Infos de la mission*/}
            <View style={{ gap: 15 }}>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Détails de la mission : </Text> {mission?.commentaire}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Adresse : </Text> {mission?.address}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date de début : </Text> {mission?.date_creation ? new Date(mission.date_creation).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date de fin : </Text> {mission?.date_fin ? new Date(mission.date_fin).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Durée : </Text>{mission?.date_fin ? calculerDuree(mission.date_creation, mission.date_fin): ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Email créateur de la mission : </Text> {mission?.mail_utilisateur}</Text>
            </View>

            
            {/* BOUTONS */}
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 10, marginTop: 30 }}>
              <ButtonLog label="FERMER" onPress={() => { if (userRole) naviguerMission(userRole); else alert("Rôle utilisateur introuvable"); }} 
              type="primary" width={150} height={45}/>

              <ButtonLog
                label="VOIR LIEU"
                onPress={() => {
                  const latitude = pointMission?.latitude;
                  const longitude = pointMission?.longitude;
                  let url = Platform.OS === "ios"
                    ? `http://maps.apple.com/?daddr=${latitude},${longitude}&dirflg=d`
                    : `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`;
                  Linking.openURL(url).catch(err => console.error("Impossible d'ouvrir l'application de navigation", err));
                }}
                type="primary" width={150} height={45}
              />
            </View>


          </View>
        </View>
        </ScrollView>
    </>
  );
}

// Style
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
    fontSize: 30,
    fontWeight: "bold",
    marginBottom: 30
  },

  boutton:{
    marginTop: 15,
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
  },
});

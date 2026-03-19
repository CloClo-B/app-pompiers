import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Alert, Image, ScrollView, Platform, Linking } from "react-native";
import HautPage from '@/app/hautPage';
import { router, useLocalSearchParams} from 'expo-router';
import proj4 from "proj4";
import { naviguerPointEau } from '@/config/navigation';
import { API_ENDPOINTS } from '@//config/api';
import { getSignalementByIndex } from "@/service/signalementService";
import { getPointEauByID } from "@/service/pointEauService";
import { getRole, getToken } from "@/service/infosStocker";
import ButtonLog from '@/components/ButtonLog';

// Donnée du Signalement
type Signale = {
  id: string;
  id_point: string;
  probleme: string;
  photo: string;
  mail_utilisateur: string;
  date_creation: string;
};
type lePoint = {
  latitude: number;
  longitude: number;
};

// Permet de consulter les informations d'un Signalement
export default function UserDetails() {
  const [token, setToken] = useState<string | null>(null);
  const [userRole, setUserRole] = useState<string | null>(null);
    
  useEffect(() => {
    const chargerRoleEtToken = async () => {
      try {
        // recup role et token
        const tokenValue = await getToken();
        const roleValue = await getRole();
        if (tokenValue){
          setToken(tokenValue);
        }
        if (roleValue){
          setUserRole(roleValue);
        }
        // afficher info
        if (tokenValue) {
          infoSignalementSelect(tokenValue); 
        }
      } 
      catch (e) {
        console.log("erreur de récupération du token ou du rôle");
      }
    };

    chargerRoleEtToken();
  }, []);

  const [signalement, setSignalement] = useState<Signale | null>(null);
  const [pointSignale, setPointSignale] = useState<lePoint | null>(null);

  const params = useLocalSearchParams();
  const id_s = params.id_s as string

  
  const infoSignalementSelect = async (token: string) => {
    if (!token) {
      alert("Impossible d'afficher les signalements en cours");
      return;
    }
    try {
      console.log("iddddd", id_s)
      
      // appel du fichier signalementService pour recuperer le signalement EN FONCTION DE L'INDEX DU TABLEAU
      const reponse = await getSignalementByIndex(token, id_s);

      // affichage des données
      console.log("Données reçues:", reponse);
      
      setSignalement({
        id: String(reponse.id),
        id_point: reponse.id_point,
        probleme: reponse.probleme,
        photo: reponse.photo,
        mail_utilisateur: String(reponse.mail_utilisateur),
        date_creation: String(reponse.date_creation),
      });
      fetchPointsEau(reponse.id_point, token);

  } catch (error) {
    console.error("Erreur lors du chargement du signalement :", error);
    Alert.alert("Erreur", "Impossible de récupérer le signalement.");
  }
  };

  const fetchPointsEau = async (id_point: string, token: string) => {
    if (!token) {
      Alert.alert("Erreur", "Impossible de récupérer le point d'eau.");
      return;
    }
    try {
      // affichage des données
      // console.log("Données reçues:", reponse);
      
      // appel du fichier pointEauService pour la envoyer la requete de recuperation par id Point
      const point = await getPointEauByID(token, id_point);      
      
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
  };


  return (

    <>

      <View>
        <HautPage title="point signalé" />
      </View>
      
      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
        <View style={styles.container}>
            <TouchableOpacity style={[{width: 150, height: 45, alignSelf: 'flex-start' }]} onPress={() => {if (userRole) naviguerPointEau(userRole); else alert("Rôle utilisateur introuvable"); }}>
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
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Signaler par : </Text> {signalement?.mail_utilisateur}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Problème : </Text> {signalement?.probleme}</Text>
              {signalement?.photo && (
                <Image
                  source={{ uri: API_ENDPOINTS.GET_IMAGE_SIGNALEMENT(signalement.photo) }}
                  style={{ width: 300, height: 250, borderRadius: 10, marginTop: 10, marginBottom:10 }}
                  resizeMode="cover"
                />
              )}
            </View>

            
            {/* BOUTONS */}
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 10 }}>

                <ButtonLog label="Itinéraire" onPress={() => {
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
                      console.error("Impossible d'ouvrir l'application de navigation", err));
                    }} type="primary" width={150} height={45}
                />

              <ButtonLog
                label="Marquer résolu"
                onPress={() => router.push({ pathname: '/marquerResolu', params: { id_s: id_s } })}
                type="primary" width={150} height={45}/>

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
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 15
  },
});

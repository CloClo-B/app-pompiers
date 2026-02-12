import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Button, TouchableOpacity, Alert, Image, ScrollView, Platform, Linking } from "react-native";
import HautPage from './hautPage';
import { router, useLocalSearchParams} from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { naviguerPointEau } from '@/config/navigation';
import { getData } from '@/config/recupRole';
import { API_ENDPOINTS } from '@/config/api';
import { deleteSignalement, getSignalementByIndex } from "@/service/signalementService";

// Donnée du Signalement
type Signale = {
  id: string;
  id_point: string;
  probleme: string;
  photo: string;
  mail_utilisateur: string;
  date_creation: string;
};

// Permet de consulter les détails d'un signalement et de le résoudre
export default function UserDetails() {
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
          infoSignalementSelect(tokenValue); 
        }
      } 
      catch (e) {
        console.log("erreur récupération token ou rôle");
      }
    };

    chargerRoleEtToken();
  }, []);


  const [signalement, setSignalement] = useState<Signale | null>(null);

  const params = useLocalSearchParams();
  const id_s = params.id_s as string

  // Charge les infos du signalement
  const infoSignalementSelect = async (token: string) => {
    if (!token) {
      Alert.alert("Erreur", "Impossible d'afficher les missions en cours");
      return;
    }
    try {
      console.log("iddddd", id_s)
      // apelle du fichier signalementService pour recuperer le signalement EN FONCTION DE L'INDEX DU TABLEAU
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

  } catch (error) {
    console.error("Erreur lors du chargement du signalement :", error);
    Alert.alert("Erreur", "Impossible de récupérer le signalement.");
  }
  };

  // Supprime le signalement
  const suprimmerSignalement = async () => {

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification de l'id à envoyer pour supprimer\n");
    console.log("IDPoint:", signalement?.id_point);

    if (!token) {
      Alert.alert("Erreur, impossible de supprimer le signalement");
      return;
    }
    try {
        
      // apelle du fichier signalementService pour supprimer le signalement via son id
      await deleteSignalement(token, signalement!.id_point);

        
      router.push({
          pathname: '/succes',
          params: { title: 'Signalement suprrimer avec succès', page:"point_eau" }
          });
      } catch (error) {
          console.error(error);
          Alert.alert("Erreur", "Supresion signalement");
      }
    };



  return (

    <>

      <View>
        <HautPage title="Confirmer la résolution" />
      </View>
      
      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
        <View style={styles.container}>
 
          <View style={styles.card}>
            <Text style={styles.titre}>Confirmer la résolution du signalement</Text>
              

            {/* Infos*/}
            <View style={{ gap: 10 }}>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID signalement : </Text>{signalement?.id}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID du point signaler : </Text> {signalement?.id_point}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date du signalement : </Text> {signalement?.date_creation ? new Date(signalement.date_creation).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Heure du signalement : </Text> {signalement?.date_creation ? new Date(signalement.date_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Signaler par : </Text> {signalement?.mail_utilisateur}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Problème : </Text> {signalement?.probleme}</Text>
              {signalement?.photo && (
                <Image
                  source={{ uri: API_ENDPOINTS.IMAGE(signalement.photo) }}
                  style={{ width: 300, height: 250, borderRadius: 10, marginTop: 10, marginBottom:10 }}
                  resizeMode="cover"
                />
              )}
            </View>


            
            {/* BOUTONS */}
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 10 }}>
              <TouchableOpacity style={[styles.boutton, { backgroundColor: '#457B9D', width: 150, height: 45 }]}  onPress={() => {if (userRole) naviguerPointEau(userRole); else alert("Rôle utilisateur introuvable"); }}>
                <Text style={{color:'#ffffff'}}>Annuler</Text>
              </TouchableOpacity>
              <TouchableOpacity style={[styles.boutton, { backgroundColor: '#457B9D', width: 150, height: 45 }]} onPress={suprimmerSignalement}>
                <Text style={{color:'#ffffff'}}>Valider</Text>
              </TouchableOpacity>
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
  boutton:{
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
  },

});

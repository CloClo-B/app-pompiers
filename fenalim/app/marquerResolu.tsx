import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Button, TouchableOpacity, Alert, Image, ScrollView, Platform, Linking } from "react-native";
import HautPage from './hautPage';
import axios from "axios";
import { router, useLocalSearchParams} from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { naviguerPointEau } from '../config/navigation';
import { getData } from "../config/recupRole"; 


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


  const infoSignalementSelect = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible d'afficher les missions en cours");
      return;
    }
    try {
      console.log("iddddd", id_s)
      const response = await axios.get(`http://192.168.2.215:8000/signaler/id_s/${id_s}`, {
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
  } catch (error) {
    console.error("Erreur lors du chargement du signalement :", error);
    Alert.alert("Erreur", "Impossible de récupérer le signalement.");
  }
  };

  
  const suprimmerSignalement = async () => {

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification de l'id à envoyer pour supprimer\n");
    console.log("IDPoint:", signalement?.id_point);


        try {
        
        const response = await axios.delete(`http://192.168.2.215:8000/signaler/suprimmer/${signalement?.id_point}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
        
        router.push({
            pathname: '/succes',
            params: { title: 'Signalement suprrimer avec succès', page:"point_eau" }
            });
        } catch (error) {
            console.error(error);
            alert('Erreur lors de la supression du signalement');
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
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date du signalement : </Text>  {signalement?.date_creation ? new Date(signalement.date_creation).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Heure du signalement : </Text>  {signalement?.date_creation ? new Date(signalement.date_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Signaler par : </Text> {signalement?.id_utilisateur}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Problème : </Text> {signalement?.probleme}</Text>
              {signalement?.photo && (
                <Image
                  source={{ uri: `http://192.168.2.215:8000/${signalement.photo}` }}
                  style={{ width: 300, height: 200, borderRadius: 10, marginTop: 10, marginBottom:10 }}
                  resizeMode="cover"
                />
              )}
            </View>


            {/* possibilité d'ajouter photo de preuve par la suite */}
            
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

import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Button, TouchableOpacity, Alert } from "react-native";
import HautPage from './hautPage';
import axios from "axios";
import { router, useLocalSearchParams } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';


type User = {
  id: string;
  nom: string;
  prenom: string;
  role: string;
  email: string;
  telephone: string;
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
        infoUtilisateurSelect(value);
      }
    } catch(e) {
      console.log("erreur token affichage utilisateur");
    }
  }
  const [chargement, setChargement] = useState(true);
  const [utilisateur, setUtilisateur] = useState<User | null>(null);
  const params = useLocalSearchParams();
  const id = params.id as string


  
  const infoUtilisateurSelect = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible d'afficher les missions en cours");
      return;
    }
    try {
      console.log("iddddd", id)
      const response = await axios.get(`http://192.168.1.178:8000/utilisateurs/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      // affichage des données
      console.log("Données reçues:", response.data);
      
      setUtilisateur({
        id: String(response.data.id_utilisateur),
        nom: response.data.nom,
        prenom: response.data.prenom,
        role: response.data.role,
        email: response.data.email,
        telephone: response.data.telephone,
      });
  } catch (error) {
    console.error("Erreur lors du chargement des utilisateur :", error);
    Alert.alert("Erreur", "Impossible de récupérer l'utilisateur.");
  } finally {
      setChargement(false);
    }
  };


  return (

    <>

      <View>
        <HautPage title="Utilisateur" />
      </View>
      
      
      <View style={styles.container}>

        <View style={styles.card}>

          {/* Card de l'utilisateur */}
          <Text style={styles.titre}>utilisateur</Text>

          {/* Infos exemple en statique*/}
          <View style={{ gap: 10 }}>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID : </Text>{utilisateur?.id}</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Rôle : </Text> {utilisateur?.role}</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Nom : </Text> {utilisateur?.nom}</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Prénom : </Text> {utilisateur?.prenom}</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Email : </Text> {utilisateur?.email}</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Téléphone : </Text> {utilisateur?.telephone}</Text>
          </View>

          
          {/* BOUTONS */}
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 10 }}>
            <TouchableOpacity style={[styles.boutton ,{ backgroundColor: '#457B9D', width: 150, height: 45 }]} onPress={() => router.navigate('/(tabs_admin)/utilisateur')}>
                <Text style={{color:'#ffffff'}}>FERMER</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.boutton, { backgroundColor: '#457B9D', width: 150, height: 45 }]} onPress={() => console.log("appliquer")}>
              <Text style={{color:'#ffffff'}}>APPLIQUER</Text>
            </TouchableOpacity>
          </View>


        </View>
      </View>

    </>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  },
  card: {
    width: 340,      
    height: 370,      
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

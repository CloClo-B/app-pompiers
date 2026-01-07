import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, Alert } from 'react-native';
import HautPage from '../hautPage';
import { router, useRouter } from 'expo-router';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_ENDPOINTS } from '../../config/api';


const roue = require('@/assets/images/parametres.png');
type User = {
  id: string;
  nom: string;
  prenom: string;
  role: string;
  email: string;
  telephone: string;
};


export default function HomeScreen() {
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
        fetchUtilisateurs(value);
      }
    } catch(e) {
      console.log("erreur token affichage utilisateur");
    }
  }

  const [chargement, setChargement] = useState(true);
  const [utilisateur, setUtilisateur] = useState<User[]>([]);
  
  const router = useRouter();
  
  const renderItem = ({ item }: { item: User }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.nom}</Text>
      <Text style={styles.cell}>{item.prenom}</Text>
      <Text style={styles.cell}>{item.role}</Text>
      <TouchableOpacity onPress={() => router.push({ pathname: '/infoUtilisateur', params: { id: item.id } })}>
        <Image source={roue} style={styles.cellImage} />
      </TouchableOpacity>
    </View>
  );
  

  const fetchUtilisateurs = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible d'afficher les missions en cours");
      return;
    }
    try {
      const response = await axios.get(API_ENDPOINTS.REGISTER, {
      headers: { Authorization: `Bearer ${token}` },
    });
      // affichage des données
      console.log("Données reçues:", response.data);
      
      const UtilisateurRaw = Array.isArray(response.data) ? response.data : response.data.utilisateurs;

      if (!UtilisateurRaw) {
        console.error("Impossible de récupérer les utlisateur:", response.data);
        setChargement(false);
        return;
      }
      
    const lesUtilisateurs: User[] = UtilisateurRaw.map((u: any) => ({
      id: String(u.id_utilisateur),
      nom: u.nom,
      prenom: u.prenom,
      role: u.role,
      email: u.email,
      telephone: u.telephone,
    }));
    
    
    
    setUtilisateur(lesUtilisateurs);
  } catch (error) {
      console.error("Erreur lors du chargement des utilisateur :", error);
      Alert.alert("Erreur", "Impossible de récupérer les utilisateurs.");
    } finally {
      setChargement(false);
    }
  };
  
  return (
    
    <>

    <View>
      <HautPage title="Utilisateurs" />
    </View>

    <View style={styles.container}>

    <View>
      <Text style={styles.titre2}>Liste des utilisateurs de l'application</Text>
    </View>

      <View style={styles.hautBleu}>
        <Text style={styles.textTittre}>Nom</Text>
        <Text style={styles.textTittre}>Prénom</Text>
        <Text style={styles.textTittre}>Rôle</Text>
        <Text style={styles.textTittre}>info</Text>
      </View>

      

      <View style={styles.tableContainer}>
        <FlatList
          data={utilisateur}
          renderItem={renderItem}
          keyExtractor={(item) => item.id}
        />
      </View>

    </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center'
  },
  header: { 
    flexDirection: 'row', 
    backgroundColor: '#3498db', 
    padding: 8 
  },
  headerCell: { 
    flex: 1, 
    color: 'white', 
    fontWeight: 'bold' 
  },
  tableContainer: { 
    width: 345, 
    height: 365, 
    borderWidth: 1, 
    borderColor: '#ccc', 
    marginTop: 8 
  },
  row: { 
    justifyContent: 'center',
    flexDirection: 'row', 
    padding: 15, 
    borderBottomWidth: 1, 
    borderBottomColor: '#eee' 
  },
  cell: { 
    flex: 1 
  },
  cellImage: { 
    width: 25, 
    height: 25 
  },
  hautBleu:{
    borderTopLeftRadius: 15,
    borderTopRightRadius: 15,
    width: 350,
    height: 40,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    backgroundColor: '#1D3557',
  },
  textTittre:{
    color: '#ffffff',
    fontSize: 17,
  },
  titre2: {
    textAlign: 'center',
    color: '#1D3557',
    fontSize: 25,
    marginBottom: 30,
  }

});
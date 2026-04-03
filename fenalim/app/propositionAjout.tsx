import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, Alert, ScrollView } from 'react-native';
import { router } from 'expo-router';
import { getToken } from '@/service/infosStocker';
import {getAllPropositionMin } from '@/service/propoAjoutService';


const roue = require('@/assets/images/parametres.png');

// Donnée de proposition
type Proposition = {
  id: string;
  description: string;
  date: string;
};

// Affichage des proposition d'ajout de point d'eau
export default function PropositionAjout() {
  
  const [proposition, setProposition] = useState<Proposition[]>([]);
  const [chargement, setChargement] = useState(true);
  
  // récupérer le token 
  useEffect(() => {
    getData();
  }, []);

  const getData = async () => {
    try {
      const value = await getToken();
      if(value !== null) {
        fetchProposition(value);
      }
    } catch(e) {
      console.log("Erreur token affichage proposition d'ajout");
    }
  }

  const fetchProposition = async (token: string) => {
    if (!token) {
      alert("Impossible de recuperer les information");
      return;
    }
    else{
      console.log(token);
    }
    try {
      // apelle du fichier propoAjoutService pour recuperer tout les proposition via la requete
      const reponseProposition = await getAllPropositionMin(token);

      // affichage des données
      console.log("Données reçues:", reponseProposition);
      
      const propositionRaw = Array.isArray(reponseProposition) ? reponseProposition : reponseProposition.proposition;

      if (!propositionRaw) {
        console.error("Impossible de récupérer la proposition:", reponseProposition);
        return;
    }

    const lesProposition: Proposition[] = propositionRaw.map((u: any) => ({
      id: String(u.id),
      description: u.description,
      date: String(u.date_creation),
    }));
    setProposition(lesProposition);

    } catch (error) {
        console.error("Erreur lors du chargement des proposition d'ajout :", error);
        Alert.alert("Erreur", "Impossible de récupérer la proposition d'ajout.");
    } finally {
        setChargement(false);
    }
  };


  // affichage en tableau
  const renderItem = ({ item }: { item: Proposition }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.id}</Text>
      <Text style={styles.cell}> {item.description.length > 10 ? item.description.slice(0, 10) + ' ...' : item.description}</Text>
      <Text style={styles.cell}> {new Date(item.date).toLocaleDateString()}</Text>
      
      <TouchableOpacity onPress={() => router.push({ pathname: '/infoProposition', params: { id: item.id } })}>
        <Image source={roue} style={styles.cellImage} />
      </TouchableOpacity>
    </View>
  );
  
  return (
    <>    
    <View style={styles.container}>

      <View style={styles.hautBleu}>
        <Text style={styles.textTitre}>ID</Text>
        <Text style={styles.textTitre}>Description</Text>
        <Text style={styles.textTitre}>Date</Text>
        <Text style={styles.textTitre}>Info</Text>
      </View>
    
      <View style={styles.tableContainer}>
          <FlatList
          data={proposition}
          renderItem={renderItem}
          keyExtractor={(item, index) => `${item.id}-${index}`}
          scrollEnabled={true}
          />
      </View>
      
    </View>
    </>
  );
}

// Style
const styles = StyleSheet.create({
  contenue: {
    marginTop: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  container: { 
    flex: 1, 
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center'
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
    flex: 0.5 
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
  textTitre:{
    color: '#ffffff',
    fontSize: 17,
  },


});
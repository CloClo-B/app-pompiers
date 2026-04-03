import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, Alert } from 'react-native';
import { router } from 'expo-router';
import { getAllSignalement } from '@/service/signalementService';
import { getToken } from '@/service/infosStocker';


const roue = require('@/assets/images/parametres.png');

// Donnée du Signalement
type Signale = {
  id_s: string;
  id: string;
  probleme: string;
  date: string;
};

// Affichage des Signalement des points d'eau
export default function PointSignale() {
  
  const [signaler, setSignale] = useState<Signale[]>([]);
  const [chargement, setChargement] = useState(true);
  
  // récupérer le token 
  useEffect(() => {
    getData();
  }, []);
  const getData = async () => {
    try {
      const value = await getToken();
      if(value !== null) {
        fetchPointSignale(value);
      }
    } catch(e) {
      console.log("Erreur token affichage point eau signalé");
    }
  }

  const fetchPointSignale = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible de créer le point d'eau");
      return;
    }
    else{
      console.log(token);
    }
    try {
      // apelle du fichier signalementService pour recuperer tout les signalement via la requete
      const reponseSignalement = await getAllSignalement(token);

      // affichage des données
      console.log("Données reçues:", reponseSignalement);
      
      const signaleRaw = Array.isArray(reponseSignalement) ? reponseSignalement : reponseSignalement.signalement;

      if (!signaleRaw) {
        console.error("Impossible de récupérer les points signalés:", reponseSignalement);
        return;
    }

    const lesSignaler: Signale[] = signaleRaw.map((u: any) => ({
      id_s: String(u.id),
      id: String(u.id_point),
      probleme: u.probleme,
      date: String(u.date_creation),
    }));
    setSignale(lesSignaler);

    } catch (error) {
        console.error("Erreur lors du chargement des points signalés :", error);
        Alert.alert("Erreur", "Impossible de récupérer les points signalés.");
    } finally {
        setChargement(false);
    }
  };


  // affichage en tableau
  const renderItem = ({ item }: { item: Signale }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.id}</Text>
      <Text style={styles.cell}> {item.probleme.length > 10 ? item.probleme.slice(0, 10) + ' ...' : item.probleme}</Text>
      <Text style={styles.cell}> {new Date(item.date).toLocaleDateString()}</Text>
      <TouchableOpacity onPress={() => router.push({ pathname: '/infoSignalement', params: { id_s: item.id_s } })}>
        <Image source={roue} style={styles.cellImage} />
      </TouchableOpacity>
    </View>
  );
  
  return (
    <>    
    <View style={styles.container}>

      <View style={styles.hautBleu}>
        <Text style={styles.textTitre}>ID point</Text>
        <Text style={styles.textTitre}>Problème</Text>
        <Text style={styles.textTitre}>Date</Text>
        <Text style={styles.textTitre}>Info</Text>
      </View>


      <View style={styles.tableContainer}>
        <FlatList
          data={signaler}
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
  textTitre:{
    color: '#ffffff',
    fontSize: 17,
  },


});
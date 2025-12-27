import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, Alert } from 'react-native';
import { router, useRouter } from 'expo-router';
import axios from 'axios';

const roue = require('@/assets/images/parametres.png');


type Signale = {
  id_s: string;
  id: string;
  probleme: string;
  date: string;
};


export default function PointSignale() {
  
  const [signaler, setSignale] = useState<Signale[]>([]);
  const [chargement, setChargement] = useState(true);
  
  
  useEffect(() => {
    fetchPointSignale();
  }, []);

  const fetchPointSignale = async () => {
    try {
      const response = await axios.get("http://192.168.1.178:8000/signaler/");
      // affichage des données
      console.log("Données reçues:", response.data);
      
      const signaleRaw = Array.isArray(response.data) ? response.data : response.data.signalement;

      if (!signaleRaw) {
        console.error("Impossible de récupérer les points signaler:", response.data);
        setChargement(false);
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
        console.error("Erreur lors du chargement des points signaler :", error);
        Alert.alert("Erreur", "Impossible de récupérer les points signaler.");
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
        <Text style={styles.textTittre}>ID point</Text>
        <Text style={styles.textTittre}>Problème</Text>
        <Text style={styles.textTittre}>Date</Text>
        <Text style={styles.textTittre}>Info</Text>
      </View>


      <View style={styles.tableContainer}>
        <FlatList
          data={signaler}
          renderItem={renderItem}
          keyExtractor={(item, index) => `${item.id}-${index}`}
          scrollEnabled={false}
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
  imageDuProb: {
    width: 60, 
    height: 60,
    marginRight: 25

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
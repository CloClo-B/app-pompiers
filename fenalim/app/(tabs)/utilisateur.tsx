import React from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity } from 'react-native';
import HautPage from '../hautPage';
import { useRouter } from 'expo-router';

type User = {
  id: string;
  nom: string;
  localisation: string;
  probleme: string;
  image: string;
};

const data: User[] = [
  { id: '1', nom: 'Alice', localisation: 'Paris', probleme: 'Bug', image: 'https://via.placeholder.com/30' },
  { id: '2', nom: 'Bob', localisation: 'Lyon', probleme: 'Erreur', image: 'https://via.placeholder.com/30' },
  { id: '3', nom: 'Charlie', localisation: 'Marseille', probleme: 'Crash', image: 'https://via.placeholder.com/30' },
  { id: '4', nom: 'Alice', localisation: 'Paris', probleme: 'Bug', image: 'https://via.placeholder.com/30' },
  { id: '5', nom: 'Bob', localisation: 'Lyon', probleme: 'Erreur', image: 'https://via.placeholder.com/30' },
  { id: '6', nom: 'Charlie', localisation: 'Marseille', probleme: 'Crash', image: 'https://via.placeholder.com/30' },
  { id: '7', nom: 'Alice', localisation: 'Paris', probleme: 'Bug', image: 'https://via.placeholder.com/30' },
  { id: '8', nom: 'Bob', localisation: 'Lyon', probleme: 'Erreur', image: 'https://via.placeholder.com/30' },
  { id: '9', nom: 'Charlie', localisation: 'Marseille', probleme: 'Crash', image: 'https://via.placeholder.com/30' },
  { id: '10', nom: 'Alice', localisation: 'Paris', probleme: 'Bug', image: 'https://via.placeholder.com/30' },
  { id: '11', nom: 'Bob', localisation: 'Lyon', probleme: 'Erreur', image: 'https://via.placeholder.com/30' },
  { id: '12', nom: 'Charlie', localisation: 'Marseille', probleme: 'Crash', image: 'https://via.placeholder.com/30' },
];

export default function HomeScreen() {
  const renderItem = ({ item }: { item: User }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.nom}</Text>
      <Text style={styles.cell}>{item.localisation}</Text>
      <Text style={styles.cell}>{item.probleme}</Text>
      <Image source={{ uri: item.image }} style={styles.cellImage} />
    </View>
  );

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
        <Text style={styles.textTittre}>Localisation</Text>
        <Text style={styles.textTittre}>Problème</Text>
        <Text style={styles.textTittre}>Infos</Text>
      </View>
      
      {/*
      <TouchableOpacity
        onPress={() => router.push(`/user-details/${item.id}`)} // navigation vers la page détails
      >
        <Image
          source={require('@/assets/images/flamme1.png')}
          style={styles.cellImage}
        />
      </TouchableOpacity>
      */}

      <View style={styles.tableContainer}>
        <FlatList
          data={data}
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
    width: 30, 
    height: 30 
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
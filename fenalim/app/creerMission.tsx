import axios from 'axios';
import { router } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_ENDPOINTS } from '@/config/api';

// Page de création de Mission
export default function CreerMission() {

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
      }
    } catch(e) {
      console.log("erreur token creation point eau");
    }
  }

  // variable pour ensuite envoyer à l'api
  // text input
  const [nomMission, setnomMission] = useState(''); 
  const [IDPoint, setIDPoint] = useState(''); 
  const [commentaire, setCommentaire] = useState('');
  const [itineraire, setItineraire] = useState('');



  const creerMission = async () => {
    if (!token) {
      alert("Token manquant, impossible de créer la mission");
      return;
    }
    else{
      console.log(token);
    }
    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification des valeurs à envoyer\n");
    console.log("nomMission:", nomMission);
    console.log("IDPoint:", IDPoint);
    console.log("commentaire:", commentaire);
    console.log("itinéraire:", itineraire);
    if(nomMission == null || !nomMission.trim()){
      console.log("Erreur le nom de mission est incorrect");
      alert("Le nom de mission est incorect");
      return;
    }
    else if(IDPoint == null || !IDPoint.trim() || Number.isInteger(Number(IDPoint)) == false){
      console.log("Erreur l'ID du point incorrect");
      alert("L'ID du point est incorect");
      return;
    }
    else if(commentaire == null || !commentaire.trim() || commentaire.length>250){
      console.log("Erreur le détail de la mission est incorrect");
      alert("Le détail de la mission incorect");
      return;
    }
    else if(itineraire == null || !itineraire.trim()){
      console.log("Erreur l'adresse de la mission est incorrect");
      alert("L'adresse de la mission incorect");
      return;
    }
    else{
      try {
        const response = await axios.post(API_ENDPOINTS.MISSIONS, {
          nom_mission: nomMission,        
          id_point: parseInt(IDPoint),
          commentaire: commentaire, 
          itineraire: itineraire,
  
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
        
        router.push({
            pathname: '/succes',
            params: { title: 'Mission créé avec succès', page:"missions" }
          });
        }
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          // erreur renvoyée par l’API
          console.log(error.response?.status);
          console.log(error.response?.data);
          alert(error.response?.data?.detail ?? "Erreur lors de la création de la mission");
        } else {
          // autre erreur
          alert("Erreur lors de la création de la mission");
        }
      }
    }
  };




  return (
    <>  
    {/* nom mission */}
    <View style={styles.tout}>
      <Text style={styles.text}>Nom de la mission</Text> 
      <TextInput value={nomMission} onChangeText={setnomMission} style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* ID du point d'eau */}
    <View style={styles.tout}>
      <Text style={styles.text}>ID du point d'eau à utiliser</Text> 
      <TextInput value={IDPoint} onChangeText={setIDPoint} style={styles.entree} keyboardType='number-pad' placeholder=""></TextInput>
    </View> 


    {/* message mission */}
    <View style={styles.tout}>
      <Text style={styles.text}>Détails de la mission</Text>
          <TextInput value={commentaire} onChangeText={setCommentaire} style={styles.entreeD} maxLength={250} multiline={true} placeholder="Ecrivez ici"></TextInput>
    </View>

    {/* itinéraire */}
    <View style={styles.tout}>
      <Text style={styles.text}>Adresse de la mission</Text> 
      <TextInput value={itineraire} onChangeText={setItineraire} style={styles.entree} placeholder=""></TextInput>
    </View> 


    {/* creer */}
      <View style={styles.tout}>
        <TouchableOpacity style={[styles.boutton, {marginTop: 15, backgroundColor: '#457B9D', width: 200, height: 45}]} onPress = {creerMission}>
          <Text style={{color:'#ffffff'}}>CREER</Text>
        </TouchableOpacity>
    </View>

    </>
  );
}

// Style
const styles = StyleSheet.create({
  tout:{
    alignSelf: 'center',
    alignItems: "center",
    marginTop: 20,
  },

  text: {
    marginBottom: 5,
    color: '#1D3557',
    fontSize: 15,
    fontWeight: '600',
    alignSelf: 'center',
  },
  entree: {
    backgroundColor: '#ffffffff',
    width: 340,
    height: 50,
    paddingHorizontal: 10,
    borderRadius: 30,
    borderWidth: 1,
    borderColor: '#1D3557',
  },
  boutton:{
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
  },

  entreeD: {
    width: 300,
    height: 282,
    borderWidth: 1,
    borderColor: '#1D3557',
    backgroundColor: '#D4D4D4',
    paddingVertical:15,
    paddingHorizontal: 15,
    borderRadius: 20,
    textAlignVertical:"top",
  },
});
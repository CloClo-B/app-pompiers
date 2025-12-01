import axios from 'axios';
import { router } from 'expo-router';
import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { setNativeProps } from 'react-native-reanimated';

export default function CreerMission() {
   
  // variable pour ensuite envoyer à l'api
  // text input

  const [nomMission, setnomMission] = useState(''); 
  const [IDPoint, setIDPoint] = useState(''); 
  const [statut, setStatut] = useState('');
  const [commentaire, setCommentaire] = useState('');
  const [itineraire, setItineraire] = useState('');



  // communication avec l'api  /missions/
  // valentin : 172.20.10.2 | 192.168.1.184
  const creerMission = async () => {

    // Avant l'appel API, pour vérifier les valeurs
  console.log("Vérification des valeurs à envoyer\n");
  console.log("nomMission:", nomMission);
  console.log("IDPoint:", IDPoint);
  console.log("idUtilisateur temporaire", "1")
  console.log("statut:", statut);
  console.log("commentaire:", commentaire);
  console.log("itinéraire:", itineraire);

    try {
      const response = await axios.post('http://10.201.126.118:8000/missions/', {
        // nomMission: nomMission,     a ajouter dans la bdd
        
        id_point: parseInt(IDPoint),
        id_utilisateur : 1,  // a changer par la suite celui ci est un utilisateur créer sur ma bdd
        commentaire: commentaire, 
        itineraire: itineraire,

      });
      
      router.push({
          pathname: '/creationSucces',
          params: { title: 'Mission créé avec succès', creerMission: 'creerMission', chemainPage: '/point_eau' }
        });
      } catch (error) {
          console.error(error);
          alert('Erreur lors de la création de la mission');
    }
  };




  return (
    <>  
    {/* nom mission */}
    <View style={styles.tout}>
      <Text style={styles.text}>Nom de la mission a rajouter dans la bdd</Text> 
      <TextInput value={nomMission} onChangeText={setnomMission} style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* ID du point d'eau */}
    <View style={styles.tout}>
      <Text style={styles.text}>ID du point d'eau à utiliser</Text> 
      <TextInput value={IDPoint} onChangeText={setIDPoint} style={styles.entree} keyboardType='number-pad' placeholder=""></TextInput>
    </View> 

    {/* Statut */}
    <View style={styles.tout}>
      <Text style={styles.text}>Statuts de la mission</Text> 
      <TextInput value={statut} onChangeText={setStatut} style={styles.entree} placeholder=""></TextInput>
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
  menuD: {
    borderRadius: 30,
    width: '90%',
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

    // {/* afficher la carte */}
    //   <View style={styles.tout}>
    //     <Text style={styles.text}>Localisation incendie</Text> 
    //     <TouchableOpacity style={[styles.boutton, {backgroundColor: '#457B9D', width: 250, height: 45}]} onPress={() => console.log("afficher carte")}>
    //       <Text style={{color:'#ffffff'}}>AFFICHER SUR LA CARTE</Text>
    //     </TouchableOpacity>
    // </View>


    // {/* Choix du point d’eau */}
    //   <View style={styles.tout}>
    //     <Text style={styles.text}>Choix du point d’eau</Text> 
    //     <TouchableOpacity style={[styles.boutton, {backgroundColor: '#457B9D', width: 250, height: 45}]} onPress={() => console.log("afficher carte")}>
    //       <Text style={{color:'#ffffff'}}>AFFICHER SUR LA CARTE</Text>
    //     </TouchableOpacity>
    // </View>
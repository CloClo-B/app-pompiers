import axios from 'axios';
import { router } from 'expo-router';
import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';
import { setNativeProps } from 'react-native-reanimated';

export default function CreerMission() {
   
  // variable pour ensuite envoyer à l'api
  // liste déroulante
  const [valueStatut, setValueStatut] = useState(null);
  
  // text input
  const [nomMission, setnomMission] = useState(''); 
  const [IDPoint, setIDPoint] = useState(''); 
  const [commentaire, setCommentaire] = useState('');
  const [itineraire, setItineraire] = useState('');

  // liste pour les différents niveau de statuts
  const [openStatuts, setOpenStatuts] = useState(false);
  const [etatStatuts, setItemsSatatus] = useState ([ 
    { label : 'En attente' , value : 'EN ATTENTE'}, 
    { label : 'En cours' , value : 'EN COURS' }, 
    { label : 'Terminer' , value : 'TERMINER' }, 
  ]);

  // méthode de vérification
  const verifTypeStatut = (type: string) => {
    const typeValides = ['EN ATTENTE', 'EN COURS', 'TERMINER'];
    return typeValides.includes(type);
  }

  const creerMission = async () => {

    // Avant l'appel API, pour vérifier les valeurs
  console.log("Vérification des valeurs à envoyer\n");
  console.log("nomMission:", nomMission);
  console.log("IDPoint:", IDPoint);
  console.log("idUtilisateur temporaire", "1")
  console.log("statut:", valueStatut);
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
    else if(valueStatut == null || verifTypeStatut(valueStatut) == false){
      console.log("Erreur le statut de la mission incorrect");
      alert("Le statut de la mission est incorect");
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
        const response = await axios.post('http://192.168.1.178:8000/missions/', {
          nom_mission: nomMission,        
          id_point: parseInt(IDPoint),
          statut: valueStatut,
          id_utilisateur : 1,  // a changer par la suite celui ci est un utilisateur créer sur ma bdd
          commentaire: commentaire, 
          itineraire: itineraire,
  
        });
        
        router.push({
            pathname: '/creationSucces',
            params: { title: 'Mission créé avec succès', creerMission: 'creerMission', chemainPage: '/point_eau' }
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


    {/* statut */}
    <View style={[styles.tout, {zIndex: 100, marginTop:20}]}>
      <Text style={styles.text}>Statut du point d’eau</Text> 
      <DropDownPicker 
        open={openStatuts} 
        value={valueStatut} 
        items={etatStatuts} 
        setOpen={setOpenStatuts} 
        setValue={setValueStatut} 
        setItems={setItemsSatatus}
        placeholder="Sélectionnez le statut de la mission" 
        listMode= "SCROLLVIEW"
        style={styles.menuD}
      /> 
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
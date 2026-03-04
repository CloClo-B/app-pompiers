import axios from 'axios';
import { router } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { CreateMission } from '@/service/MissionService';
import { getToken } from '@/service/infosStocker';
import { useLocalSearchParams } from 'expo-router';
import ButtonLog from '@/components/ButtonLog';

// Page de création de Mission depuis la carte
export default function CreerMission() {
  const { idPoint } = useLocalSearchParams<{ idPoint: string }>();
  const [token, setToken] = useState<string | null>(null);

  // récupérer le token et l'id du point
  useEffect(() => {
    if (idPoint) {
      setIDPoint(idPoint);
      getData();
    }
  }, [idPoint]);



  const getData = async () => {
    try {
      const value = await getToken();
      if(value !== null) {
        setToken(value);
      }
    } catch(e) {
      console.log("erreur token creation point eau");
    }
  }

  // variable pour ensuite envoyer à l'api
  // text input
  const [IDPoint, setIDPoint] = useState(''); 
  const [nomMission, setnomMission] = useState(''); 
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

        // apelle du fichier MissionService pour la envoyer la requete de creation mission 
        const response = await CreateMission(token, nomMission, IDPoint, commentaire, itineraire);

        
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

    <View style={styles.tout}>
      {/* hydrant selectionner */}
      <Text style={styles.choixhydrant}> Hydrant #{IDPoint}</Text>
    
      {/* nom mission */}
      <Text style={styles.text}>Nom de la mission</Text> 
      <TextInput value={nomMission} onChangeText={setnomMission} style={styles.entree} placeholder=""></TextInput>


      {/* message mission */}
      <Text style={styles.text}>Détails de la mission</Text>
      <TextInput value={commentaire} onChangeText={setCommentaire} style={styles.entreeD} maxLength={250} multiline={true} placeholder="Ecrivez ici"></TextInput>

      {/* itinéraire */}
      <Text style={styles.text}>Adresse de la mission</Text> 
      <TextInput value={itineraire} onChangeText={setItineraire} style={styles.entree} placeholder=""></TextInput>


      {/* creer */}
      <ButtonLog label="CREER" onPress={creerMission} type="primary" width={200} height={45} marginTop={35}/>
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

  choixhydrant: {
    marginBottom: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    backgroundColor:'#c8cac8ff',
    borderRadius: 40,
    fontSize: 20,
  },
});
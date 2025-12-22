import { Camera } from 'expo-camera';
import { Alert, Image, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import axios from 'axios';
import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
import { useState } from 'react';
import HautPage from './hautPage';

// petit encadrer pour choix photo
const ajouterPhoto = require('@/assets/images/ajouter_photo.png');




export default function Signalement() {
  const router = useRouter();
  
  // variable pour ensuite envoyer à l'api
  
  const [IDPoint, setIDPoint] = useState(''); 
  const [probleme, setProbleme] = useState('');
  const [photo, setPhoto] = useState('');

//  ouvrir la galerie
  const [image, setImage] = useState<string | null>(null);
  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    console.log(result);

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };


// ouvrir la caméra
const prendrePhoto = async () => {
  const { status } = await Camera.requestCameraPermissionsAsync();
  if (status === "granted") {
    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });
    if (!result.canceled) setImage(result.assets[0].uri);
  } else {
    Alert.alert("Autorisation refusée", "Vous devez autoriser l'accès à la caméra.");
  }
};


// choisir entre camera ou galerie
const handlePickImage = () => {
        Alert.alert(
        "Ajouter une image",
        "",
        [
            {
            text: "Galerie", onPress: async () => {pickImage()} },
            {
            text: "Caméra", onPress: async () => {prendrePhoto()},
            },
            {
            text: "Annuler",
            style: "cancel",
            },
        ]
        );
    };

  // communication avec l'api  /missions/
  const creerSignalement = async () => {

    // Avant l'appel API, pour vérifier les valeurs
  console.log("Vérification des valeurs à envoyer\n");
  console.log("IDPoint:", IDPoint);
  console.log("probleme:", probleme);
  console.log("photo", photo);


  if(probleme == null || !probleme.trim() || probleme.trim().length<10 || probleme.trim().length> 100){
    console.log("Erreur le nom est incorrect");
    alert("La description du probleème est incorrect minimum 10 caractère maximum 100");
  }
      else if(image == null){
        console.log("Erreur pas d'image");
        alert("Image requise");
      }
      else{        
        try {
          const formData = new FormData();
          formData.append("id_point", "444");
          formData.append("probleme", probleme);
          formData.append("photo", {
            uri: image,
            name: "pointsignaler.jpg",
            type: "image/jpeg",
          } as any);
          formData.append("id_utilisateur", "1");
          
          const response = await axios.post("http://192.168.1.178:8000/signaler/", formData, {
            headers: { "Content-Type": "multipart/form-data" }
          });
          router.push({
              pathname: '/creationSucces',
              params: { title: 'Signalement créé avec succès', creerMission: 'creerMission', chemainPage: '/point_eau' }
            });
          } 
          catch (error) {
            console.error(error);
            alert('Erreur lors de la création du signalement');
          }
      }
  };




  return (
    <>
    <View>
      <HautPage title="Signalement hydrant" />
    </View>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
      >

      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
    
        <View style={styles.info}>

            {/* hydrant selectionner */}
            <Text style= {styles.choixhydrant} >Hydrant #235</Text>


            {/* message signalement */}
            <View style={styles.total}>
              <Text style={styles.text}>Descripton du problème</Text>
              <View style={styles.entreeCryon}>
                  <TextInput value={probleme} onChangeText={setProbleme} style={styles.entree} maxLength={100} multiline={true} placeholder="Ecrivez ici"></TextInput>
              </View>
            </View>

            {/* ajout de l'image */}
            <TouchableOpacity onPress={handlePickImage}>
            <Image source={ajouterPhoto}/>
            {image && <Image source={{ uri: image }} style={styles.image} />}
            </TouchableOpacity>


            {/* choix validation annulation */}
            <View style={styles.validation}>

                <TouchableOpacity style={styles.boutton} onPress={() => router.navigate('/(tabs)/acceuil')}>
                <Text style={{color:'#ffffff'}}>ANNULER</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.boutton} onPress={creerSignalement}>
                <Text style={{color:'#ffffff'}}>CONFIRMER</Text>
                </TouchableOpacity>

            </View>

        </View>
        
      </ScrollView>
    </KeyboardAvoidingView>

    </>
  );
}

const styles = StyleSheet.create({

  image: {
    alignSelf:'center',
    width: 200,
    height: 200,
  },
  contenue: {
    marginTop: 40,
    
    alignItems: 'center',
    justifyContent: 'center',
  },
  entreeCryon: {
    flexDirection: 'row',     
    alignItems: 'center',
    width: '100%',
  },

  validation:{
    flexDirection: 'row',
    marginTop: 40,
    alignItems: 'center',
    gap:'10%',    
  },


  total:{
    backgroundColor:'#ffffff',
    width: '90%',
    padding: 20,
    borderRadius: 20,
    marginBottom: 20,
  },

  boutton:{
    paddingVertical: 15,
    paddingHorizontal:25,
    backgroundColor: '#457B9D',
    borderRadius: 30,
    alignSelf: 'center',
  },

  info: {
    alignItems: 'center',
    width: '100%', 
  },
  
  text: {
    marginBottom: 10,
    fontWeight: '700',
    fontSize: 23,
    textAlign: 'center', 
    paddingLeft: 10,

  },
  entree: {
    flex: 1,
    backgroundColor: '#D4D4D4',
    height: 282,
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

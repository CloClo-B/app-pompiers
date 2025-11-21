import { Camera } from 'expo-camera';
import { Alert, Image, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
import { useState } from 'react';
import HautPage from '../hautPage';

const ajouterPhoto = require('@/assets/images/ajouter_photo.png');




export default function Compte() {
  const router = useRouter();

 
//  ouvrir la galerie
  const [image, setImage] = useState<string | null>(null);
  const pickImage = async () => {
    // No permissions request is necessary for launching the image library
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
                <TextInput style={styles.entree} maxLength={250} multiline={true} placeholder="Ecrivez ici"></TextInput>
                <TouchableOpacity  onPress={() => console.log('Bouton pressé')}>
                </TouchableOpacity>
            </View>
            </View>

            {/* ajout de l'image */}
            <TouchableOpacity onPress={handlePickImage}>
            <Image source={ajouterPhoto}/>
            {image && <Image source={{ uri: image }} style={styles.image} />}
            </TouchableOpacity>


            {/* choix validation annulation */}
            <View style={styles.validation}>

                <TouchableOpacity style={styles.boutton} onPress={() => console.log("annuler")}>
                <Text style={{color:'#ffffff'}}>ANNULER</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.boutton} onPress={() => console.log("confirmer")}>
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

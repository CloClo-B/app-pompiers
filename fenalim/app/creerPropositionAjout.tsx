import { Camera } from 'expo-camera';
import { Alert, Image, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import axios from 'axios';
import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import HautPage from './hautPage';
import { naviguerAccueil} from '@/config/navigation';
import { useLocalSearchParams } from 'expo-router';
import { createProposition } from '@/service/propoAjoutService';
import { getRole, getToken } from '@/service/infosStocker';
import ButtonLog from '@/components/ButtonLog';


// petit encadrer pour choix photo
const ajouterPhoto = require('@/assets/images/ajouter_photo.png');

// Page pour créer une proposition d'ajout de points d'eau
export default function creerPropositionAjout() {
  const router = useRouter();

  //recup les infos stocké 
  const { latitude, longitude } = useLocalSearchParams<{ latitude: string; longitude: string }>();
  
  
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);
  const [image, setImage] = useState<string | null>(null);

    useEffect(() => {
    getData();
    }, []);


  const getData = async () => {
    try {
      // recup role et token
      const token = await getToken();
      const role = await getRole();
      if(token !== null && role !== null) {
        setToken(token);
        setRole(role);
      }
    } catch(e) {
      console.log("erreur créer proposition ajout");
    }
  }



  // variable pour ensuite envoyer à l'api

  const [description, setDescription] = useState('');

  //  ouvrir la galerie
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

  // communication avec l'api  /propositionAjout/
  const creerProposition = async () => {

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification des valeurs à envoyer\n");
    console.log("description:", description);
    console.log("lattitude:", latitude);
    console.log("longitude:", longitude);
    console.log("photo", image);


    if (!latitude || !longitude){
      console.log("Erreur coordonnée");
      alert("Erreur coordonnée");
      return;
    }
    
    else if(description == null || !description.trim() || description.trim().length<50 || description.trim().length> 255){
      console.log("Erreur le nom est incorrect");
      alert("La description du problème est incorrect minimum 50 caractère maximum 255");
      return;
    }
    else if(image == null){
      console.log("Erreur pas d'image");
      alert("Image requise");
      return;
    }
    else if(token == null){
      console.log("Pas de token");
      alert("Erreur création proposition");
      return;
    }
    else{        
      try {
        const formData = new FormData();
        formData.append("description", description);
        formData.append("latitude", latitude);
        formData.append("longitude", longitude);
        formData.append("photo", {
          uri: image,
          name: "imageProposition.jpg",
          type: "image/jpeg",
        } as any);
        
        // apelle du fichier signalementService pour la envoyer la requete
        await createProposition(token, formData);

        router.push({
            pathname: '/succes',
            params: { title: 'Proposition créé avec succès',  page:"acceuil"  }
          });
      } 
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          // erreur renvoyée par l’API
          console.log(error.response?.status);
          console.log(error.response?.data);
          alert(error.response?.data?.detail ?? "Erreur lors du création de proposition");
        } else {
          // autre erreur
          alert("Erreur lors du création de proposition");
        }
      }
    }
  };


  return (
    <>
    <View>
      <HautPage title="Proposition point d'eau"/>
    </View>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
      >

      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
    
        <View style={styles.info}>
            
            <Text style={styles.text}>La localisation du point se fait directement à partir de votre position</Text>

            {/* message proposition */}
            <View style={styles.total}>
              <Text style={styles.text}>Décrivez le plus précisément possible les informations du point d'eau</Text>
              <View style={styles.entreeCryon}>
                  <TextInput value={description} onChangeText={setDescription} style={styles.entree} maxLength={255} multiline={true} placeholder="Explication des informations"></TextInput>
              </View>
            </View>

            {/* ajout de l'image */}
            <TouchableOpacity onPress={handlePickImage}>
            <Image source={ajouterPhoto}/>
            {image && <Image source={{ uri: image }} style={styles.image} />}
            </TouchableOpacity>


            {/* choix validation annulation */}
            <View style={styles.validation}>
                <ButtonLog label="ANNULER" onPress={() => { if (role) naviguerAccueil(role); else alert("Rôle utilisateur introuvable"); }} type="primary" width={150} height={45} />
                <ButtonLog label="CONFIRMER" onPress={creerProposition} type="primary" width={150} height={45}/>
            </View>

        </View>
        
      </ScrollView>
    </KeyboardAvoidingView>

    </>
  );
}

// Style
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



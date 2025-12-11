import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import { ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

import Button from '@/components/ButtonLog';
import axios from 'axios';
import { useState } from 'react';

export default function Connexion() {
  
  // variable pour ensuite envoyer à l'api
  // text input
  const [nom, setNom] = useState(''); 
  const [prenom, setPrenom] = useState(''); 
  const [email, setEmail] = useState('');
  const [telephone, setTelephone] = useState('');
  const [motDePasse, setMDP] = useState('');
  const [ConfirmmotDePasse, setConfirmMDP] = useState('');



  // communication avec l'api  /utilisateurs/
  // valentin : 172.20.10.2 | 192.168.1.184
  const creerUtilisateur = async () => {

    // Avant l'appel API, pour vérifier les valeurs
  console.log("Vérification des valeurs à envoyer\n");
  console.log("nom: ", nom);
  console.log("prenom: ", prenom);
  console.log("email: ", email);
  console.log("téléphone: ", telephone);
  console.log("mdp: ", motDePasse);
  console.log("confirme mdp: ", motDePasse);


    try {
      const response = await axios.post('http://172.20.10.2:8000/utilisateurs/', {
        nom: nom,        
        prenom: prenom,
        telephone : telephone,
        email: email, 
        mot_de_passe: motDePasse,
        confirm_password: ConfirmmotDePasse, 


      });
      
      router.navigate('/(tabs)/acceuil')
      } catch (error) {
          console.error(error);
          alert("Erreur lors de la création de l'utilisateur");
    }
  };



  const router = useRouter();
  return (
    <ScrollView>
        <LinearGradient colors={['#E63946', '#1D3557']} style={styles.container}>

                <View>
                    <Text style={[styles.title,{marginTop: 30}]}>Créer mon compte</Text>
                </View>

                <View style={styles.aligne}>
                  <Text style={styles.title_ID_MDP}>Nom</Text>
                  <TextInput value={nom} onChangeText={setNom} style={styles.saisiChamp}/>
                </View>

                <View style={styles.aligne}>
                  <Text style={styles.title_ID_MDP}>Prénom</Text>
                  <TextInput value={prenom} onChangeText={setPrenom} style={styles.saisiChamp}/>
                </View>

                <View style={styles.aligne}>
                  <Text style={styles.title_ID_MDP}>Numéro de téléphone</Text>
                  <TextInput value={telephone} onChangeText={setTelephone} style={styles.saisiChamp}/>
                </View>

                <View style={styles.aligne}>
                  <Text style={styles.title_ID_MDP}>Email</Text>
                  <TextInput value={email} onChangeText={setEmail} style={styles.saisiChamp}/>
                </View>

                <View style={styles.aligne}>
                  <Text style={styles.title_ID_MDP}>Mot de passe</Text>
                  <TextInput value={motDePasse} onChangeText={setMDP} style={styles.saisiChamp}/>
                </View>

                <View style={styles.aligne}>
                    <Text style={styles.title_ID_MDP}>Confirmer le mot de passe</Text>
                   <TextInput value={ConfirmmotDePasse} onChangeText={setConfirmMDP} style={styles.saisiChamp}/>
                </View>

                <View style={{ marginTop: 50}}>
                    <Button label='Valider' onPress={creerUtilisateur} backColor="#30D936"/>
                </View>

                <View>
                    <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Connexion' onPress={() => router.navigate('/connexion')}/>
                </View>
                
        </LinearGradient>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 40,
  },
  title: {
    color: '#fff',
    fontSize: 40,
    fontWeight: 'bold',
    marginBottom: 70,
  },
  title_ID_MDP: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    alignSelf: 'flex-start',
  },
  aligne: {
    width: '80%', 
    maxWidth: 300, 
    alignSelf: 'center', 
    marginTop: 20,
  },
  saisiChamp: {
    width: '100%',
    height: 40, 
    color: '#000000ff',
    backgroundColor: '#fff',
    borderRadius: 10,
    paddingHorizontal: 10,
  }
});

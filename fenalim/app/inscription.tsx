import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import { KeyboardAvoidingView,Platform, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

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

  const verifEmail = (email: string) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email.trim());
  }

  const creerUtilisateur = async () => {

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification des valeurs à envoyer\n");
    console.log("nom: ", nom);
    console.log("prenom: ", prenom);
    console.log("email: ", email);
    console.log("téléphone: ", telephone);
    console.log("mdp: ", motDePasse);
    console.log("confirme mdp: ", ConfirmmotDePasse);


    // vérfication des valeurs correct avant envoyer à l'api + affichage message de l'erreur
    if(nom == null || !nom.trim()){
      console.log("Erreur le nom est incorrect");
      alert("Le nom est incorrect");
      return;
    }
    else if(prenom == null || !prenom.trim()){
      console.log("Erreur le prénom est incorrect");
      alert("Le prénom est incorrect");
      return;
    }
    else if(email == null || !email.trim() || !verifEmail(email)){
      console.log("Erreur le mail est incorrect");
      alert("Le mail est incorrect");
      return;
    }
    else if(!/^\d{10}$/.test(telephone) || !telephone.trim()){
      console.log("Erreur le numéro de téléphone est incorrect");
      alert("Le numéro de téléphone est incorrect");
      return;
    }
    else if(motDePasse.length < 12 || !motDePasse.trim()){
      console.log("Erreur a longeur du mot de passe est incorect il faut minimum 12 caracères");
      alert("La longeur du mot de passe est incorect il faut minimum 12 caracères");
      return;
    }
    else if(motDePasse.trim() != ConfirmmotDePasse.trim() ){
      console.log("Erreur les mots de passe sont différents");
      alert("Les mots de passe sont différents");
      return;
    }
    else{
      try {
        const response = await axios.post('http://192.168.1.178:8000/utilisateurs/', {
          nom: nom,        
          prenom: prenom,
          telephone : telephone,
          email: email, 
          mot_de_passe: motDePasse,
          confirm_password: ConfirmmotDePasse, 
        });
        
        router.navigate('/(tabs)/acceuil')
        } 
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          // erreur renvoyée par l’API
          console.log(error.response?.status);
          console.log(error.response?.data);
          alert(error.response?.data?.detail ?? "Erreur lors de l'inscription");
        } else {
          // autre erreur
          alert("Erreur lors de l'inscription");
        }
      }
    };
  }




  const router = useRouter();
  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
    >

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
                    <TextInput keyboardType='phone-pad' value={telephone} onChangeText={setTelephone} style={styles.saisiChamp}/>
                  </View>

                  <View style={styles.aligne}>
                    <Text style={styles.title_ID_MDP}>Email</Text>
                    <TextInput keyboardType='email-address' value={email} onChangeText={setEmail} style={styles.saisiChamp}/>
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
    </KeyboardAvoidingView>

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

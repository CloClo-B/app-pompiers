import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';

import { ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

import Button from '@/components/ButtonLog';
import { useState } from 'react';
import axios from 'axios';

export default function Connexion() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [motDePasse, setMDP] = useState('');

  const verifEmail = (email: string) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email.trim());
  }
  const verifUtilisateurExiste = async () => {

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification des valeurs à envoyer\n");
    console.log("email: ", email);
    console.log("mdp: ", motDePasse);


    // vérfication des valeurs correct avant envoyer à l'api + affichage message de l'erreur
    if(email == null || !email.trim() || !verifEmail(email)){
      console.log("Erreur le mail est incorrect");
      alert("Le mail est incorrect");
      return;
    }
    else if(motDePasse == null || !motDePasse.trim()){
      console.log("Erreur le mot de passe n'est pas remplie");
      alert("Le champ mot de passe n'est pas completer");
      return;
    }

    else{
      try {
        const response = await axios.post('http://192.168.1.178:8000/utilisateurs/login', {
          email: email,        
          mot_de_passe: motDePasse,
        });
        
        router.navigate('/(tabs)/acceuil')
        }
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          // erreur renvoyée par l’API
          console.log(error.response?.status);
          console.log(error.response?.data);
          alert(error.response?.data?.detail ?? "Erreur lors de la connexion");
        } else {
          // autre erreur
          alert("Erreur lors de la connexion");
        }
      }
    };
  }

  return (
    <ScrollView>
        <LinearGradient colors={['#E63946', '#1D3557']} style={styles.container}>

                <View>
                    <Text style={[styles.title,{marginTop: 30}]}>Connexion</Text>
                </View>

                <View style={styles.aligne}>
                  <Text style={styles.title_ID_MDP}>E-mail</Text>
                  <TextInput keyboardType='email-address' value={email} onChangeText={setEmail} style={styles.saisiChamp}/>
                </View>

                <View style={styles.aligne}>
                    <Text style={styles.title_ID_MDP}>Mot de passe</Text>
                  <TextInput value={motDePasse} secureTextEntry onChangeText={setMDP} style={styles.saisiChamp}/>
                </View>

                <View style={{ marginTop: 50}}>
                    <Button label='Connexion' onPress={verifUtilisateurExiste} backColor="#30D936"/>
                </View>

                <View>
                    <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Mot de passe oublié' onPress={() => {console.log('en cours')}}/>
                    <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Créer un compte' onPress={() => router.navigate('/inscription')}/>
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

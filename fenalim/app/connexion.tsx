import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';

import { ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View, Image, KeyboardAvoidingView, Platform } from 'react-native';

import { useState } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';
import { setRole, setToken } from '@/service/infosStocker';
import ButtonLog, { BoutonConnexion } from '@/components/ButtonLog';


const Oeil = require('@/assets/images/oeil.png');
const OeilCache = require('@/assets/images/oeil_cacher.png');

// Gère la connexion des utilisateurs
export default function Connexion() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [motDePasse, setMDP] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [attenteChargement, setLoading] = useState(false);

  // Vérif adresse mail
  const verifEmail = (email: string) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email.trim());
  }
  const verifUtilisateurExiste = async () => {

    if (attenteChargement) return;
    

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification des valeurs à envoyer\n");
    console.log("email: ", email);
    console.log("mdp: ", motDePasse);


    // vérfication des valeurs correct avant envoyer à l'api + affichage message de l'erreur
    if(email == null || !email.trim() || !verifEmail(email)){
      console.log("Erreur le mail est incorrect");
      alert("Le champ mail est incorrect ou non complété");
      return;
    }
    else if(motDePasse == null || !motDePasse.trim()){
      console.log("Erreur le mot de passe n'est pas rempli");
      alert("Le champ mot de passe est incorrect ou non complété");
      return;
    }

    setLoading(true);

      try {
        const response = await axios.post(API_ENDPOINTS.LOGIN, {
          email: email,        
          mot_de_passe: motDePasse,
        });

        // recupération du token utilisateur
        console.log("Token du compte", email, ":", response.data.token);

        const role = response.data.role;  //recuperation du role de l'utilisateur
        console.log(role);

        // stockage du token et du role
        setToken(response.data.token)
        setRole(response.data.role)

        // affichage en fonction du role
        if (role === 'public') {
          router.replace('/(tabs_public)/acceuil');
        } else if (role === 'pompier') {
          router.replace('/(tabs_pompier)/acceuil_pompier');
        } else if (role === 'commandement') {
          router.replace('/(tabs_commandement)/acceuil_commandement');
        } else if (role === 'admin') {
          router.replace('/(tabs_admin)/acceuil_admin');
        }

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
      } finally {
        setLoading(false);
      }
      
  }

  return (
    <KeyboardAvoidingView
            style={{ flex: 1 }}
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}>

      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
          <LinearGradient colors={['#E63946', '#1D3557']} style={styles.container}>

                  <View>
                      <Text style={[styles.title,{marginTop: 30}]}>Connexion</Text>
                  </View>

                  {/* Champ E-mail */}
                  <View style={styles.aligne}>
                    <Text style={styles.title_ID_MDP}>E-mail</Text>
                    <TextInput keyboardType='email-address' value={email} onChangeText={setEmail} style={styles.saisiChamp}/>
                  </View>

                  {/* Champ Mot de passe */}
                  <View style={styles.aligne}>
                      <Text style={styles.title_ID_MDP}>Mot de passe</Text>
                      <View style={styles.entreeCrayon}>          
                        <TextInput value={motDePasse} secureTextEntry={!showPassword} onChangeText={setMDP} style={styles.saisiChampMDP}/>
                        <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
                          <Image source={showPassword ? Oeil : OeilCache} style={styles.imageC} />
                        </TouchableOpacity>
                    </View>
                  </View>

                  {/* Bouton de validation */}
                  <View style={{ marginTop: 50}}>
                      <ButtonLog label='Connexion' onPress={verifUtilisateurExiste} backColor="#30D936" disabled={attenteChargement} loading={attenteChargement}/>
                  </View>
                  
                  {/* Liens vers Mot de passe oublié / Inscription */}
                  <BoutonConnexion/>
                  
          </LinearGradient>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

// Style
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
  },
  imageC: {
    width: 30,
    height: 30,
    marginLeft: 8,
  },
  entreeCrayon: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  saisiChampMDP: {
    flex: 1,
    height: 40,
    color: '#000000ff',
    backgroundColor: '#fff',
    borderRadius: 10,
    paddingHorizontal: 10,
  }
});
function asetRole(role: any) {
  throw new Error('Function not implemented.');
}


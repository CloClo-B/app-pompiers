import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import { KeyboardAvoidingView,Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View, Image } from 'react-native';

import axios from 'axios';
import { useState } from 'react';
import { API_ENDPOINTS } from '@/config/api';
import { setRole, setToken } from '@/service/infosStocker';
import ButtonLog, { BoutonConnexion } from '@/components/ButtonLog';

import TurnstileCaptcha from '@/components/TurnstileCaptcha';
import { ValidationCaptcha } from '@/service/captchaService';

const Oeil = require('@/assets/images/oeil.png');
const OeilCache = require('@/assets/images/oeil_cacher.png');

// Gère l'inscription des nouveaux utilisateurs
export default function Inscription() {

  // captcha
  const [captchaToken, setCaptchaToken] = useState<string | null>(null);


  // variable pour ensuite envoyer à l'api
  // text input
  const [nom, setNom] = useState(''); 
  const [prenom, setPrenom] = useState(''); 
  const [email, setEmail] = useState('');
  const [telephone, setTelephone] = useState('');
  const [motDePasse, setMDP] = useState('');
  const [confirmmotDePasse, setConfirmMDP] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmePassword, setshowConfirmePassword] = useState(false);
  const [attenteChargement, setLoading] = useState(false);

  const verifEmail = (email: string) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email.trim());
  }

  const creerUtilisateur = async () => {
    
    if (attenteChargement) return;

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification des valeurs à envoyer\n");
    console.log("nom: ", nom);
    console.log("prenom: ", prenom);
    console.log("email: ", email);
    console.log("téléphone: ", telephone);
    console.log("mdp: ", motDePasse);
    console.log("confirme mdp: ", confirmmotDePasse);


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
    else if(motDePasse.trim() != confirmmotDePasse.trim() ){
      console.log("Erreur les mots de passe sont différents");
      alert("Les mots de passe sont différents");
      return;
    }
    

    // verification du captcha
    if (!captchaToken) {
      alert("Veuillez valider le captcha");
      return;
    }
    try {
      const validation = await ValidationCaptcha(captchaToken);
      if (validation.status !== "success") {
      alert("Captcha invalide, veuillez réessayer");
      return;
      }
    } catch (err) {
      alert("Erreur lors de la validation du captcha");
      return;
    }
      
      
      // si captcah ok alors créer utilisateur
      setLoading(true);
      try {
        const response = await axios.post(API_ENDPOINTS.REGISTER, {
          nom: nom,        
          prenom: prenom,
          telephone : telephone,
          email: email, 
          mot_de_passe: motDePasse,
          confirm_password: confirmmotDePasse, 
        });
        // recup token
        console.log("Token du compte", email, ":", response.data.token);
        const role = response.data.role;  //recuperation du role 
        console.log(role);
        
        // stockage du token et du role
        setToken(response.data.token)
        setRole(response.data.role)

        // affichage en focntion du role
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
          alert(error.response?.data?.detail ?? "Erreur lors de l'inscription");
        } else {
          // autre erreur
          alert("Erreur lors de l'inscription");
        }
        
      } finally {
        setLoading(false);
      }
  }




  const router = useRouter();
  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
    >
      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
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
                    <View style={styles.entreeCrayon}>
                      <TextInput
                        value={motDePasse}
                        secureTextEntry={!showPassword} 
                        onChangeText={setMDP}
                        placeholder="Minimum 12 caractères"
                        style={styles.saisiChampMDP}
                      />
                      <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
                        <Image source={showPassword ? Oeil : OeilCache} style={styles.imageC} />
                      </TouchableOpacity>
                    </View>
                  </View>

                  <View style={styles.aligne}>
                    <Text style={styles.title_ID_MDP}>Confirmer le mot de passe</Text>
                    <View style={styles.entreeCrayon}>
                      <TextInput
                        value={confirmmotDePasse}
                        secureTextEntry={!showConfirmePassword}
                        onChangeText={setConfirmMDP}
                        placeholder="Minimum 12 caractères"
                        style={styles.saisiChampMDP}
                      />
                      <TouchableOpacity onPress={() => setshowConfirmePassword(!showConfirmePassword)}>
                        <Image source={showConfirmePassword ? Oeil : OeilCache} style={styles.imageC} />
                      </TouchableOpacity>
                    </View>
                  </View>

                  <TurnstileCaptcha onVerify={setCaptchaToken} />
                  
                  <View style={{ marginTop: 50}}>
                      <ButtonLog label='Valider' onPress={creerUtilisateur} backColor="#30D936" disabled={attenteChargement} loading={attenteChargement}/>
                  </View>

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
    fontSize: 35,
    fontWeight: 'bold',
    marginBottom: 50,
  },
  title_ID_MDP: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    alignSelf: 'flex-start',
  },
  aligne: {
    width: '100%', 
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


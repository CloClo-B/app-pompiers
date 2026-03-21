import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';
import { ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View, Image, KeyboardAvoidingView, Platform } from 'react-native';
import { useState } from 'react';
import axios from 'axios';
//import { API_ENDPOINTS } from '@/config/api';
import ButtonLog, { BoutonConnexion } from '@/components/ButtonLog';

const Oeil = require('@/assets/images/oeil.png');
const OeilCache = require('@/assets/images/oeil_cacher.png');

export default function MdpOublie() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [motDePasse, setMDP] = useState('');
  const [confirmMotDePasse, setConfirmMDP] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [attenteChargement, setLoading] = useState(false);
  const [codeEnvoye, setCodeEnvoye] = useState(false);

  const valider = async () => {
    if (attenteChargement) return;
    if (!email.trim()) { alert("Email incorrect"); return; }
    if (!code.trim()) { alert("Code incorrect"); return; }
    if (motDePasse.length < 12) { alert("Minimum 12 caractères"); return; }
    if (motDePasse !== confirmMotDePasse) { alert("Les mots de passe sont différents"); return; }

    setLoading(true);
    try {
      //Lorsque le système de reset pour le mot de passe sera implémenté, enlevé le code commenté 
      //await axios.post(`${API_ENDPOINTS.RESET_PASSWORD}?token=${code}&nouveau_mot_de_passe=${motDePasse}`);
      //alert("Mot de passe modifié");
      //router.replace('/connexion');
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        alert(error.response?.data?.detail ?? "Erreur");
      } else {
        alert("Erreur");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
        <LinearGradient colors={['#E63946', '#1D3557']} style={styles.container}>

          <View>
            <Text style={[styles.title, { marginTop: 30 }]}>Mot de passe oublié</Text>
          </View>

          {/* Envoie du code de sécurité par le mail renseigné*/}
          <View style={styles.aligne}>
            <Text style={styles.title_ID_MDP}>Renseignez votre e-mail pour l'envoi d'un code de sécurité</Text>
            <TextInput keyboardType='email-address' value={email} onChangeText={setEmail} style={styles.saisiChamp}/>
          </View>

          {/* Renseigner le code reçu par mail */}
          <View style={styles.aligne}>
            <Text style={styles.title_ID_MDP}>Code de sécurité reçu par mail</Text>
            <TextInput value={code} onChangeText={setCode} style={styles.saisiChamp}/>
          </View>

          {/* Nouveau mot de passe choisi */}
          <View style={styles.aligne}>
            <Text style={styles.title_ID_MDP}>Nouveau mot de passe</Text>
            <View style={styles.entreeCrayon}>
              <TextInput value={motDePasse} secureTextEntry={!showPassword} onChangeText={setMDP} style={[styles.saisiChamp, !codeEnvoye && { opacity: 0.5 }]} editable={codeEnvoye}/>
              <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
                <Image source={showPassword ? Oeil : OeilCache} style={styles.imageC}/>
              </TouchableOpacity>
            </View>
          </View>

          {/* Confirmation du nouveau mot de passe choisi*/}
          <View style={styles.aligne}>
            <Text style={styles.title_ID_MDP}>Confirmation du mot de passe</Text>
            <View style={styles.entreeCrayon}>
              <TextInput value={confirmMotDePasse} secureTextEntry={!showConfirmPassword} onChangeText={setConfirmMDP} style={[styles.saisiChamp, !codeEnvoye && { opacity: 0.5 }]} editable={codeEnvoye}/>
              <TouchableOpacity onPress={() => setShowConfirmPassword(!showConfirmPassword)}>
                <Image source={showConfirmPassword ? Oeil : OeilCache} style={styles.imageC}/>
              </TouchableOpacity>
            </View>
          </View>

          <View style={{ marginTop: 50 }}>
            <ButtonLog label='Valider' onPress={valider} backColor="#30D936" disabled={attenteChargement} loading={attenteChargement}/>
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
    fontSize: 30,
    fontWeight: 'bold',
    marginBottom: 50,
  },
  title_ID_MDP: {
    color: '#fff',
    fontSize: 17,
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


import { Image, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

import { useRouter } from 'expo-router';
import { useState } from 'react';
import HautPage from '../hautPage';

const imgMonCompte = require('@/assets/images/mon_compte.png');
const imgCrayon = require('@/assets/images/stylo.png');
const Oeil = require('@/assets/images/oeil.png');
const OeilCache = require('@/assets/images/oeil_cacher.png');


export default function Compte() {
    const [showPassword, setShowPassword] = useState(false);
    const router = useRouter();

  return (
    <>
    <View>
      <HautPage title="Mon compte" />
    </View>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
      >
      <ScrollView contentContainerStyle={styles.contenue}>
        <Image source={imgMonCompte} style={styles.imageH}/>


        <View style={styles.info}>
        

        {/* Nom */}
          <Text style={styles.text}>Nom</Text>
          <View style={styles.entreeCryon}>
            <TextInput style={styles.entree} placeholder="Macé"></TextInput>
            <TouchableOpacity  onPress={() => console.log('Bouton pressé')}>
              <Image source={imgCrayon} style={styles.imageC} />
            </TouchableOpacity>
          </View>



        {/* Prenom */}
          <Text style={styles.text}>Prénom</Text>
          <View style={styles.entreeCryon}>
            <TextInput style={styles.entree} placeholder="Bernardo"></TextInput>
            <TouchableOpacity  onPress={() => console.log('Bouton pressé')}>
              <Image source={imgCrayon} style={styles.imageC} />
            </TouchableOpacity>
          </View>



        {/* Numero de telephone */}
          <Text style={styles.text}>Numéro de téléphone</Text>
          <View style={styles.entreeCryon}>
            <TextInput keyboardType='phone-pad' style={styles.entree} placeholder="06737128"></TextInput>
            <TouchableOpacity  onPress={() => console.log('Bouton pressé')}>
              <Image source={imgCrayon} style={styles.imageC} />
            </TouchableOpacity>
          </View>
        

        {/* Email */}
        <Text style={styles.text}>Email</Text>
          <View style={styles.entreeCryon}>
            <TextInput keyboardType='email-address' style={styles.entree} placeholder="bernardo.mace@gmail.com"></TextInput>
            <TouchableOpacity  onPress={() => console.log('Bouton pressé')}>
              <Image source={imgCrayon} style={styles.imageC} />
            </TouchableOpacity>
          </View>
        
        
        
        {/* Mot de passe */}
        <Text style={styles.text}>Mot de passe</Text>
          <View style={styles.entreeCryon}>
            <TextInput style={styles.entree} placeholder="*****" secureTextEntry={!showPassword}></TextInput>

          <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
            <Image source={showPassword ? Oeil : OeilCache} style={styles.imageC} />
          </TouchableOpacity>
            <TouchableOpacity  onPress={() => console.log('Bouton pressé')}>
              <Image source={imgCrayon} style={styles.imageC} />
            </TouchableOpacity>
          </View>


        {/* Deconnexion */}
          <TouchableOpacity style={styles.boutton} onPress={() => router.navigate('/')}>
            <Text style={{color:'#ffffff'}}>SE DECONNECTER</Text>
          </TouchableOpacity>

        </View>
        
      </ScrollView>
    </KeyboardAvoidingView>

    </>
  );
}

const styles = StyleSheet.create({

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

  imageH: {
    width: 70,
    height: 70,
  },
  imageC: {
    width: 30,
    height: 30,
    marginLeft: 8,

  },


  boutton:{
    marginTop: 40,
    padding: 20,
    backgroundColor: '#E63946',
    borderRadius: 30,
    alignSelf: 'center',
  },

  info: {
    alignItems: 'flex-start',
    width: '70%', 
    marginVertical: 10, 
  },


  
  text: {
    marginTop: 20,
    marginBottom: 5,
    color: '#1D3557',
    fontWeight: '600',
    textAlign: 'left', 
    paddingLeft: 10,

  },
  entree: {
    flex: 1,
    backgroundColor: '#D4D4D4',
    width: '100%',
    height: 45,
    paddingHorizontal: 10,
    borderRadius: 30,
  },
});

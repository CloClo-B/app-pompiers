import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import HautPage from '../hautPage';

import CreerPoint from '@/app/creerPoint';
import PointSignale from '@/app/pointSignale';

// Gestion des points d'eau, affiche les différentes pages
export default function HomeScreen() {
  const { page: pageR } = useLocalSearchParams<{ page?: string }>();

  const [page, setPage] = useState("signale"); 
  const [choix, setChoix] = useState("signale"); 

  useEffect(() => {
    if (pageR) {
      setPage(pageR);
      setChoix(pageR);
    }
  }, [pageR]);

  return (

    <>
    <View>
      <HautPage title="Point d’eau signalé" />
    </View>


  {/* onglet entre deux choix */}
  <View style={styles.typeD}>

      <TouchableOpacity style={[styles.bouttonG, styles.boutton, choix === "signale" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("signale"); setChoix("signale");}}>
      <Text style={choix === "signale" ? styles.txtActif : styles.txtInactif}>Point d’eau signalé</Text>
      </TouchableOpacity>

      {/* <TextInput value={recherche} onChangeText={setRecherche} style={styles.recherche} placeholder="Rechercher un utilisateur" /> */}

      <TouchableOpacity style={[styles.bouttonD, styles.boutton, choix === "creer" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("creer"); setChoix("creer");}}>
      <Text style={choix === "creer" ? styles.txtActif : styles.txtInactif}>Créer un point d’eau</Text>
      </TouchableOpacity>
   




  {/* affichage */}
  </View>
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
    >


      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
      <View style={styles.contenue}>
          {page === "signale" && <PointSignale />}
          {page === "creer" && <CreerPoint />}
      </View>
        
      </ScrollView>
    </KeyboardAvoidingView>

    </>
  );
}

// Style
const styles = StyleSheet.create({
  contenue: {
    marginTop: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },

  typeD:{ 
    flexDirection: 'row',
    marginTop: 30,
    alignSelf: 'center',  
  },
  boutton:{
    paddingVertical: 15,
    paddingHorizontal:15,
    alignSelf: 'center',
    borderWidth: 1,
    borderColor: '#1D3557',
  },

  bouttonG:{
    borderTopLeftRadius: 26,
    borderBottomLeftRadius: 27,
  },

  bouttonD:{

    borderTopRightRadius: 26,
    borderBottomRightRadius: 27,
  },



  /* couleurs bouton état */
  bouttonActif:{
    backgroundColor: '#1D3557',
  },

  bouttonInactif:{
    backgroundColor: '#E7E7E7',
  },

  /* texte */
  txtActif:{
    color: '#ffffff',
  },
  txtInactif:{
    color: '#1D3557',
  }

});

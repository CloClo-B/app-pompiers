import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import HautPage from '../hautPage';

import CreerPoint from '@/app/creerPoint';
import PointSignale from '@/app/pointSignale';
import PropositionAjout from '@/app/propositionAjout';

// Gestion des points d'eau, affiche les différentes pages
export default function HomeScreen() {
  const { page: pageR } = useLocalSearchParams<{ page?: string }>();

  const [page, setPage] = useState("signale"); 
  const [sousPage, setSousPage] = useState("signalement");

  useEffect(() => {
    if (pageR) {
      setPage(pageR);
    }
  }, [pageR]);

  return (

    <>
    <View>
      <HautPage title="Point d’eau signalé" />
    </View>


  {/* onglet entre deux choix */}
  <View style={styles.typeD}>

      <TouchableOpacity style={[styles.bouttonG, styles.boutton, page === "signale" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("signale"); setPage("signale");}}>
      <Text style={page === "signale" ? styles.txtActif : styles.txtInactif}>Point d’eau signalé</Text>
      </TouchableOpacity>


      <TouchableOpacity style={[styles.bouttonD, styles.boutton, page === "creer" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("creer"); setPage("creer");}}>
      <Text style={page === "creer" ? styles.txtActif : styles.txtInactif}>Créer un point d’eau</Text>
      </TouchableOpacity>
  </View>
   


  {/* choix entre la pages des points d'eau signaler ou la pages des points d'eau en suggestion d'ajout */}
  {page === "signale" && (
    <View style={styles.typeD}>
      <TouchableOpacity
        style={[styles.bouttonG, styles.boutton, sousPage === "signalement" ? styles.bouttonActif : styles.bouttonInactif]}
        onPress={() => setSousPage("signalement")}
      >
        <Text style={sousPage === "signalement" ? styles.txtActif : styles.txtInactif}>
          Point signalé
        </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.bouttonD, styles.boutton, sousPage === "proposition" ? styles.bouttonActif : styles.bouttonInactif]}
        onPress={() => setSousPage("proposition")}
      >
        <Text style={sousPage === "proposition" ? styles.txtActif : styles.txtInactif}>
          Suggestion ajout
        </Text>
      </TouchableOpacity>

    </View>
  )}

  {/* affichage des pages en fonction du choix*/}
  <KeyboardAvoidingView
    style={{ flex: 1 }}
    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
  >
      {page === "signale" && sousPage === "signalement" && <PointSignale />}
      {page === "signale" && sousPage === "proposition" && <PropositionAjout />}
      {page === "creer" && <CreerPoint />}
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

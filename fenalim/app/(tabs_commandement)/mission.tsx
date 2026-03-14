import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

import HautPage from "@/app/hautPage";
import CreerMission from '@/app/creerMission';
import HistoriqueMission from '@/app/historiqueMission';
import MissionEnCours from "@/app/missionEnCours";


// Gestion des Missions, affiche les différentes pages
export default function HomeScreen() {
  const { page: pageR } = useLocalSearchParams<{ page?: string }>();

  const [page, setPage] = useState("enCours"); 
  const [choix, setChoix] = useState("enCours"); 

  useEffect(() => {
    if (pageR) {
      setPage(pageR);
      setChoix(pageR);
    }
  }, [pageR]);

  return (

    <>
    <View>
      <HautPage title="Mission" />
    </View>


  {/* choix type demande */}
  <View style={styles.typeD}>

      <TouchableOpacity style={[styles.boutonG, styles.bouton, choix === "creer" ? styles.boutonActif : styles.boutonInactif]} onPress={() => {setPage("creer"); setChoix("creer");}}>
      <Text style={choix === "creer" ? styles.txtActif : styles.txtInactif}>Créer mission</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.bouton, choix === "enCours" ? styles.boutonActif : styles.boutonInactif]} onPress={() => {setPage("enCours"); setChoix("enCours");}}>
      <Text style={choix === "enCours" ? styles.txtActif : styles.txtInactif}>En cours</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.boutonD, styles.bouton, choix === "historique" ? styles.boutonActif : styles.boutonInactif]} onPress={() => {setPage("historique"); setChoix("historique");}}>
      <Text style={choix === "historique" ? styles.txtActif : styles.txtInactif}>Historique</Text>
      </TouchableOpacity>
   
  </View>

    {/* affichage */}
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={0}
    >

      {page === "creer" && (
        <ScrollView>
          <CreerMission />
        </ScrollView>
      )}

      {page === "enCours" && (
        <View style={{ flex: 1 }}>
          <MissionEnCours />
        </View>
      )}

      {page === "historique" && (
        <View style={{ flex: 1 }}>
          <HistoriqueMission />
        </View>
      )}

    </KeyboardAvoidingView>

    </>
  );
}

// Style
const styles = StyleSheet.create({
  contenue: {
    marginTop: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },

  typeD:{ 
    flexDirection: 'row',
    marginTop: 20,
    alignSelf: 'center',  
  },
  
  bouton:{
    paddingVertical: 15,
    paddingHorizontal:20,
    alignSelf: 'center',
    borderWidth: 1,
    borderColor: '#1D3557',
  },

  boutonG:{
    borderTopLeftRadius: 26,
    borderBottomLeftRadius: 27,
  },

  boutonD:{

    borderTopRightRadius: 26,
    borderBottomRightRadius: 27,
  },



  /* couleurs bouton état */
  boutonActif:{
    backgroundColor: '#1D3557',
  },

  boutonInactif:{
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

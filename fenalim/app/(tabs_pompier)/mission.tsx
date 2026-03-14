import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

import HautPage from "@/app/hautPage";
import HistoriqueMission from '@/app/historiqueMission';
import MissionEnCours from "@/app/missionEnCours";


// Affichage des missions
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
      <TouchableOpacity style={[styles.bouttonG, styles.boutton , choix === "enCours" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("enCours"); setChoix("enCours");}}>
        <Text style={choix === "enCours" ? styles.txtActif : styles.txtInactif}>En cours</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.bouttonD, styles.boutton, choix === "historique" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("historique"); setChoix("historique");}}>
        <Text style={choix === "historique" ? styles.txtActif : styles.txtInactif}>Historique</Text>
      </TouchableOpacity>
  </View>
   

   {/* affichage */}

      <View style={[styles.contenue]} >
          {page === "enCours" && <MissionEnCours />}
          {page === "historique" && <HistoriqueMission />}
      </View>
        

    </>
  );
}

// Style
const styles = StyleSheet.create({
  contenue: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },


  typeD:{ 
    flexDirection: 'row',
    marginTop: 20,
    alignSelf: 'center',  
  },
  
  boutton:{
    paddingVertical: 15,
    paddingHorizontal:20,
    alignSelf: 'center',
    borderWidth: 1,
    borderColor: '#1D3557',
  },

  bouttonG:{
    borderTopLeftRadius: 30,
    borderBottomLeftRadius: 30,
  },

  bouttonD:{
    borderTopRightRadius: 30,
    borderBottomRightRadius: 30,
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

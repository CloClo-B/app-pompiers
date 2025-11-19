import { useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

import CreerPoint from '../creerPoint';
import HautPage from '../hautPage';
import PointSignale from '../pointSignale';

export default function HomeScreen() {
  const [page, setPage] = useState("signale"); 
  const [choix, setChoix] = useState("signale"); 

  return (

    <>
    <View>
      <HautPage title="Point d’eau signalé" />
    </View>


  {/* choix type demande */}
  <View style={styles.typeD}>

      <TouchableOpacity style={[styles.bouttonG, styles.boutton, choix === "signale" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("signale"); setChoix("signale");}}>
      <Text style={choix === "signale" ? styles.txtActif : styles.txtInactif}>Point d’eau signalé</Text>
      </TouchableOpacity>

      <TouchableOpacity style={[styles.bouttonD, styles.boutton, choix === "creer" ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => {setPage("creer"); setChoix("creer");}}>
      <Text style={choix === "creer" ? styles.txtActif : styles.txtInactif}>Créer un point d’eau</Text>
      </TouchableOpacity>
   
  </View>
    <View>
        {page === "signale" && <PointSignale />}
        {page === "creer" && <CreerPoint />}
    </View>

    </>
  );
}

const styles = StyleSheet.create({

  typeD:{ 
    flexDirection: 'row',
    marginTop: 40,
    alignItems: 'center',
       
  },
  boutton:{
    paddingVertical: 15,
    paddingHorizontal:25,
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

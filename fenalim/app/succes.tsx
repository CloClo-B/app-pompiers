import { useLocalSearchParams } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { Button, Image, StyleSheet, Text, View } from 'react-native';
import { naviguerPointEau, naviguerMission, naviguerAccueil } from '@/config/navigation';
import { getRole } from "@/service/infosStocker";
import ButtonLog from '@/components/ButtonLog';

const reussi = require('@/assets/images/succes.png');

// Page des Succes creation ou supression (point_eau, missions, signalement, supression ...)
// la page est appelée depuis les autres pages et contient le message envoyer en parametre 
export default function CreationSucces() {
  const [userRole, setUserRole] = useState<string | null>(null);
  
  // récupérer le role
  useEffect(() => {
    const chargerRole = async () => {
      const role = await getRole();
      setUserRole(role);
    };
    chargerRole();
  }, []);
  const params = useLocalSearchParams();
  
  // message affiché sur la page 
  const title = params.title;
  // page de redirection fonctionne en fonction du rôle
  const page = params.page;

  // Redirection de page
  const choixType = () => {
  if (userRole){
    if(page=="point_eau"){
      naviguerPointEau(userRole);
    }
    else if(page=="missions"){
      naviguerMission(userRole);
    }
    else if(page=="acceuil"){
      naviguerAccueil(userRole);
    }
    else{
      console.log("nom de la route incorect");
    }
  }
  else {
    alert("Rôle utilisateur introuvable")
  };
}
  return (
    <>    

    {/* reussi */}
      <View style={[styles.tout, {marginTop:20}]}>

        <Text style={styles.text}>{title}</Text>
        <Image source={reussi} style={styles.imageR}></Image>

    {/* retour */}
      <ButtonLog label="CONTINUER" onPress={choixType} type="primary" width={250} height={55}/>
    </View>
    </>
  );
}

// Style
const styles = StyleSheet.create({
  tout:{
    alignSelf: 'center',
    alignItems: "center",
    justifyContent: 'center',
    flex: 1,
  },

  text: {
    textAlign:'center',
    marginBottom: 5,
    color: '#1D3557',
    fontSize: 40,
    fontWeight: '600',
  },
  imageR: {
    width: 100,
    height: 100,
  },

});

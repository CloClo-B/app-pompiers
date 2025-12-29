import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { naviguerPointEau, naviguerMission } from '../config/navigation';
const reussi = require('@/assets/images/succes.png');
import { getData } from "../config/recupRole"; 

export default function CreationSucces() {
  const [userRole, setUserRole] = useState<string | null>(null);
  
  // récupérer le role 
  useEffect(() => {
  const chargerRole = async () => {
    const role = await getData();
    setUserRole(role);
  };
    chargerRole();
  }, []);
  const params = useLocalSearchParams();

  const title = params.title;
  const page = params.page;

  const choixType = () => {
  if (userRole){
    if(page=="point_eau"){
      naviguerPointEau(userRole);
    }
    else if(page=="missions"){
      naviguerMission(userRole);
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
        <TouchableOpacity style={styles.boutton} onPress={() => {choixType()}}>
          <Text style={{color:'#ffffff', fontSize:20}}>CONTINUER</Text>
        </TouchableOpacity>
    </View>
    </>
  );
}

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

  boutton:{
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
    marginTop: 15, 
    backgroundColor: '#457B9D', 
    width: 250, 
    height: 55
},




});

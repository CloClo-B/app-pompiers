import { router } from 'expo-router';
import React from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

export default function CreerMission() {
 
  return (
    <>  
    {/* nom mission */}
    <View style={styles.tout}>
      <Text style={styles.text}>Nom de la mission</Text> 
      <TextInput style={styles.entree} placeholder=""></TextInput>
    </View> 


    {/* afficher la carte */}
      <View style={styles.tout}>
        <Text style={styles.text}>Localisation incendie</Text> 
        <TouchableOpacity style={[styles.boutton, {backgroundColor: '#457B9D', width: 250, height: 45}]} onPress={() => console.log("afficher carte")}>
          <Text style={{color:'#ffffff'}}>AFFICHER SUR LA CARTE</Text>
        </TouchableOpacity>
    </View>


    {/* Choix du point d’eau */}
      <View style={styles.tout}>
        <Text style={styles.text}>Choix du point d’eau</Text> 
        <TouchableOpacity style={[styles.boutton, {backgroundColor: '#457B9D', width: 250, height: 45}]} onPress={() => console.log("afficher carte")}>
          <Text style={{color:'#ffffff'}}>AFFICHER SUR LA CARTE</Text>
        </TouchableOpacity>
    </View>

    {/* message mission */}
    <View style={styles.tout}>
      <Text style={styles.text}>Détails de la mission</Text>
          <TextInput style={styles.entreeD} maxLength={250} multiline={true} placeholder="Ecrivez ici"></TextInput>

    </View>


    {/* creer */}
      <View style={styles.tout}>
        <TouchableOpacity style={[styles.boutton, {marginTop: 15, backgroundColor: '#457B9D', width: 200, height: 45}]} onPress={() => router.navigate({ pathname: '/creationSucces', params: {title: 'Mission créée avec succès', nomPage: 'creer', chemainPage: '/(tabs)/mission'}})}>
          <Text style={{color:'#ffffff'}}>CREER</Text>
        </TouchableOpacity>
    </View>

    </>
  );
}

const styles = StyleSheet.create({
  tout:{
    alignSelf: 'center',
    alignItems: "center",
    marginTop: 20,
  },

  text: {
    marginBottom: 5,
    color: '#1D3557',
    fontSize: 15,
    fontWeight: '600',
    alignSelf: 'center',
  },
  menuD: {
    borderRadius: 30,
    width: '90%',
  },
  entree: {
    backgroundColor: '#ffffffff',
    width: 340,
    height: 50,
    paddingHorizontal: 10,
    borderRadius: 30,
    borderWidth: 1,
    borderColor: '#1D3557',
  },
  boutton:{
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
  },

  entreeD: {
    width: 300,
    height: 282,
    borderWidth: 1,
    borderColor: '#1D3557',
    backgroundColor: '#D4D4D4',
    paddingVertical:15,
    paddingHorizontal: 15,
    borderRadius: 20,
    textAlignVertical:"top",
  },



});

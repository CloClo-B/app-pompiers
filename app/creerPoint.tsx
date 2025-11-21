import { router } from 'expo-router';
import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';

export default function CreerPoint() {
 
  const [openType, setOpenType] = useState(false);
  const [valueType, setValueType] = useState(null);

  const [typePoint, setItemsType] = useState ([ 
    { label : 'Hydrant (borne incendie)' , value : 'hydrant' }, 
    { label : 'Poteau incendie' , value : 'poteau' }, 
    { label : 'Point d’eau naturel (rivière, étang, lac…)' , value : 'naturel' }, 
    { label : 'Point d’eau artificiel (bassin, réserve)' , value : 'artificiel' }, 
    { label : 'Citerne enterrée' , value : 'citerne_enterrée' }, 
    { label : 'Réservoir agricole (cuve, tonne)' , value : 'agricole' }, 
    { label : 'Point d’eau privé déclaré utilisable' , value : ' prive' }, 
  ]);
  
  const [openEtat, setOpenEtat] = useState(false);
  const [valueEtat, setValueEtat] = useState(null);

  const [etatPoint, setItemsEtat] = useState ([ 
    { label : 'Fonctionnel' , value : 'fonctionnel' }, 
    { label : 'Non fonctionnel' , value : 'nonFonctionnel' }, 

  ]);
  return (
    <>    

    {/* type point eau */}
    <View style={styles.tout}>
      <Text style={styles.text}>Type de point d’eau</Text> 
      <DropDownPicker
        open={openType}
        value={valueType}
        items={typePoint}
        setOpen={setOpenType}
        setValue={setValueType}
        setItems={setItemsType}
        placeholder="Sélectionnez un type de point d'eau"
        listMode="SCROLLVIEW"
        style={styles.menuD}
      />
    </View> 

    {/* etat poin eau */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>État du point d’eau</Text> 
      <DropDownPicker 
        open={openEtat} 
        value={valueEtat} 
        items={etatPoint} 
        setOpen={setOpenEtat} 
        setValue={setValueEtat} 
        setItems={setItemsEtat} 
        placeholder="Sélectionnez l'état du point d'eau" 
        listMode= "SCROLLVIEW"
        style={styles.menuD}
      /> 
    </View> 
  
    {/* debit */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Débit en L/min</Text> 
      <TextInput keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* capacite */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Capacité en L</Text> 
      <TextInput keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 


    {/* afficher la carte */}
      <View style={[styles.tout, {marginTop:20}]}>
        <Text style={styles.text}>Localisation du point d’eau</Text> 
        <TouchableOpacity style={[styles.boutton, {backgroundColor: '#457B9D', width: 250, height: 45}]} onPress={() => console.log("afficher carte")}>
          <Text style={{color:'#ffffff'}}>AFFICHER SUR LA CARTE</Text>
        </TouchableOpacity>
    </View>

    {/* creer */}
      <View style={[styles.tout, {marginTop:20}]}>
        <TouchableOpacity style={[styles.boutton, {marginTop: 15, backgroundColor: '#457B9D', width: 200, height: 45}]} onPress={() => router.navigate('/creation_point_succes')}>
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
  },

  text: {
    marginBottom: 5,
    color: '#1D3557',
    fontSize: 15,
    fontWeight: '600',
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


});

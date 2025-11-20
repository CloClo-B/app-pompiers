import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, View } from 'react-native';
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
  
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Débit en L/min</Text> 
      <TextInput keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Capacité en L</Text> 
      <TextInput keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
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


});

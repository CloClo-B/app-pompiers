import { router } from 'expo-router';
import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';
import axios from 'axios';



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

  const [debit, setDebit] = useState('');
  const [pression, setPression] = useState('');
  const [capacite, setCapacite] = useState('');
  const [longitude, setLongitude] = useState('');
  const [latitude, setLatitude] = useState('');

const creerPointAPI = async () => {
  try {
    // 172.20.10.2:8000 valentin
    const response = await axios.post('http:/172.20.10.2:8000/points_eau/', {
      numero_pei: 'ftgyhujioijhujfdhgyu',
      nom: 'Pompe A',
      statut: 'PUBLIC',
      type_nature: valueType,
      insee5: '29001', 
      accessibilite: '',
      disponibilite: '',
      carto_ref: null,
      press_deb: parseFloat(pression),
      debit_1_bar: parseFloat(debit),
      vol_eau_mi: parseFloat(capacite),
      longitude: parseFloat(longitude),
      latitude: parseFloat(latitude),
      utilisateur: '', //ne pas oublié par la suite c'est pour savoir qui a ajouter le point 
      date_crea: new Date().toISOString(),
      date_maj: new Date().toISOString()
    });
    console.log(response.data);
    router.push({
      pathname: '/creationSucces',
      params: { title: 'Point d’eau créé avec succès', nomPage: 'creer', chemainPage: '/point_eau' }
    });
  } catch (error) {
    console.error(error);
    alert('Erreur lors de la création du point d’eau');
  }
};


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

    {/* etat point eau */}
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
      <TextInput value={debit} onChangeText={setDebit} keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* préssion */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>préssion</Text> 
      <TextInput value={pression} onChangeText={setPression} keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* capacite */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Capacité en L</Text> 
      <TextInput keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* longitude */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Longitude</Text> 
      <TextInput value={longitude} onChangeText={setLongitude} keyboardType='numbers-and-punctuation' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* lattitude */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Lattitude</Text> 
      <TextInput value={latitude} onChangeText={setLatitude} keyboardType='numbers-and-punctuation' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* creer */}
      <View style={[styles.tout, {marginTop:20}]}>
        <TouchableOpacity style={[styles.boutton, {marginTop: 15, backgroundColor: '#457B9D', width: 200, height: 45}]} onPress={creerPointAPI}>
          <Text style={{color:'#ffffff'}}>CREER</Text>
        </TouchableOpacity>
    </View>
{/* router.navigate({ pathname: '/creationSucces', params: {title: 'Point d’eau créé avec succès', nomPage: 'creer', chemainPage: '/point_eau'}}) */}
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

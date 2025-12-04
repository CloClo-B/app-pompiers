import { router } from 'expo-router';
import React, { createRef, useState } from 'react';
import { AccessibilityInfo, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';
import axios from 'axios';



export default function CreerPoint() {
  
  
  
  
  // variable pour ensuite envoyer à l'api

  // liste déroulante
  const [valueType, setValueType] = useState(null);
  const [valueDispo, setValueDispo] = useState(null);
  const [valueAcces, setValueAcces] = useState(null);
  // text input
  const [numeroPEI, setNumeroPEI] = useState('');

  const [debit, setDebit] = useState('');
  const [pression, setPression] = useState('');
  const [volumeMin, setVolumeMin] = useState('');
  const [longitude, setLongitude] = useState('');
  const [latitude, setLatitude] = useState('');
  const [insee5, setInsee5] = useState('');
  const [refCarto, setRefCarto] = useState('');

  
  
  
  
  

  // liste pour les type de point d'eau
  const [openType, setOpenType] = useState(false);
  const [typePoint, setItemsType] = useState ([ 
    { label : 'BI' , value : 'BI' }, 
    { label : 'BI100' , value : 'BI100' }, 
    { label : 'PENA' , value : 'PENA' }, 
    { label : 'PI100' , value : 'PI100' }, 
    { label : 'PI110' , value : 'PI110' }, 
    { label : 'PI150' , value : 'PI150' }, 
    { label : 'PI65' , value : 'PI65' },
    { label : 'PI70' , value : 'PI70' }, 
    { label : 'PI80' , value : 'PI80' }, 
    { label : 'RESERVE EAU INCENDIE' , value : 'RESERVE EAU INCENDIE' }, 
    
  ]);
  
  // liste pour les différents niveau de disponibilité
  const [openDispo, setOpenDispo] = useState(false);
  const [etatDispo, setItemsDispo] = useState ([ 
    { label : 'DI' , value : 'DI' }, 
    { label : 'IN' , value : 'IN' }, 
  ]);
  
  // liste pour les différents niveau d'accès
  const [openAcces, setOpenAcces] = useState(false);
  const [etatAcces, setItemsAcces] = useState ([ 
    { label : 'C' , value : 'C' }, 
    { label : 'NC' , value : 'NC' }, 
    { label : 'NON' , value : 'NON' }, 

  ]);

  // liste pour les différents statut
  const [openStatut, setOpenStatut] = useState(false);
  const [valueStatut, setValueStatut] = useState(null);
  const [etatStatut, setItemsStatut] = useState ([ 
    { label : 'Public' , value : 'PUBLIC' }, 
    { label : 'Privé' , value : 'PRIVE' }, 
  ]);
  // une seul ouverture a la fois sinon erreur 
  const onOpenType = () => { setOpenDispo(false); setOpenAcces(false); setOpenStatut(false); };
  const onOpenDispo = () => { setOpenType(false); setOpenAcces(false); setOpenStatut(false); };
  const onOpenAcces = () => { setOpenType(false); setOpenDispo(false); setOpenStatut(false); };
  const onOpenStatut = () => { setOpenType(false); setOpenDispo(false); setOpenAcces(false); };
  
  
 


  // communication avec l'api  /points-eau/
  // valentin : 172.20.10.2 | 192.168.1.184
  const creerPointAPI = async () => {

    // Avant l'appel API, pour vérifier les valeurs
  console.log("Vérification des valeurs à envoyer\n");
  console.log("numeroPEI:", numeroPEI);
  console.log("nom:", ""); // a changer par la suite
  console.log("statut:", valueStatut);
  console.log("type_nature:", valueType);
  console.log("insee5:", insee5);
  console.log("accessibilite:", valueAcces);
  console.log("disponibilite:", valueDispo);
  console.log("carto_ref:", refCarto ? parseInt(refCarto) : null);
  console.log("press_deb:", parseFloat(pression));
  console.log("debit_1_bar:", parseFloat(debit));
  console.log("vol_eau_mi:", parseFloat(volumeMin));
  console.log("longitude:", parseFloat(longitude));
  console.log("latitude:", parseFloat(latitude));
  console.log("utilisateur:", "");

    try {
      const response = await axios.post('http://10.201.126.118:8000/points-eau/', {
        numero_pei: parseInt(numeroPEI),
        nom: '',
        statut: valueStatut,
        type_nature: valueType,
        insee5: insee5, 
        accessibilite: valueAcces,
        disponibilite: valueDispo,
        carto_ref: parseInt(refCarto)  ? parseInt(refCarto) : null ,
        press_deb: parseFloat(pression),
        debit_1_bar: parseFloat(debit),
        vol_eau_mi: parseFloat(volumeMin),
        longitude: parseFloat(longitude),
        latitude: parseFloat(latitude),
        utilisateur: '', //ne pas oublié par la suite c'est pour savoir qui a ajouter le point 
      });
      
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
    <View style={[styles.tout, { zIndex: 400 }]}>
      <Text style={styles.text}>Type de point d’eau</Text> 
      <DropDownPicker
        open={openType}
        value={valueType}
        items={typePoint}
        setOpen={setOpenType}
        setValue={setValueType}
        setItems={setItemsType}
        onOpen={onOpenType}
        placeholder="Sélectionnez un type de point d'eau"
        listMode="SCROLLVIEW"
        style={styles.menuD}
      />
    </View> 

    {/* disponiilite */}
    <View style={[styles.tout, {zIndex: 300, marginTop:20}]}>
      <Text style={styles.text}>Disponibilité du point d’eau</Text> 
      <DropDownPicker 
        open={openDispo} 
        value={valueDispo} 
        items={etatDispo} 
        setOpen={setOpenDispo} 
        setValue={setValueDispo} 
        setItems={setItemsDispo}
        onOpen={onOpenDispo}
        placeholder="Sélectionnez la disponibilité du point d'eau" 
        listMode= "SCROLLVIEW"
        style={styles.menuD}
      /> 
    </View> 

    {/* accessibilite */}
    <View style={[styles.tout, {zIndex: 200, marginTop:20}]}>
      <Text style={styles.text}>Acceésibilite du point d’eau</Text> 
      <DropDownPicker 
        open={openAcces} 
        value={valueAcces} 
        items={etatAcces} 
        setOpen={setOpenAcces} 
        setValue={setValueAcces} 
        setItems={setItemsAcces}
        onOpen={onOpenAcces}
        placeholder="Sélectionnez le niveau d'accèes du point d'eau" 
        listMode= "SCROLLVIEW"
        style={styles.menuD}
      /> 
    </View> 

    {/* statut */}
    <View style={[styles.tout, {zIndex: 100, marginTop:20}]}>
      <Text style={styles.text}>Statut du point d’eau</Text> 
      <DropDownPicker 
        open={openStatut} 
        value={valueStatut} 
        items={etatStatut} 
        setOpen={setOpenStatut} 
        setValue={setValueStatut} 
        setItems={setItemsStatut}
        onOpen={onOpenStatut}
        placeholder="Sélectionnez le statut du point d'eau" 
        listMode= "SCROLLVIEW"
        style={styles.menuD}
      /> 
    </View> 
  
    {/* numero PEI */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Numéro PEI</Text> 
      <TextInput value={numeroPEI} onChangeText={setNumeroPEI} keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
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

    {/* volume eau */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Volume eau minimum en L</Text> 
      <TextInput value={volumeMin} onChangeText={setVolumeMin} keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

   {/* insee5 */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>insee5</Text> 
      <TextInput value={insee5} onChangeText={setInsee5} keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* ref carto */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Référence carthographique</Text> 
      <TextInput value={refCarto} onChangeText={setRefCarto} keyboardType='number-pad' style={styles.entree} placeholder=""></TextInput>
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
        <TouchableOpacity style={[styles.boutton, {marginTop: 15, backgroundColor: '#457B9D', width: 200, height: 45}]} onPress = {creerPointAPI} >
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
  

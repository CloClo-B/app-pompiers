import { useRouter } from 'expo-router';
import React, {useEffect, useState } from 'react';
import {StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_ENDPOINTS } from '@/config/api';

// Page création de Point d'eau
export default function CreerPoint() {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);

  // récupérer le token 
  useEffect(() => {
    getData();
  }, []);
  const getData = async () => {
    try {
      const value = await AsyncStorage.getItem('@token')
      if(value !== null) {
        setToken(value);
      }
    } catch(e) {
      console.log("erreur token creation point eau");
    }
  }
  
  // variable pour ensuite envoyer à l'api

  // liste déroulante
  const [valueType, setValueType] = useState(null);
  const [valueDispo, setValueDispo] = useState(null);
  const [valueAcces, setValueAcces] = useState(null);
  const [valueStatut, setValueStatut] = useState(null);
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
  const [etatStatut, setItemsStatut] = useState ([ 
    { label : 'Public' , value : 'PUBLIC' }, 
    { label : 'Privé' , value : 'PRIVE' }, 
  ]);

  // une seul ouverture a la fois sinon erreur 
  const onOpenType = () => { setOpenDispo(false); setOpenAcces(false); setOpenStatut(false); };
  const onOpenDispo = () => { setOpenType(false); setOpenAcces(false); setOpenStatut(false); };
  const onOpenAcces = () => { setOpenType(false); setOpenDispo(false); setOpenStatut(false); };
  const onOpenStatut = () => { setOpenType(false); setOpenDispo(false); setOpenAcces(false); };
  
  
  // méthode verifiaction champs correct avant d'envoyer à l'api
  const verifTypePoint = (type: string) => {
    const typesValides = ['BI','BI100','PENA','PI100','PI110','PI150','PI65','PI70','PI80','RESERVE EAU INCENDIE'];
    return typesValides.includes(type);
  }
  const verifDispo = (dispo: string) => {
    const dispoValides = ['DI', 'IN'];
    return dispoValides.includes(dispo);
  }

  const verifAcces = (acces: string) => {
    const accesValides = ['C', 'NC', 'NON'];
    return accesValides.includes(acces);
  }
 
  const verifTypeStatut = (type: string) => {
    const typeValides = ['PUBLIC', 'PRIVE'];
    return typeValides.includes(type);
  }
  

  
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
  
  if (!token) {
    alert("Token manquant, impossible de créer le point d'eau");
    return;
  }
  else{
    console.log(token);
  }

  // vérfication des valeurs correct avant envoyer à l'api + affichage message de l'erreur
  if(valueType == null || verifTypePoint(valueType) == false){
    console.log("Erreur le type de point est incorrect");
    alert("Le type de point est incorrect");
    return;
  }
  else if(valueDispo == null || verifDispo(valueDispo) == false){
    console.log("Erreur la disponibilité du point est incorrect");
    alert("La disponibilité du point est incorrect");
    return;  
  }
  else if(valueAcces == null || verifAcces(valueAcces) == false){
    console.log("Erreur l'accèe de point est incorrect");
    alert("Le type d'accèe du point est incorrect");
    return; 
  }
  else if(valueStatut == null || verifTypeStatut(valueStatut) == false){
    console.log("Erreur le statut du point est incorrect");
    alert("Le statut du est incorrect");
    return;  
  }
  else if(numeroPEI == null || !numeroPEI.trim() || Number.isInteger(Number(numeroPEI)) == false){
    console.log("Erreur le numéro pei est incorrect");
    alert("Le numéro pei est incorect");
    return;  
  }
  else if(debit == null || !debit.trim() || isNaN(Number(debit.replace(',', '.'))) || (parseFloat(debit.replace(',', '.')) <=0)){
    console.log("Erreur le débit est incorrect");
    alert("Le débit est incorect");
    return;  
  }
  else if(pression == null || !pression.trim() || isNaN(Number(pression.replace(',', '.'))) || (parseFloat(pression.replace(',', '.')) <=0)){
    console.log("Erreur la préssion est incorrect");
    alert("La préssion est incorect");
    return;  
  }
  else if(volumeMin == null || !volumeMin.trim() || isNaN(Number(volumeMin.replace(',', '.'))) || (parseFloat(volumeMin.replace(',', '.')) <=0)){
    console.log("Erreur le volume minimum est incorrect");
    alert("Le volume minimum est incorect");
    return;  
  }
  else if(insee5 == null || !insee5.trim() || insee5.length>10 || Number.isInteger(Number(insee5)) == false || parseInt(insee5) <=0 ){
    console.log("Erreur le code insee5 est incorrect");
    alert("Le code insee5 est incorect");
    return;  
  }
  else if(refCarto == null || !refCarto.trim() || Number.isInteger(Number(refCarto)) == false || (parseInt(refCarto) <=0)){
    console.log("Erreur la référence carthographique est incorrect");
    alert("La référence carthographique est incorect");
    return;  
  }
  else if(longitude == null || !longitude.trim() || isNaN(Number(longitude.replace(',', '.'))) || (parseFloat(longitude.replace(',', '.')) <-180) || (parseFloat(longitude.replace(',', '.'))) > 180){
    console.log("Erreur la longitude est incorrect");
    alert("La longitude est incorect");
    return;  
  }
  else if(latitude == null || !latitude.trim() || isNaN(Number(latitude.replace(',', '.')))  || (parseFloat(latitude.replace(',', '.')) <-90) || (parseFloat(latitude.replace(',', '.')) > 90)){
    console.log("Erreur la latitude est incorrect");
    alert("La latitude est incorect");
    return;  
  }

    else{
      try {
        const response = await axios.post(API_ENDPOINTS.POINTS_EAU, {
          numero_pei: parseInt(numeroPEI),
          nom: '',
          statut: valueStatut,
          type_nature: valueType,
          insee5: insee5, 
          accessibilite: valueAcces,
          disponibilite: valueDispo,
          carto_ref: parseInt(refCarto)  ? parseInt(refCarto) : null ,
          press_deb: parseFloat(pression.replace(',', '.')),
          debit_1_bar: parseFloat(debit.replace(',', '.')),
          vol_eau_mi: parseFloat(volumeMin.replace(',', '.')),
          longitude: parseFloat(longitude.replace(',', '.')),
          latitude: parseFloat(latitude.replace(',', '.')),
          utilisateur: '', //ne pas oublié par la suite c'est pour savoir qui a ajouter le point 
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
        
        router.push({
            pathname: '/succes',
            params: { title: 'Point d’eau créé avec succès', page:"point_eau" }
          });
        }
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          // erreur renvoyée par l’API
          console.log(error.response?.status);
          console.log(error.response?.data);
          alert(error.response?.data?.detail ?? "Erreur lors de la création du point d'eau");
        } else {
          // autre erreur
          alert("Erreur lors de la création du point d'eau");
        }
      }

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
      <TextInput value={debit} onChangeText={setDebit} keyboardType='decimal-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 


    {/* préssion */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>préssion</Text> 
      <TextInput value={pression} onChangeText={setPression} keyboardType='decimal-pad' style={styles.entree} placeholder=""></TextInput>
    </View> 

    {/* volume eau */}
    <View style={[styles.tout, {marginTop:20}]}>
      <Text style={styles.text}>Volume eau minimum en L</Text> 
      <TextInput value={volumeMin} onChangeText={setVolumeMin} keyboardType='decimal-pad' style={styles.entree} placeholder=""></TextInput>
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
  

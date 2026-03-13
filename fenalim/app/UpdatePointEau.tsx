import { useLocalSearchParams, useRouter } from 'expo-router';
import React, {useEffect, useState } from 'react';
import {KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';
import axios from 'axios';
import { getPointEauByID, updatePointEau } from '@/service/pointEauService';
import { getRole, getToken } from '@/service/infosStocker';
import ButtonLog from '@/components/ButtonLog';
import { naviguerAccueil } from '@/config/navigation';
import proj4 from "proj4";

// Page création de Point d'eau
export default function UpdatePointEau() {
  const router = useRouter();
  
  const [role, setRole] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  


  // recuper l'id du point a modifier
  const { idPoint } = useLocalSearchParams<{ idPoint: string }>();
  const [IDPoint, setIDPoint] = useState(''); 
  const [ID, setID] = useState(''); 

    // recupere les infos du point d'eau 
    useEffect(() => {
    const init = async () => {
        if (!idPoint) return;
        setIDPoint(idPoint);

        try {
        const tokenValue = await getToken();
        const roleValue = await getRole();
        if(tokenValue && roleValue){
            setToken(tokenValue);
            setRole(roleValue);

            const data = await getPointEauByID(tokenValue, idPoint);
            
            // convertion des données
            const lambert93 = "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs";
            const wgs84 = "+proj=longlat +datum=WGS84 +no_defs";

            const lonWGS = proj4(lambert93, wgs84, [273478, 6750525])[0];
            const latWGS = proj4(lambert93, wgs84, [273478, 6750525])[1];
            console.log("response.data:", data);
            setID(data.id?.toString() ?? '');
            setNumeroPEI(data.numero_pei?.toString() ?? '');
            setValueType(data.type_nature ?? null);
            setValueDispo(data.disponibilite ?? null);
            setValueAcces(data.accessibilite ?? null);
            setValueStatut(data.statut ?? null);
            setDebit(data.debit_1_bar?.toString() ?? '');
            setPression(data.press_deb?.toString() ?? '');
            setVolumeMin(data.vol_eau_mil?.toString() ?? '');
            setLongitude(lonWGS.toString());
            setLatitude(latWGS.toString());
            setInsee5(data.insee5?.toString() ?? '');
            setRefCarto(data.carto_ref?.toString() ?? '');
        }
        } catch(error){
        console.log("Erreur récupération point d'eau :", error);
        alert("Impossible de récupérer les informations du point d'eau.");
        }
    };

    init();
    }, [idPoint]);

  
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

    // info pour envoyer avec l'api
    const info = {
        numero_pei: Number(numeroPEI),
        statut: valueStatut,
        type_nature: valueType,
        insee5,
        accessibilite: valueAcces,
        disponibilite: valueDispo,
        carto_ref: refCarto,
        press_deb: parseFloat(pression.replace(',', '.')),
        debit_1_bar: parseFloat(debit.replace(',', '.')),
        vol_eau_mil: parseFloat(volumeMin.replace(',', '.')),
        longitude: parseFloat(longitude.replace(',', '.')),
        latitude: parseFloat(latitude.replace(',', '.'))
    };


  



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
  

  
  // communication avec l'api  /points-eau/update
  const UpdatePointAPI = async () => {

    // Avant l'appel API, pour vérifier les valeurs
  console.log("Vérification des valeurs à envoyer\n");
  console.log("numeroPEI:", numeroPEI);
  // console.log("nom:", "");
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
  console.log(token);
  
  // vérfication des valeurs correct avant envoyer à l'api + affichage message de l'erreur
  if (!token) {
    alert("Erreur, impossible de créer le point d'eau");
    return;
  }
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

        // appel du fichier pointEauService pour la envoyer la requete de modification de point d'eau 
        await updatePointEau(token, Number(ID), info);

        
        router.push({
            pathname: '/succes',
            params: { title: 'Point d’eau modifié avec succès', page:"point_eau" }
          });
        }
      catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          // erreur renvoyée par l’API
          console.log(JSON.stringify(error.response?.data, null, 2));
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
    <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
      >
        <View style={styles.tout}>
            {/* hydrant selectionner */}
            <Text style={styles.choixhydrant}> Hydrant #{IDPoint}</Text>
        </View> 

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
                placeholderStyle={{ color: '#9e9c9c' }}
                listMode="SCROLLVIEW"
                style={styles.menuD}
            />
        </View> 

        {/* disponibilité */}
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
                placeholderStyle={{ color: '#9e9c9c' }}
                listMode= "SCROLLVIEW"
                style={styles.menuD}
            /> 
        </View> 

        {/* accessibilité */}
        <View style={[styles.tout, {zIndex: 200, marginTop:20}]}>
            <Text style={styles.text}>Accessibilité du point d’eau</Text> 
            <DropDownPicker 
                open={openAcces} 
                value={valueAcces} 
                items={etatAcces} 
                setOpen={setOpenAcces} 
                setValue={setValueAcces} 
                setItems={setItemsAcces}
                onOpen={onOpenAcces}
                placeholder="Sélectionnez le niveau d'accès du point d'eau"
                placeholderStyle={{ color: '#9e9c9c' }}
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
                placeholderStyle={{ color: '#9e9c9c' }}
                listMode= "SCROLLVIEW"
                style={styles.menuD}
            /> 
        </View> 
        
        
            {/* debit */}
            <View style={[styles.tout, {marginTop:20}]}>
            <Text style={styles.text}>Débit en L/min</Text> 
            <TextInput value={debit} onChangeText={setDebit} keyboardType='decimal-pad' style={styles.entree} placeholder=""></TextInput>
            </View> 


            {/* préssion */}
            <View style={[styles.tout, {marginTop:20}]}>
            <Text style={styles.text}>Pression</Text> 
            <TextInput value={pression} onChangeText={setPression} keyboardType='decimal-pad' style={styles.entree} placeholder=""></TextInput>
            </View> 

            {/* volume eau */}
            <View style={[styles.tout, {marginTop:20}]}>
            <Text style={styles.text}>Volume eau minimum en L</Text> 
            <TextInput value={volumeMin} onChangeText={setVolumeMin} keyboardType='decimal-pad' style={styles.entree} placeholder=""></TextInput>
            </View> 

            {/* insee5 */}
            <View style={[styles.tout, {marginTop:20}]}>
            <Text style={styles.text}>INSEE5</Text> 
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
            <Text style={styles.text}>Latitude</Text> 
            <TextInput value={latitude} onChangeText={setLatitude} keyboardType='numbers-and-punctuation' style={styles.entree} placeholder=""></TextInput>
            </View> 


            <View style={[styles.tout, styles.validation]}>
                {/* retour */}
                <View style={[styles.tout, {marginTop:20}]}>
                    <ButtonLog label="ANNULER" onPress={() => { if (role) naviguerAccueil(role); else alert("Rôle utilisateur introuvable"); }} type="primary" width={150} height={45} />
                </View>
                {/* modifier */}
                <View style={[styles.tout, {marginTop:20}]}>
                    <ButtonLog label="MODIFIER" onPress={UpdatePointAPI} type="primary" width={200} height={45} marginTop={15}/>
                </View>
            </View>

        </KeyboardAvoidingView>
      </ScrollView>

    </>
  );
}




const styles = StyleSheet.create({
  contenue: {
    marginTop: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
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
  validation:{
    flexDirection: 'row',
    alignItems: 'center',
    gap:'10%',    
  },
  choixhydrant: {
    marginBottom: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    backgroundColor:'#c8cac8ff',
    borderRadius: 40,
    fontSize: 20,
  },
});
  

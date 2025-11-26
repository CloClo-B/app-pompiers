import { useLocalSearchParams, useRouter } from 'expo-router';
import React from 'react';
import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
const reussi = require('@/assets/images/succes.png');

export default function CreationSucces() {
  const router = useRouter();
  const params = useLocalSearchParams();

  const title = params.title;
  const nomPage = params.nomPage;
  const chemainPage = params.chemainPage;
  return (
    <>    

    {/* reussi */}
      <View style={[styles.tout, {marginTop:20}]}>

        <Text style={styles.text}>{title}</Text>
        <Image source={reussi} style={styles.imageR}></Image>

    {/* retour */}
        <TouchableOpacity style={styles.boutton} onPress={() => router.push({ pathname: chemainPage as any, params: { page: nomPage }})}>
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

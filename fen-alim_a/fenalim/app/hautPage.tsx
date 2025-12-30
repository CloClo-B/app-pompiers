import { Image } from 'expo-image';
import { StyleSheet, Text, View } from 'react-native';

const imgSDIS = require('@/assets/images/logo_sdis_56-detoure.png');

export default function hautPage({ title }: { title: string }) {
  return (

    <View style={styles.container}>

      <View style={styles.rectangle1}></View>
      <View style={styles.rectangle2}></View>

      <Image source={imgSDIS} style={styles.imageSdis}/>
      <Text style={styles.leTexte}>{title}</Text>
    </View>
  
);
}

const styles = StyleSheet.create({
  container: {
    backgroundColor:'#1D3557',    
    width: '100%',
    height: 75,
    alignItems: 'center',
    justifyContent: 'center',
  },
  rectangle1: {
    width: 80,
    height: 40,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.4)', 
    left: 20,
    position: 'absolute',
  },
  rectangle2: {
    top: 17,
    width: 80,
    height: 40,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.4)', 
    left: 15,
    position: 'absolute',
  },
  imageSdis: {
    width: 80,
    height: 50,
    zIndex: 2,
    left: 15,
    position: 'absolute',
  },
  leTexte: {
  position: 'absolute',
  left: '30%',
  fontSize: 18,

  color: '#ffffff',
},
});
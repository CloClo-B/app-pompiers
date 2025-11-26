import { Image } from 'expo-image';
import { StyleSheet, View } from 'react-native';

const imgSDIS = require('@/assets/images/logo_sdis_56-detoure.png');

export default function ImageLogo() {
  return (

    <View style={styles.container}>

      <View style={styles.rectangle1}></View>
      <View style={styles.rectangle2}></View>

      <Image source={imgSDIS} style={styles.imageSdis}/>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 300,
    height: 150,
    alignItems: 'center',
    justifyContent: 'center',
  },
  rectangle1: {
    width: 300,
    height: 120,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.4)', 
    right: 15,
    position: 'relative',
  },
  rectangle2: {
    top: 30,
    width: 300,
    height: 120,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.4)', 
    left: 15,
    position: 'absolute',
  },
  imageSdis: {
    width: 290,
    height: 80,
    zIndex: 2,
    top: 40,
    position: 'absolute',
  },
});

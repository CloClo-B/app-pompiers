import { Image } from 'expo-image';
import { StyleSheet, Text, View, TouchableOpacity, ActivityIndicator } from 'react-native';

// Logo du SDIS
const imgSDIS = require('@/assets/images/logo_sdis_56-detoure.png');

// Haut des Pages de l'appplication
export default function hautPage({ title, onLogoPress, isRefreshing = false }: { title: string; onLogoPress?: () => void; isRefreshing?: boolean }) {
  return (

    <View style={styles.container}>

      <View style={styles.rectangle1}></View>
      <View style={styles.rectangle2}></View>

      <TouchableOpacity onPress={onLogoPress} activeOpacity={0.7} disabled={isRefreshing} style={styles.logoButton}>
        {isRefreshing ? (
          <ActivityIndicator size="small" color="#ffffff" />
        ) : (<Image source={imgSDIS} style={styles.imageSdis}/>)}
      </TouchableOpacity>
      <Text style={styles.leTexte}>{title}</Text>
    </View>
  
);
}

// Style
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
    left: 5,
    position: 'absolute',
  },
  logoButton: {
    width: 80,
    height: 50,
    zIndex: 2,
    left: 15,
    position: 'absolute',
    justifyContent: 'center',
    alignItems: 'center',
  },
  leTexte: {
  position: 'absolute',
  left: '30%',
  fontSize: 18,

  color: '#ffffff',
},
});
import { Image } from 'expo-image';
import { useRouter } from 'expo-router';

import { LinearGradient } from 'expo-linear-gradient';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import Button from '@/components/ButtonLog';
import ImageLogo from '@/components/LogoSDIS56';

const Flamme = require('@/assets/images/flamme1.png');


// Page index qui affiche les méthodes de connection
export default function Accueil() {
  const router = useRouter();

  return (
    <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
        <LinearGradient colors={['#E63946', '#1D3557']} style={styles.container}>

                <View>
                    <ImageLogo/>
                </View>

                <View style={{ alignItems: 'center'}}>
                    <Image source={Flamme} style={styles.imageFlamme}/>
                    <Text style={styles.title}>FEN-Alim</Text>
                </View>


                <View style={{ marginTop: 40}}>
                    <Button label="Se connecter" type="connexion" onPress={() => router.navigate('/connexion')} />
                    <Button label="S'inscrire" type="inscription" onPress={() => router.navigate('/inscription')} />
                </View>
                
        </LinearGradient>
    </ScrollView>
  );
}

// Style
const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 40,
  },
  imageFlamme: {
    width: 290,
    height: 300,
    transform: [{ scale: 0.5 }],
  },
  title: {
    color: '#fff',
    fontSize: 40,
    fontWeight: 'bold',
    position: 'absolute',
    top: '50%',
  },
  title2: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
});

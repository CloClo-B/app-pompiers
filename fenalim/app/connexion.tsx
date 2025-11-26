import { LinearGradient } from 'expo-linear-gradient';
import { useRouter } from 'expo-router';

import { ScrollView, StyleSheet, Text, View } from 'react-native';

import Button from '@/components/ButtonLog';
import Saisi from '@/components/RectangleSaisi';

export default function Connexion() {
  const router = useRouter();

  return (
    <ScrollView>
        <LinearGradient colors={['#E63946', '#1D3557']} style={styles.container}>

                <View>
                    <Text style={[styles.title,{marginTop: 30}]}>Connexion</Text>
                </View>

                <View style={styles.aligne}>
                  <Text style={styles.title_ID_MDP}>Identifiant</Text>
                  <Saisi />
                </View>

                <View style={styles.aligne}>
                    <Text style={styles.title_ID_MDP}>Mot de passe</Text>
                    <Saisi/>
                </View>

                <View style={{ marginTop: 50}}>
                    <Button label='Connexion' onPress={() => router.navigate('/acceuil')} backColor="#30D936"/>
                </View>

                <View>
                    <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Mot de passe oublié' onPress={() => {console.log('en cours')}}/>
                    <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Créer un compte' onPress={() => router.navigate('/inscription')}/>
                </View>
                
        </LinearGradient>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 40,
  },
  title: {
    color: '#fff',
    fontSize: 40,
    fontWeight: 'bold',
    marginBottom: 70,
  },
  title_ID_MDP: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    alignSelf: 'flex-start',
  },
  aligne: {
    width: '80%', 
    maxWidth: 300, 
    alignSelf: 'center', 
    marginTop: 20,
  },
});

import { StyleSheet, Text, View } from 'react-native';


export default function MissionEnCours() {
  return (
    <>    

    <View style={styles.hautBleu}>
      <Text style={styles.textTittre}>Nom mission</Text>
      <Text style={styles.textTittre}>Distance</Text>
      <Text style={styles.textTittre}>Date</Text>
      <Text style={styles.textTittre}>Partir</Text>
    </View>
    
    </>
  );
}

const styles = StyleSheet.create({
  hautBleu:{
    borderTopLeftRadius: 15,
    borderTopRightRadius: 15,
    width: 350,
    height: 40,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    backgroundColor: '#1D3557',
  },
  textTittre:{
    color: '#ffffff',
    fontSize: 17,
  }
});

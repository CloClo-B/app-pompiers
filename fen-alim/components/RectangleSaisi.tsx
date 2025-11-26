import { StyleSheet, TextInput } from 'react-native';

export default function Saisi() {
  return (
    <TextInput style={styles.saisiChamp}/>
  );
}

const styles = StyleSheet.create({
  saisiChamp: {
    width: '100%',
    height: 40, 
    color: '#000000ff',
    backgroundColor: '#fff',
    borderRadius: 10,
    paddingHorizontal: 10,
  }
});

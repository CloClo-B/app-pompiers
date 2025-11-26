import { Pressable, StyleSheet, Text, View } from 'react-native';

type Props = {
  label: string;
  onPress?: () => void;
  type?: 'connexion' | 'inscription';
  backColor?: string;
  color?: string;
};

export default function Button({ label, onPress, type = 'connexion', backColor='#fff', color='#000000ff'}: Props) {
  return (
    <View style={[styles.container, type === 'connexion' ? styles.connexion : styles.inscription, {backgroundColor: backColor}]}>
      <Pressable onPress={onPress} style={styles.press}>
        <Text style={[styles.buttonLabel,{color: color}]}>{label}</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 100,
    borderRadius: 40,
    height: 50,
    width: 300,
  },
  connexion: {
    marginBottom: 20,
    backgroundColor: '#fff',
  },
  inscription: {
    backgroundColor: '#f1f1f1',
  },
  press: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonLabel: {
    color: '#183BB1',
    fontSize: 18,
    fontWeight: 'bold',
  },
  mdpLost: {
    fontSize: 5,
    marginBottom: 20,
    backgroundColor: '#fff',
  },
});

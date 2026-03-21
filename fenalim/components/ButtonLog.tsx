import { Pressable, StyleSheet, Text, View, ActivityIndicator } from 'react-native';

type Props = {
  label: string;
  onPress?: () => void;
  type?: 'connexion' | 'inscription' | 'action' | 'primary' | 'secondary' | 'itineraire' | 'mission' | 'signalement' | 'valider';
  backColor?: string | undefined;
  color?: string;
  width?: number | `${number}%` | 'auto';
  height?: number;
  marginTop?: number | undefined;
  borderRadius?: number | undefined;
  marginBottom?: number | undefined;
  padding?: number | number | undefined;
  fontWeight?: string | undefined;
  textAlign?: string | undefined;
  disabled?: boolean;
  alignSelf?: 'center'| undefined;
  loading?: boolean;
};

export default function Button({
  label,
  onPress,
  type = 'connexion',
  backColor = undefined,
  color = undefined,
  width = 300 as number | `${number}%` | 'auto',
  height = 50,
  marginTop = 0,
  borderRadius = undefined,
  marginBottom = undefined,
  padding = undefined,
  disabled = false,
  loading = false,

}: Props) {
  return (
    <View style={[
      styles.container,
      type === 'connexion' ? styles.connexion
      : type === 'inscription' ? styles.inscription
      : type === 'primary' ? styles.primary
      : type === 'secondary' ? styles.secondary
      : type === 'itineraire' ? styles.itineraire
      : type === 'mission' ? styles.mission
      : type === 'signalement' ? styles.signalement
      : type === 'valider' ? styles.valider
      : styles.action,
      { width, height, marginTop, 
        ...(backColor && { backgroundColor: backColor }),
        ...(borderRadius && { borderRadius }),
        ...(marginBottom && { marginBottom }),
        ...(padding && { padding }),
        ...(disabled && { opacity: 0.5 }),
      }
    ]}>
      <Pressable onPress={disabled ? undefined : onPress} style={styles.press}>
        {loading ? (
          <ActivityIndicator size="small" color={color || '#ffffff'} />
        ) : (

          <Text style={[
            styles.buttonLabel,
            type === 'primary' || type === 'secondary' || 
            type === 'itineraire' || type === 'mission' || 
            type === 'signalement' || type === 'valider'
            ? { color: color || '#ffffff' }
            :type === 'action'
            ? { color: color || '#000000' }
            : { color: color || '#0e0d0d' }
          ]}>
            {label}
          </Text>
        )}
      </Pressable>
    </View>
    
  );
}

import { router, useRouter } from 'expo-router';

// boutons de la page connexion (unique)
export function BoutonInscription() {
  const router = useRouter();

  return (
    <View>
      <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Créer un compte' onPress={() => router.navigate('/inscription')}/>
    </View>
  );
}

// boutons de la page inscription (unique)
export function BoutonConnexion() {
  const router = useRouter();

  return (
    <View>
      <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Connexion' onPress={() => router.navigate('/connexion')}/>
    </View>
  );
}

// boutons de la page connexion (unique)
export function BoutonMdpOublie() {
  const router = useRouter();

  return (
    <View>
      <Button color='rgba(255, 255, 255, 0.86)' backColor='rgba(255, 255, 255, 0)' label='Mot de passe oublié' onPress={() => router.navigate('/mdp_oublie')}/>
    </View>
  );
}



const styles = StyleSheet.create({
  container: {
    borderRadius: 40,
    height: 50,
    width: 300,
    alignSelf: 'center'
  },
  connexion: {
    marginBottom: 20,
    backgroundColor: '#fff',
  },

  inscription: {
    backgroundColor: '#f1f1f1',
  },

  // Bleu clair pour CREER, CONFIRMER, Fermer
  primary: {
    backgroundColor: '#457B9D',
    color: '#fff',
  },

  // Rouge pour SUPPRIMER, SE DECONNECTER
  secondary: {
    backgroundColor: '#E63946',
  },

  // Bleu pour afficher l'itinéraire d'une mission
  itineraire: {
    backgroundColor: '#007AFF',
    borderRadius: 8,
    marginBottom: 10,
  },

  // Orange pour Créer une mission
  mission: {
    backgroundColor: '#FF9500',
    borderRadius: 8,
    marginBottom: 10,
  },

  // Rouge pour signalement
  signalement: {
    backgroundColor: '#FF3B30',
    borderRadius: 8,
    marginBottom: 10,
  },

  valider: {
    backgroundColor: '#06A77D',
    marginTop: 20,
  },

  //  Les boutons uniques
  action: {},
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

});
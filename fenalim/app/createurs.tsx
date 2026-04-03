import React, { useState } from 'react';
import { LinearGradient } from 'expo-linear-gradient';
import { FontAwesome } from '@expo/vector-icons';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Linking, Alert } from 'react-native';

export default function Createurs() {
  const [fields, setFields] = useState({
    titre: '',
    description: '',
    telephone: '',
    email: '',
    entreprise: '',
  });

  const handleChange = (key: keyof typeof fields, value: string) => {
    setFields((prev) => ({ ...prev, [key]: value }));
  };

  const openLink = async (url: string) => {
    try {
      const supported = await Linking.canOpenURL(url);
      if (!supported) {
        Alert.alert('Lien non supporté', `Impossible d\'ouvrir ce lien : ${url}`);
        return;
      }
      await Linking.openURL(url);
    } catch (err) {
      Alert.alert('Erreur', "Impossible d\'ouvrir le lien");
    }
  };

  const [status, setStatus] = useState<'en attente' | 'accepté' | 'refusé'>('en attente');

  return (
    <LinearGradient colors={['#E63946', '#1D3557']} style={styles.root}>
      <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
        <Text style={styles.header}>Créateurs</Text>

        <View style={styles.cardContainer}>

            <View style={styles.card}>
                <Text style={styles.cardLabel}>Clovis BOURRE - Développeur</Text>
                <Text style={styles.cardLabel2} >Mail</Text>
                <Text style={styles.input}>clovisbrr.pro@protonmail.com</Text>

                <Text style={styles.cardLabel2}>Réseaux sociaux</Text>
                <View style={styles.socialRow}>
                    <TouchableOpacity style={styles.socialButtonLinkedin} onPress={() => openLink('https://www.linkedin.com/in/clovis-bourre/')}>
                        <FontAwesome name="linkedin-square" size={28} color="#0A66C2" />
                        <Text style={styles.socialText}>LinkedIn</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.socialButtonGithub} onPress={() => openLink('https://github.com/CloClo-B')}>
                        <FontAwesome name="github" size={28} color="#d3afaf" />
                        <Text style={styles.socialText}>GitHub</Text>
                    </TouchableOpacity>
                </View>

            </View>

            <View style={styles.card}>
                <Text style={styles.cardLabel}>Valentin HUTA-CEVER - développeur</Text>
                <Text style={styles.cardLabel2} >Mail</Text>
                <Text style={styles.input}>hutavalentin@gmail.com</Text>

                <Text style={styles.cardLabel2}>Réseaux sociaux</Text>
                <View style={styles.socialRow}>
                    <TouchableOpacity style={styles.socialButtonLinkedin} onPress={() => openLink('https://www.linkedin.com/in/valentin-huta-773802354/')}>
                        <FontAwesome name="linkedin-square" size={28} color="#0A66C2" />
                        <Text style={styles.socialText}>LinkedIn</Text>
                    </TouchableOpacity>
                </View>

            </View>

            <View style={styles.card}>
                <Text style={styles.cardLabel}>Mathéo BIET - développeur</Text>
                <Text style={styles.cardLabel2} >Mail</Text>
                <Text style={styles.input}></Text>

                <Text style={styles.cardLabel2}>Réseaux sociaux</Text>
                <View style={styles.socialRow}>
                    <TouchableOpacity style={styles.socialButtonLinkedin} onPress={() => openLink('https://www.linkedin.com/in/ton-profil')}>
                        <FontAwesome name="linkedin-square" size={28} color="#0A66C2" />
                        <Text style={styles.socialText}>LinkedIn</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.socialButtonGithub} onPress={() => openLink('https://github.com/ton-profil')}>
                        <FontAwesome name="github" size={28} color="#d3afaf" />
                        <Text style={styles.socialText}>GitHub</Text>
                    </TouchableOpacity>
                </View>

            </View>

            <View style={styles.card}>
                <Text style={styles.cardLabel}>Teï Garnier - développeur</Text>
                <Text style={styles.cardLabel2} >Mail</Text>
                <Text style={styles.input}></Text>

                <Text style={styles.cardLabel2}>Réseaux sociaux</Text>
                <View style={styles.socialRow}>
                    <TouchableOpacity style={styles.socialButtonLinkedin} onPress={() => openLink('https://www.linkedin.com/in/ton-profil')}>
                        <FontAwesome name="linkedin-square" size={28} color="#0A66C2" />
                        <Text style={styles.socialText}>LinkedIn</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.socialButtonGithub} onPress={() => openLink('https://github.com/ton-profil')}>
                        <FontAwesome name="github" size={28} color="#d3afaf" />
                        <Text style={styles.socialText}>GitHub</Text>
                    </TouchableOpacity>
                </View>

            </View>

            <View style={styles.card}>
                <Text style={styles.cardLabel}>Clément HOARAU - développeur</Text>
                <Text style={styles.cardLabel2} >Mail</Text>
                <Text style={styles.input}></Text>

                <Text style={styles.cardLabel2}>Réseaux sociaux</Text>
                <View style={styles.socialRow}>
                    <TouchableOpacity style={styles.socialButtonLinkedin} onPress={() => openLink('https://www.linkedin.com/in/ton-profil')}>
                        <FontAwesome name="linkedin-square" size={28} color="#0A66C2" />
                        <Text style={styles.socialText}>LinkedIn</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.socialButtonGithub} onPress={() => openLink('https://github.com/ton-profil')}>
                        <FontAwesome name="github" size={28} color="#d3afaf" />
                        <Text style={styles.socialText}>GitHub</Text>
                    </TouchableOpacity>
                </View>

            </View>

        </View>
          
        <Text style={styles.tip}>
          Astuce : remplace les URLs par celles de tes profils personnels LinkedIn et GitHub.
        </Text>
        
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
  },
  scroll: {
    paddingHorizontal: 20,
    paddingBottom: 40,
    alignItems: 'center',
  },
  header: {
    color: '#fff',
    fontSize: 34,
    fontWeight: 'bold',
    marginTop: 60,
    marginBottom: 12,
  },
  subHeader: {
    color: '#fff',
    fontSize: 20,
    alignSelf: 'flex-start',
    marginTop: 8,
    marginBottom: 6,
  },
  cardContainer: {
    width: '100%',
  },
  card: {
    backgroundColor: '#FFFFFFCC',
    borderRadius: 14,
    padding: 18,
    marginVertical: 8,
    width: '100%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 5,
    elevation: 3,
  },
  cardLabel: {
    color: '#1D3557',
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 6,
  },
  cardLabel2: {
    color: '#5a6a80',
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 3,
    paddingTop: 10,
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#c5c5c5',
    paddingVertical: 8,
    paddingHorizontal: 10,
    color: '#111',
    fontSize: 15,
  },
  socialRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginTop: 5,
  },
  socialButtonGithub: {
    backgroundColor: '#f3eeeecc',
    borderRadius: 12,
    paddingVertical: 10,
    paddingHorizontal: 16,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    flex: 1,
    marginHorizontal: 4,
  },
  socialButtonLinkedin: {
    backgroundColor: '#16a7f5',
    borderRadius: 12,
    paddingVertical: 10,
    paddingHorizontal: 16,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    flex: 1,
    marginHorizontal: 4,
  },
  socialText: {
    color: '#1D3557',
    fontSize: 16,
    fontWeight: '700',
    marginLeft: 8,
  },
  statusRow: {
    flexDirection: 'row',
    width: '100%',
    marginTop: 12,
    justifyContent: 'space-around',
  },
  buttonAccept: {
    backgroundColor: '#06A77D',
    borderRadius: 12,
    paddingVertical: 12,
    paddingHorizontal: 20,
    flex: 1,
    marginRight: 8,
    alignItems: 'center',
  },
  buttonRefuse: {
    backgroundColor: '#E63946',
    borderRadius: 12,
    paddingVertical: 12,
    paddingHorizontal: 20,
    flex: 1,
    marginLeft: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '800',
  },
  statusCard: {
    marginTop: 16,
    width: '100%',
    backgroundColor: '#ffffffbb',
    borderRadius: 14,
    padding: 16,
    alignItems: 'center',
  },
  statusLabel: {
    color: '#1D3557',
    fontSize: 16,
    fontWeight: '600',
  },
  statusValue: {
    marginTop: 6,
    color: '#1D3557',
    fontSize: 18,
    fontWeight: '700',
  },
  tip: {
    color: '#fff',
    marginTop: 16,
    fontSize: 13,
    lineHeight: 18,
    textAlign: 'center',
    width: '100%',
    opacity: 0.9,
  },
});

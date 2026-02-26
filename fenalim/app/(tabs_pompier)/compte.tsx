import { Image, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View, Alert, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { useState, useEffect } from 'react';
import HautPage from "@/app/hautPage";
import authService, { UserData } from '@/service/authService';

// Icon
const imgMonCompte = require('@/assets/images/mon_compte.png');
const imgCrayon = require('@/assets/images/stylo.png');
const Oeil = require('@/assets/images/oeil.png');
const OeilCache = require('@/assets/images/oeil_cacher.png');

// Profil de l'utilisateur
export default function Compte() {
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [userData, setUserData] = useState<UserData | null>(null);
  
  // États pour les champs modifiables
  const [nom, setNom] = useState('');
  const [prenom, setPrenom] = useState('');
  const [telephone, setTelephone] = useState('');
  const [email, setEmail] = useState('');
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  
  // États pour savoir quels champs sont en cours d'édition
  const [editingNom, setEditingNom] = useState(false);
  const [editingPrenom, setEditingPrenom] = useState(false);
  const [editingTelephone, setEditingTelephone] = useState(false);
  const [editingEmail, setEditingEmail] = useState(false);
  const [changingPassword, setChangingPassword] = useState(false);
  
  const router = useRouter();

  // Charger les infos de l'utilisateur
  useEffect(() => {
    loadUserData();
  }, []);

  // Chargement des infos du user
  const loadUserData = async () => {
    try {
      setLoading(true);
      const data = await authService.getUserInfo();
      if (data) {
        setUserData(data);
        setNom(data.nom);
        setPrenom(data.prenom);
        setTelephone(data.telephone);
        setEmail(data.email);
      } else {
        Alert.alert('Erreur', 'Session expirée. Veuillez vous reconnecter.');
        router.navigate('/connexion');
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger vos informations.');
    } finally {
      setLoading(false);
    }
  };

  // Enregistre les Modifications
  const handleUpdateField = async (field: string, value: string) => {
    // Validation basique
    if (!value || value.trim() === '') {
      Alert.alert('Erreur', 'Le champ ne peut pas être vide');
      return;
    }

    if (field === 'telephone' && !/^\d{10}$/.test(value)) {
      Alert.alert('Erreur', 'Le numéro de téléphone doit contenir 10 chiffres');
      return;
    }

    if (field === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      Alert.alert('Erreur', 'Format d\'email invalide');
      return;
    }

    try {
      setSaving(true);
      await authService.updateUserInfo({ [field]: value });
      
      Alert.alert('Succès', 'Informations mises à jour');
      setEditingNom(false);
      setEditingPrenom(false);
      setEditingTelephone(false);
      setEditingEmail(false);
      await loadUserData();
    } catch (error: any) {
      Alert.alert('Erreur', error.message || 'Impossible de mettre à jour les informations');
      // Restaurer la valeur précédente
      if (userData) {
        if (field === 'nom') setNom(userData.nom);
        if (field === 'prenom') setPrenom(userData.prenom);
        if (field === 'telephone') setTelephone(userData.telephone);
        if (field === 'email') setEmail(userData.email);
      }
    } finally {
      setSaving(false);
    }
  };

  // Changement du mot de passe
  const handleChangePassword = async () => {
    if (!oldPassword || !newPassword || !confirmNewPassword) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs');
      return;
    }

    if (newPassword.length < 12) {
      Alert.alert('Erreur', 'Le nouveau mot de passe doit contenir au moins 12 caractères');
      return;
    }

    if (newPassword !== confirmNewPassword) {
      Alert.alert('Erreur', 'Les mots de passe ne correspondent pas');
      return;
    }

    try {
      setSaving(true);
      await authService.changePassword(oldPassword, newPassword, confirmNewPassword);
      
      Alert.alert('Succès', 'Mot de passe modifié avec succès');
      setOldPassword('');
      setNewPassword('');
      setConfirmNewPassword('');
      setChangingPassword(false);
    } catch (error: any) {
      Alert.alert('Erreur', error.message || 'Impossible de modifier le mot de passe');
    } finally {
      setSaving(false);
    }
  };

  // Déconnecte l'utilisateur
  const handleLogout = () => {
    Alert.alert(
      'Déconnexion',
      'Êtes-vous sûr de vouloir vous déconnecter ?',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Déconnecter',
          style: 'destructive',
          onPress: async () => {
            await authService.logout(userData?.id_utilisateur);
            router.navigate('/');
          },
        },
      ]
    );
  };

  // Texte lisible des Roles
  const getRoleLabel = (role: string) => {
    const labels = {
      'public': 'Utilisateur Public',
      'pompier': 'Pompier',
      'commandement': 'Commandement',
      'admin': 'Administrateur',
    };
    return labels[role as keyof typeof labels] || role;
  };
  
  // Couleur du badge selon le métier
  const getRoleBadgeColor = (role: string) => {
    const colors = {
      'public': '#457B9D',
      'pompier': '#E63946',
      'commandement': '#F77F00',
      'admin': '#06A77D',
    };
    return colors[role as keyof typeof colors] || '#1D3557';
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#E63946" />
        <Text style={styles.loadingText}>Chargement...</Text>
      </View>
    );
  }

  // Affiche la Page
  return (
    <>
      <View>
        <HautPage title="Mon compte" />
      </View>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
      >
        <ScrollView 
          contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} 
          keyboardShouldPersistTaps="handled"
        >
          <Image source={imgMonCompte} style={styles.imageH} />

          {/* Affichage du rôle (Badge) */}
          {userData && (
            <View style={[styles.roleBadge, { backgroundColor: getRoleBadgeColor(userData.role) }]}>
              <Text style={styles.roleText}>{getRoleLabel(userData.role)}</Text>
            </View>
          )}

          <View style={styles.info}>
            {/* Nom */}
            <Text style={styles.text}>Nom</Text>
            <View style={styles.entreeCryon}>
              <TextInput
                style={[styles.entree, !editingNom && styles.entreeDisabled]}
                value={nom}
                onChangeText={setNom}
                editable={editingNom}
              />
              {editingNom ? (
                <TouchableOpacity 
                  onPress={() => handleUpdateField('nom', nom)}
                  disabled={saving}
                >
                  <Text style={styles.saveButton}>✓</Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity onPress={() => setEditingNom(true)}>
                  <Image source={imgCrayon} style={styles.imageC} />
                </TouchableOpacity>
              )}
            </View>

            {/* Prénom */}
            <Text style={styles.text}>Prénom</Text>
            <View style={styles.entreeCryon}>
              <TextInput
                style={[styles.entree, !editingPrenom && styles.entreeDisabled]}
                value={prenom}
                onChangeText={setPrenom}
                editable={editingPrenom}
              />
              {editingPrenom ? (
                <TouchableOpacity 
                  onPress={() => handleUpdateField('prenom', prenom)}
                  disabled={saving}
                >
                  <Text style={styles.saveButton}>✓</Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity onPress={() => setEditingPrenom(true)}>
                  <Image source={imgCrayon} style={styles.imageC} />
                </TouchableOpacity>
              )}
            </View>

            {/* Numéro de téléphone */}
            <Text style={styles.text}>Numéro de téléphone</Text>
            <View style={styles.entreeCryon}>
              <TextInput
                keyboardType='phone-pad'
                style={[styles.entree, !editingTelephone && styles.entreeDisabled]}
                value={telephone}
                onChangeText={setTelephone}
                editable={editingTelephone}
                maxLength={10}
              />
              {editingTelephone ? (
                <TouchableOpacity 
                  onPress={() => handleUpdateField('telephone', telephone)}
                  disabled={saving}
                >
                  <Text style={styles.saveButton}>✓</Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity onPress={() => setEditingTelephone(true)}>
                  <Image source={imgCrayon} style={styles.imageC} />
                </TouchableOpacity>
              )}
            </View>

            {/* Email */}
            <Text style={styles.text}>Email</Text>
            <View style={styles.entreeCryon}>
              <TextInput
                keyboardType='email-address'
                style={[styles.entree, !editingEmail && styles.entreeDisabled]}
                value={email}
                onChangeText={setEmail}
                editable={editingEmail}
                autoCapitalize="none"
              />
              {editingEmail ? (
                <TouchableOpacity 
                  onPress={() => handleUpdateField('email', email)}
                  disabled={saving}
                >
                  <Text style={styles.saveButton}>✓</Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity onPress={() => setEditingEmail(true)}>
                  <Image source={imgCrayon} style={styles.imageC} />
                </TouchableOpacity>
              )}
            </View>

            {/* Changement de mot de passe */}
            <TouchableOpacity 
              style={styles.passwordChangeButton}
              onPress={() => setChangingPassword(!changingPassword)}
            >
              <Text style={styles.passwordChangeText}>
                {changingPassword ? 'Annuler le changement' : 'Modifier mon mot de passe'}
              </Text>
            </TouchableOpacity>

            {changingPassword && (
              <>
                <Text style={styles.text}>Ancien mot de passe</Text>
                <View style={styles.entreeCryon}>
                  <TextInput
                    style={styles.entree}
                    placeholder="Ancien mot de passe"
                    secureTextEntry={!showOldPassword}
                    value={oldPassword}
                    onChangeText={setOldPassword}
                    autoCapitalize="none"
                  />
                  <TouchableOpacity onPress={() => setShowOldPassword(!showOldPassword)}>
                    <Image source={showOldPassword ? Oeil : OeilCache} style={styles.imageC} />
                  </TouchableOpacity>
                </View>

                <Text style={styles.text}>Nouveau mot de passe</Text>
                <View style={styles.entreeCryon}>
                  <TextInput
                    style={styles.entree}
                    placeholder="Minimum 12 caractères"
                    secureTextEntry={!showNewPassword}
                    value={newPassword}
                    onChangeText={setNewPassword}
                    autoCapitalize="none"
                  />
                  <TouchableOpacity onPress={() => setShowNewPassword(!showNewPassword)}>
                    <Image source={showNewPassword ? Oeil : OeilCache} style={styles.imageC} />
                  </TouchableOpacity>
                </View>
                

                <Text style={styles.text}>Confirmer le mot de passe</Text>
                <View style={styles.entreeCryon}>
                  <TextInput
                    style={styles.entree}
                    placeholder="Confirmation"
                    secureTextEntry={!showNewPassword}
                    value={confirmNewPassword}
                    onChangeText={setConfirmNewPassword}
                    autoCapitalize="none"
                  />
                </View>

                <TouchableOpacity 
                  style={[styles.boutton, styles.validateButton]}
                  onPress={handleChangePassword}
                  disabled={saving}
                >
                  <Text style={{color:'#ffffff', fontWeight: '600'}}>
                    {saving ? 'ENREGISTREMENT...' : 'VALIDER'}
                  </Text>
                </TouchableOpacity>
              </>
            )}

            {/* Déconnexion */}
            <TouchableOpacity 
              style={styles.boutton} 
              onPress={handleLogout}
            >
              <Text style={{color:'#ffffff', fontWeight: '600'}}>SE DÉCONNECTER</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </>
  );
}

// Style
const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F1FAEE',
  },
  loadingText: {
    marginTop: 10,
    color: '#1D3557',
    fontSize: 16,
  },
  contenue: {
    marginTop: 40,
    alignItems: 'center',
    justifyContent: 'center',
  },
  entreeCryon: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
  },
  imageH: {
    width: 70,
    height: 70,
  },
  imageC: {
    width: 30,
    height: 30,
    marginLeft: 8,
  },
  saveButton: {
    fontSize: 30,
    color: '#06A77D',
    marginLeft: 8,
    fontWeight: 'bold',
  },
  boutton: {
    marginTop: 40,
    padding: 20,
    backgroundColor: '#E63946',
    borderRadius: 30,
    alignSelf: 'center',
  },
  validateButton: {
    backgroundColor: '#06A77D',
    marginTop: 20,
  },
  info: {
    alignItems: 'flex-start',
    width: '70%',
    marginVertical: 10,
  },
  text: {
    marginTop: 20,
    marginBottom: 5,
    color: '#1D3557',
    fontWeight: '600',
    textAlign: 'left',
    paddingLeft: 10,
  },
  entree: {
    flex: 1,
    backgroundColor: '#D4D4D4',
    width: '100%',
    height: 45,
    paddingHorizontal: 10,
    borderRadius: 30,
  },
  entreeDisabled: {
    backgroundColor: '#E8E8E8',
  },
  roleBadge: {
    marginTop: 10,
    marginBottom: 20,
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 20,
  },
  roleText: {
    color: '#ffffff',
    fontWeight: '700',
    fontSize: 14,
  },
  passwordChangeButton: {
    marginTop: 30,
    alignSelf: 'center',
  },
  passwordChangeText: {
    color: '#1D3557',
    fontWeight: '600',
    textDecorationLine: 'underline',
  },
});
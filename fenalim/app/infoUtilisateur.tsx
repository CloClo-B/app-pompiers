import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Alert, ActivityIndicator } from "react-native";
import HautPage from './hautPage';
import axios from "axios";
import { router, useLocalSearchParams } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {API_ENDPOINTS } from '@/config/api';

// Donnée de l'Utilisateur
type User = {
  id: string;
  nom: string;
  prenom: string;
  role: string;
  email: string;
  telephone: string;
};

type Role = 'public' | 'pompier' | 'commandement' | 'admin';


// Permet de consulter les informations d'un Utilisateur
export default function UserDetails() {
  const [token, setToken] = useState<string | null>(null);
  const [chargement, setChargement] = useState(true);
  const [utilisateur, setUtilisateur] = useState<User | null>(null);
  const [selectedRole, setSelectedRole] = useState<Role>('public');
  const [roleModified, setRoleModified] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [updating, setUpdating] = useState(false);
  
  const params = useLocalSearchParams();
  const id = params.id as string;

  // Récupérer le token 
  useEffect(() => {
    getData();
  }, []);

  const getData = async () => {
    try {
      const value = await AsyncStorage.getItem('@token');
      if (value !== null) {
        setToken(value);
        infoUtilisateurSelect(value);
      }
    } catch (e) {
      console.log("Erreur token affichage utilisateur");
    }
  };

  const infoUtilisateurSelect = async (token: string) => {
    if (!token) {
      Alert.alert("Erreur", "Token manquant");
      return;
    }
    try {
      const response = await axios.get(API_ENDPOINTS.USER_BY_ID(Number(id)), {
        headers: { Authorization: `Bearer ${token}` },
      });
      
      const userData = {
        id: String(response.data.id_utilisateur),
        nom: response.data.nom,
        prenom: response.data.prenom,
        role: response.data.role,
        email: response.data.email,
        telephone: response.data.telephone,
      };
      
      setUtilisateur(userData);
      setSelectedRole(response.data.role as Role);
    } catch (error) {
      console.error("Erreur lors du chargement de l'utilisateur :", error);
      Alert.alert("Erreur", "Impossible de récupérer l'utilisateur.");
    } finally {
      setChargement(false);
    }
  };

  // Gérer le changement de rôle dans le Picker
  const handleRoleChange = (newRole: Role) => {
    setSelectedRole(newRole);
    setRoleModified(newRole !== utilisateur?.role);
  };

  // Appliquer la modification du rôle
  const handleApplyRoleChange = async () => {
    if (!token || !utilisateur) return;

    if (!roleModified) {
      Alert.alert("Info", "Aucune modification à appliquer");
      return;
    }

    Alert.alert(
      "Confirmation",
      `Voulez-vous vraiment changer le rôle de ${utilisateur.prenom} ${utilisateur.nom} en "${getRoleLabel(selectedRole)}" ?`,
      [
        { text: "Annuler", style: "cancel" },
        {
          text: "Confirmer",
          onPress: async () => {
            try {
              setUpdating(true);
              await axios.put(
                API_ENDPOINTS.USER_BY_ID(Number(id)),
                { role: selectedRole },
                { headers: { Authorization: `Bearer ${token}` } }
              );

              Alert.alert("Succès", "Rôle modifié avec succès");
              setUtilisateur({ ...utilisateur, role: selectedRole });
              setRoleModified(false);
            } catch (error: any) {
              console.error("Erreur lors de la modification du rôle:", error);
              Alert.alert(
                "Erreur",
                error.response?.data?.detail || "Impossible de modifier le rôle"
              );
            } finally {
              setUpdating(false);
            }
          },
        },
      ]
    );
  };

  // Supprimer l'utilisateur
  const handleDeleteUser = async () => {
    if (!token || !utilisateur) return;

    // Vérifier si c'est le dernier admin
    if (utilisateur.role === 'admin') {
      try {
        const response = await axios.get(API_ENDPOINTS.USERS_LIST, {
          headers: { Authorization: `Bearer ${token}` },
        });
        
        const adminCount = response.data.filter((u: any) => u.role === 'admin').length;
        
        if (adminCount <= 1) {
          Alert.alert(
            "Suppression impossible",
            "Vous ne pouvez pas supprimer le dernier administrateur du système.",
            [{ text: "OK" }]
          );
          return;
        }
      } catch (error) {
        console.error("Erreur lors de la vérification des admins:", error);
      }
    }

    Alert.alert(
      "⚠️ Confirmation de suppression",
      `Êtes-vous vraiment sûr de vouloir supprimer l'utilisateur :\n\n${utilisateur.prenom} ${utilisateur.nom}\n(${utilisateur.email})\n\nCette action est irréversible !`,
      [
        { text: "Annuler", style: "cancel" },
        {
          text: "Supprimer",
          style: "destructive",
          onPress: async () => {
            try {
              setDeleting(true);
              await axios.delete(API_ENDPOINTS.USER_BY_ID(Number(id)), {
                headers: { Authorization: `Bearer ${token}` },
              });

              Alert.alert(
                "Succès",
                "Utilisateur supprimé avec succès",
                [
                  {
                    text: "OK",
                    onPress: () => router.navigate('/(tabs_admin)/utilisateur'),
                  },
                ]
              );
            } catch (error: any) {
              console.error("Erreur lors de la suppression:", error);
              Alert.alert(
                "Erreur",
                error.response?.data?.detail || "Impossible de supprimer l'utilisateur"
              );
            } finally {
              setDeleting(false);
            }
          },
        },
      ]
    );
  };

  const getRoleLabel = (role: string) => {
    const labels: { [key: string]: string } = {
      public: "Utilisateur Public",
      pompier: "Pompier",
      commandement: "Commandement",
      admin: "Administrateur",
    };
    return labels[role] || role;
  };

  const getRoleColor = (role: string) => {
    const colors: { [key: string]: string } = {
      public: "#457B9D",
      pompier: "#E63946",
      commandement: "#F77F00",
      admin: "#06A77D",
    };
    return colors[role] || "#1D3557";
  };

  if (chargement) {
    return (
      <>
        <View>
          <HautPage title="Utilisateur" />
        </View>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#457B9D" />
          <Text style={styles.loadingText}>Chargement...</Text>
        </View>
      </>
    );
  }

  if (!utilisateur) {
    return (
      <>
        <View>
          <HautPage title="Utilisateur" />
        </View>
        <View style={styles.container}>
          <Text>Utilisateur non trouvé</Text>
        </View>
      </>
    );
  }

  return (
    <>
      <View>
        <HautPage title="Utilisateur" />
      </View>

      <View style={styles.container}>
        <View style={styles.card}>
          {/* Titre avec badge de rôle */}
          <View style={styles.headerContainer}>
            <Text style={styles.titre}>Utilisateur</Text>
            <View
              style={[
                styles.roleBadge,
                { backgroundColor: getRoleColor(utilisateur.role) },
              ]}
            >
              <Text style={styles.roleBadgeText}>
                {getRoleLabel(utilisateur.role)}
              </Text>
            </View>
          </View>

          {/* Informations de l'utilisateur */}
          <View style={styles.infoBloc}>
            <Text style={styles.infoText}>
              <Text style={styles.infoLabel}>ID : </Text>
              {utilisateur.id}
            </Text>
            <Text style={styles.infoText}>
              <Text style={styles.infoLabel}>Nom : </Text>
              {utilisateur.nom}
            </Text>
            <Text style={styles.infoText}>
              <Text style={styles.infoLabel}>Prénom : </Text>
              {utilisateur.prenom}
            </Text>
            <Text style={styles.infoText}>
              <Text style={styles.infoLabel}>Email : </Text>
              {utilisateur.email}
            </Text>
            <Text style={styles.infoText}>
              <Text style={styles.infoLabel}>Téléphone : </Text>
              {utilisateur.telephone}
            </Text>
          </View>

          {/* Sélecteur de rôle  */}
          <View style={styles.roleSelector}>
            <Text style={styles.roleSelectorLabel}>Choisir un nouveau rôle :</Text>
            <View style={styles.roleButtonsContainer}>
              {(['public', 'pompier', 'commandement', 'admin'] as Role[]).map((role) => (
                <TouchableOpacity
                  key={role}
                  style={[
                    styles.roleOption,
                    selectedRole === role && { borderColor: getRoleColor(role), backgroundColor: getRoleColor(role) + '10' }, // +10 pour l'opacité
                    selectedRole === role && styles.roleOptionSelected
                  ]}
                  onPress={() => handleRoleChange(role)}
                >
                  <Text style={[
                    styles.roleOptionText,
                    selectedRole === role && { color: getRoleColor(role), fontWeight: 'bold' }
                  ]}>
                    {getRoleLabel(role)}
                  </Text>
                  {selectedRole === role && <Text style={{color: getRoleColor(role)}}> ✓</Text>}
                </TouchableOpacity>
              ))}
            </View>
            
            {roleModified && (
              <Text style={styles.modifiedIndicator}>
                Modification en attente d'application
              </Text>
            )}
          </View>

          {/* BOUTONS */}
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={[styles.button, styles.closeButton]}
              onPress={() => router.navigate('/(tabs_admin)/utilisateur')}
              disabled={updating || deleting}
            >
              <Text style={styles.buttonText}>FERMER</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.button,
                styles.applyButton,
                (!roleModified || updating || deleting) && styles.buttonDisabled,
              ]}
              onPress={handleApplyRoleChange}
              disabled={!roleModified || updating || deleting}
            >
              {updating ? (
                <ActivityIndicator color="#ffffff" size="small" />
              ) : (
                <Text style={styles.buttonText}>APPLIQUER</Text>
              )}
            </TouchableOpacity>
          </View>

          {/* Bouton de suppression */}
          <TouchableOpacity
            style={[
              styles.deleteButton,
              deleting && styles.buttonDisabled,
            ]}
            onPress={handleDeleteUser}
            disabled={updating || deleting}
          >
            {deleting ? (
              <ActivityIndicator color="#ffffff" size="small" />
            ) : (
              <Text style={styles.deleteButtonText}>SUPPRIMER L'UTILISATEUR</Text>
            )}
          </TouchableOpacity>
        </View>
      </View>
    </>
  );
}

// Style
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F1FAEE",
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F1FAEE",
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: "#1D3557",
  },
  card: {
    width: 360,
    backgroundColor: "#fff",
    borderRadius: 15,
    padding: 20,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  headerContainer: {
    alignItems: "center",
    marginBottom: 20,
  },
  titre: {
    textAlign: "center",
    fontSize: 26,
    fontWeight: "bold",
    color: "#1D3557",
    marginBottom: 10,
  },
  roleBadge: {
    paddingHorizontal: 15,
    paddingVertical: 5,
    borderRadius: 15,
  },
  roleBadgeText: {
    color: "#fff",
    fontWeight: "700",
    fontSize: 14,
  },
  infoBloc: {
    gap: 10,
    marginBottom: 20,
  },
  infoText: {
    fontSize: 16,
    color: "#1D3557",
  },
  infoLabel: {
    fontWeight: "bold",
    fontSize: 16,
  },
  roleSelector: {
    marginBottom: 20,
    width: '100%',
  },
  roleSelectorLabel: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1D3557",
    marginBottom: 10,
  },
  roleButtonsContainer: {
    flexDirection: 'column',
    gap: 8,
  },
  roleOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 12,
    paddingHorizontal: 15,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#D4D4D4',
    backgroundColor: '#fff',
  },
  roleOptionSelected: {
    borderWidth: 2,
  },
  roleOptionText: {
    fontSize: 15,
    color: '#457B9D',
  },
  modifiedIndicator: {
    marginTop: 10,
    fontSize: 13,
    color: "#F77F00",
    fontWeight: "600",
    textAlign: 'center',
  },
  buttonContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 10,
    marginBottom: 15,
  },
  button: {
    flex: 1,
    height: 45,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 30,
  },
  closeButton: {
    backgroundColor: "#457B9D",
  },
  applyButton: {
    backgroundColor: "#06A77D",
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "600",
    fontSize: 15,
  },
  deleteButton: {
    backgroundColor: "#E63946",
    height: 45,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 30,
  },
  deleteButtonText: {
    color: "#ffffff",
    fontWeight: "700",
    fontSize: 15,
  },
});
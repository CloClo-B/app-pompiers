import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Alert, Image, ScrollView, Platform, Linking } from "react-native";
import HautPage from '@/app/hautPage';
import { router, useLocalSearchParams} from 'expo-router';
import proj4 from "proj4";
import { naviguerPointEau } from '@/config/navigation';
import { API_ENDPOINTS } from '@//config/api';

import { getRole, getToken } from "@/service/infosStocker";
import ButtonLog from '@/components/ButtonLog';
import { deleteProposition, getPropositionByID } from "@/service/propoAjoutService";
import { CreatesignalerUtilisateur } from "@/service/SignalerUtilisateur";

// Donnée de la proposition
type Proposition = {
  id: string;
  description: string
  photo: string;
  mail_utilisateur: string;
  date_creation: string;
  latitude: number;
  longitude: number;
};

// Permet de consulter les informations d'une propostion
export default function InfoProposition() {
  const [token, setToken] = useState<string | null>(null);
  const [userRole, setUserRole] = useState<string | null>(null);
    
  useEffect(() => {
    const chargerRoleEtToken = async () => {
      try {
        // recup role et token
        const tokenValue = await getToken();
        const roleValue = await getRole();
        if (tokenValue){
          setToken(tokenValue);
        }
        if (roleValue){
          setUserRole(roleValue);
        }
        // afficher info
        if (tokenValue) {
          infoPropositionSelect(tokenValue); 
        }
      } 
      catch (e) {
        console.log("erreur de récupération du token ou du rôle");
      }
    };

    chargerRoleEtToken();
  }, []);

  const [proposition, setProposition] = useState<Proposition | null>(null);

  const params = useLocalSearchParams();
  const id = params.id as string

  

  
  const infoPropositionSelect = async (token: string) => {
    if (!token) {
      alert("Impossible d'afficher les propositon");
      return;
    }
    try {
      console.log("iddddd", id)
      
      // appel du fichier propoAjoutService pour recuperer la proposition en focntion de son id
      const reponse = await getPropositionByID(token, Number(id));

      // affichage des données
      console.log("Données reçues:", reponse);
      
      setProposition({
        id: String(reponse.id),
        description: reponse.description,
        photo: reponse.photo,
        mail_utilisateur: String(reponse.mail_utilisateur),
        date_creation: String(reponse.date_creation),
        latitude: reponse.latitude,
        longitude: reponse.longitude

      });

  } catch (error) {
    console.error("Erreur lors du chargement des propositions :", error);
    Alert.alert("Erreur", "Impossible de récupérer les propositions d'ajouts de points.");
  }
  };



  // alerte rejeter proposition
  const confirmerRejet = () => {
    Alert.alert(
    "Rejeter la proposition ?",
    undefined,
    [
        {
        text: "Non", style: "cancel" },
        {
        text: "Oui", onPress: () => {suprimmerProposition()},
        },
    ]
    );
  };

  // Supprime la proposition
  const suprimmerProposition = async () => {

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification de l'id à envoyer pour supprimer\n");
    console.log("IDPoint:", proposition?.id);

    if (!token) {
      Alert.alert("Erreur, impossible de supprimer la proposition");
      return;
    }
    try {
        
      // apelle du fichier propoAjoutService pour supprimer la proposition via son id
      await deleteProposition(token, Number(proposition?.id));

        
      router.push({
          pathname: '/succes',
          params: { title: "Proposition d'ajout supprimé avec succès", page:"point_eau" }
          });
      } catch (error) {
          console.error(error);
          Alert.alert("Erreur", "Suppression proposition");
      }
    };



  // alert confirmer signalement utilisateur
  const confirmeSupp = () => {
    Alert.alert(
    "Faux signalement ?",
    "Confirmer le signalement de l'utilisateur et donc bannissement de 3 jours",
    [
        {
        text: "Non", style: "cancel" },
        {
        text: "Oui", onPress: () => {signalerUtilisateur()},
        },
    ]
    );
  };

  // Signale utilisateur + supp la proposition
  const signalerUtilisateur = async () => {

    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification des info à envoyer pour supprimer\n");
    // console.log("ID:", signalement?.id_point);

    if (!token) {
      Alert.alert("Erreur, impossible de signaler l'utilisateur");
      return;
    }
    if(proposition?.mail_utilisateur == null){
      Alert.alert("Erreur, impossible de signaler l'utilisateur");
      return;
    }
    try {
        
      // apelle du fichier SignalerUtilisateur
      await CreatesignalerUtilisateur(token, proposition?.mail_utilisateur, "proposition" , Number(proposition?.id));

        
      router.push({
          pathname: '/succes',
          params: { title: 'Utilisateur signalé avec succès', page:"point_eau" }
          });
      } catch (error) {
          console.error(error);
          Alert.alert("Erreur", "Signalement utilisateur");
      }
    };



  return (

    <>

      <View>
        <HautPage title="Info propostion ajout de points" />
      </View>
      
      <ScrollView contentContainerStyle={[styles.contenue, { paddingBottom: 80 }]} keyboardShouldPersistTaps="handled">
        <View style={styles.container}>
            <TouchableOpacity style={[{width: 150, height: 45, alignSelf: 'flex-start' }]} onPress={() => {if (userRole) naviguerPointEau(userRole); else alert("Rôle utilisateur introuvable"); }}>
                <Text style={{color:'#000', fontWeight:'bold', fontSize:22}}>&lt; Retour</Text>
            </TouchableOpacity>

          <View style={styles.card}>
            <Text style={styles.titre}>Proposition ajout de point</Text>
              

            {/* Infos */}
            <View style={{ gap: 10 }}>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID : </Text>{proposition?.id}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date de la proposition : </Text> {proposition?.date_creation ? new Date(proposition.date_creation).toLocaleDateString() : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Heure de la proposition : </Text> {proposition?.date_creation ? new Date(proposition.date_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Proposer par : </Text> {proposition?.mail_utilisateur}</Text>
              <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>déscription : </Text> {proposition?.description}</Text>
              {proposition?.photo && (
                <Image
                  source={{ uri: API_ENDPOINTS.GET_IMAGE_PROPOSITION(proposition.photo) }}
                  style={{ width: 300, height: 250, borderRadius: 10, marginTop: 10, marginBottom:10 }}
                  resizeMode="cover"
                />
              )}
            </View>

            
            {/* BOUTONS */}
            <View style={{ flexDirection: 'column', alignItems: 'center', gap: 20, marginTop: 20 }}>

            {/* Afficher le lieu */}
            <ButtonLog
                label="Afficher le lieu"
                onPress={() => {
                const latitude = proposition?.latitude;
                const longitude = proposition?.longitude;
                if (!latitude || !longitude) return alert("Coordonnées non disponibles");

                const url = Platform.OS === "ios"
                    ? `http://maps.apple.com/?daddr=${latitude},${longitude}&dirflg=d`
                    : `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`;

                Linking.openURL(url).catch((err) =>
                    console.error("Impossible d'ouvrir l'application", err)
                );
                }}
                type="primary"
                width={300}
                height={60}
            />


            {/* Signaler utilisateur */}
          <View style={{ marginVertical: 20 }}>
            <TouchableOpacity style={styles.signalerUtilisateur} onPress={async () => confirmeSupp()}>
              <Text style={{ color: '#fff', fontSize: 18, fontWeight: 'bold' }}>
                Signaler l'utilisateur
              </Text>
            </TouchableOpacity>
          </View>


            {/* Rejeter et Créer */}
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', width: 300, gap: 15 }}>
                
                <ButtonLog
                label="Rejeter"
                onPress={() => confirmerRejet()}
                type="primary"
                width={140}
                height={60}
                />

                <ButtonLog
                label="Créer un point"
                onPress={() => router.push({ pathname: '/creerPoint', params: { latitude: proposition?.latitude, longitude: proposition?.longitude, supp: "True", id_supp: proposition?.id}})}
                type="primary"
                width={140}
                height={60}
                />

            </View>

            </View>


          </View>
        </View>
        </ScrollView>
    </>
  );
}

// Style
const styles = StyleSheet.create({
  contenue: {
    marginTop: 40,
    
    alignItems: 'center',
    justifyContent: 'center',
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  },
  card: {
    width: '90%',      
    height: '100%',      
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,     
    justifyContent: 'space-between'
  },
  titre: {
    textAlign: "center",
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 15
  },
  signalerUtilisateur: {
    backgroundColor: '#FF9500',
    width: '100%',
    height: 50,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  }
});

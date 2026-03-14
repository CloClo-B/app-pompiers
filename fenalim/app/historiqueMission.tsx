import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, Alert, Platform, Linking, TouchableHighlight } from 'react-native';
import {useRouter } from 'expo-router';
import { getAllMissions, deleteMissionById } from '@/service/MissionService';
import { getToken } from '@/service/infosStocker';

// Donnée de la Mission
const info = require('@/assets/images/information.png');
type MissionAvecPoint = {
  id_mission: string;
  nom_mission: string;
  date_fin: string;
  date_creation: string;

};

// Affichage des Historique de Missions qui on été terminer
export default function historiqueMission() {

  const [mission, seetMission] = useState<MissionAvecPoint[]>([]);

  const router = useRouter();

  const [token, setToken] = useState<string | null>(null);
  
  // récupérer le token 
  useEffect(() => {
    getData();
  }, []);
  const getData = async () => {
    try {
      const value = await getToken();
      if(value !== null) {
        setToken(value);
        fetchMissions(value);
      }
    } catch(e) {
      console.log("erreur token affichage point eau signaler");
    }
  }

  // afficher la mission a supprimer
  const appuieLongSupp = (nomMisson : string, id: string) => {
    Alert.alert(
    "Supprimer la mission ?",
    "Nom de la mission: "+ nomMisson,
    [
        {
        text: "Non", style: "cancel" },
        {
        text: "Oui", onPress: async () => {confirmeSupp(nomMisson, id)},
        },
    ]
    );
  };
  // confirmer suppression DÉFINITIVE
  const confirmeSupp = (nomMisson : string, id: string) => {
    Alert.alert(
    "Confirmer la suppression définitive de la mission: " + nomMisson,
    "",
    [
        {
        text: "Non", style: "cancel" },
        {
        text: "Oui", onPress: async () => {supprimerMission(id)},
        },
    ]
    );
  };


  // calculer la durée total de la mission
  const calculerDuree = (dateDebut: string, dateFin: string) => {
    const debut = new Date(dateDebut).getTime();
    const fin = new Date(dateFin).getTime();

    const diffMs = fin - debut;
    const diffHeures = Math.floor(diffMs / (1000 * 60 * 60));
    const jours = Math.floor(diffHeures / 24);
    const heures = diffHeures % 24;
    const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

    if (jours > 0) {
      return `${jours} j ${heures} h ${minutes} m`;
    }
    return `${heures} h ${minutes} m`;
  };



  // Affiche sous forme de tableau
  const renderItem = ({ item }: { item: MissionAvecPoint }) => (
    <View >
      <TouchableHighlight onLongPress={() => appuieLongSupp(item.nom_mission, item.id_mission)}  underlayColor="white">
        <View style={styles.row}>
          <Text style={styles.cell}>{item.nom_mission.length > 7 ? item.nom_mission.slice(0, 7) + ' ...' : item.nom_mission}</Text>
          <Text style={styles.cell}>{item?.date_creation ? new Date(item.date_creation).toLocaleDateString() : ''}</Text>
          <Text style={styles.cell}>    {item.date_fin ? calculerDuree(item.date_creation, item.date_fin): ''}</Text>
          <TouchableOpacity onPress={() => router.push({ pathname: '/infoMissionTerminer', params: { id_m: item.id_mission } })}>
            <Image source={info} style={styles.cellImage} />
          </TouchableOpacity>
        </View>
      </TouchableHighlight>
    
    </View>
  );
  

  // Récupère les données des Missions
  const fetchMissions = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible d'afficher l'historique des mission");
      return;
    }
    else{
      console.log(token);
    }
    try {

    // appel du fichier missionService pour la recuperer les données
      const responseMission = await getAllMissions(token);
  
      // affichage des données
      console.log("Données reçues:", responseMission);
      
      const MissionsRaw = Array.isArray(responseMission) ? responseMission : responseMission.missions;
      
      if (!MissionsRaw) {
        console.error("Impossible de récupérer l'historique des missions :", responseMission);
        return;
      }

      const lesMissions: MissionAvecPoint[] = MissionsRaw.filter((u: any) => u.statut === "TERMINER").map((u: any) => ({
          id_mission: String(u.id_mission),
          nom_mission: u.nom_mission,
          date_creation: u.date_creation,
          date_fin: u.date_fin,
        })
      );
    
    seetMission(lesMissions);
    
  } catch (error) {
      console.error("Erreur lors du chargement de l'historique des missions :", error);
      Alert.alert("Erreur", "Impossible de récupérer l'historique des missions");
    }
  };

  // Supprimer une mission
  const supprimerMission = async (id_mission : string) => {
    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification de l'id à envoyer pour supprimer\n");
    console.log("Id mission: ",id_mission);
    if (!token) {
      Alert.alert("Erreur", "Supression impossible");
      return;
    }
    try {
    // apelle du fichier missionService pour la supression
    await deleteMissionById(token, Number(id_mission));
    
    router.push({
        pathname: '/succes',
        params: { title: 'Mission supprimée avec succès', page:"missions" }
        });
    } catch (error) {
        console.error(error);
        alert('Erreur lors de la suppression de la mission');
    }
  };


  return (
    <>    

    
    <View style={styles.container}>

    <View style={styles.hautBleu}>
      <Text style={styles.textTitre}>Nom</Text>
      <Text style={styles.textTitre}>Début</Text>
      <Text style={styles.textTitre}>Durée</Text>
      <Text style={styles.textTitre}>Info</Text>
    </View> 


      <View style={styles.tableContainer}>
        <FlatList
          data={mission}
          renderItem={renderItem}
          keyExtractor={(item) => item.id_mission}
        />
      </View>

    </View>
    </>
  );
}

// Style
const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 3,
  },
  tableContainer: { 
    width: 345, 
    height: 365, 
    borderWidth: 1, 
    borderColor: '#ccc', 
    marginTop: 8 
  },
  row: { 
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row', 
    padding: 15, 
    borderBottomWidth: 1, 
    borderBottomColor: '#eee' 
  },
  cell: { 
    flex: 1,
    textAlign: 'center',
    justifyContent: 'center',
    alignItems: 'center'
  },
  cellImage: { 
    width: 25, 
    height: 25 
  },
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

  textTitre:{
    color: '#ffffff',
    fontSize: 17,
  },

});
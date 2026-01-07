import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Alert, Platform, Linking, TouchableHighlight } from 'react-native';
import {useRouter } from 'expo-router';
import axios from 'axios';
import proj4 from "proj4";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_ENDPOINTS } from '@/config/api';


type MissionAvecPoint = {
  id_mission: string;
  id_point: string;
  nom_mission: string;
  commentaire: string;
  date_creation: string;
  address:string;
  latitude: number;
  longitude: number;
};

export default function MissionEnCours() {
  const [chargement, setChargement] = useState(false);
  const [missions, setMissions] = useState<MissionAvecPoint[]>([]);

  const router = useRouter();
  
  const [token, setToken] = useState<string | null>(null);
  
  // récupérer le token 
  useEffect(() => {
    getData();
  }, []);
  const getData = async () => {
    try {
      const value = await AsyncStorage.getItem('@token')
      if(value !== null) {
        setToken(value);
        fetchMissions(value);
      }
    } catch(e) {
      console.log("erreur token affichage point eau signaler");
    }
  }


  // alerte terminer mission
  const appuieLongSupp = (nomMission : string, id: string) => {
    Alert.alert(
    "Mission terminé ?",
    "Nom de la mission: "+ nomMission,
    [
        {
        text: "Non", style: "cancel" },
        {
        text: "Oui", onPress: () => {confirmeSupp(nomMission, id)},
        },
    ]
    );
  };
  // alert confirmer terminer mission
  const confirmeSupp = (nomMission : string, id: string) => {
    Alert.alert(
    "Confirmer la fin de la mission: " + nomMission,
    "",
    [
        {
        text: "Non", style: "cancel" },
        {
        text: "Oui", onPress: () => {terminerMission(id)},
        },
    ]
    );
  };

  // afficher toute les infos mission
  const infoMission = (nomMission : string, commentaire: string, adr : string, latitude:number, longitude: number ) => {
    Alert.alert(
    "Mission",
    `NOM MISSION:\n${nomMission}\n\nINFORMATIONS:\n${commentaire}\n\nADRESSE:\n${adr}`,
    [
      {
        text: "Fermer", style: "cancel" ,
      },
      {
        text: "Lancer", onPress: async () => {lancerMission(latitude, longitude)},
      },
    ]
    );
  };


  //lancer une mission avec itinairaire
    const lancerMission = (latitude : number, longitude: number) => {
      let url = "";
      if (Platform.OS === "ios") {
        // Apple Maps
        url = `http://maps.apple.com/?daddr=${latitude},${longitude}&dirflg=d`;
      } else {
        // Android / Google Maps
        url = `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`;
      }
      Linking.openURL(url).catch((err) =>
        console.error("Impossible d'ouvrir l'application de navigation", err)
      );
    };


  // affichage des infos en tableau
  const renderItem = ({ item }: { item: MissionAvecPoint }) => (
    <View >
      <TouchableHighlight 
      onLongPress={() => appuieLongSupp(item.nom_mission, item.id_mission)} 
      onPress={() => infoMission(item.nom_mission, item.commentaire, item.address, item.latitude, item.longitude)}  underlayColor="white"
      >
        <View style={styles.row}>
          <Text style={styles.cell}>{item.nom_mission.length > 7 ? item.nom_mission.slice(0, 7) + ' ...' : item.nom_mission}</Text>
          <Text style={styles.cell}>{item.commentaire.length > 9 ? item.commentaire.slice(0, 9) + ' ...' : item.commentaire}</Text>
          <Text style={styles.cell}>{item?.date_creation ? new Date(item.date_creation).toLocaleDateString() : ''}</Text>
          <TouchableOpacity
            style={styles.vert}
            onPress={() => {lancerMission(item.latitude, item.longitude)}}
          >
            <Text style={{ color: '#FFF'}}>Lancer</Text>
          </TouchableOpacity>
        </View>
      </TouchableHighlight>
    
    </View>
  );
  

const fetchMissions = async (token: string) => {
  if (!token) {
    alert("Token manquant, impossible d'afficher les missions en cours");
    return;
  }
  if (chargement) return;
    setChargement(true);
  try {
    const responseMission = await axios.get(API_ENDPOINTS.MISSIONS, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const MissionsRaw = Array.isArray(responseMission.data) ? responseMission.data : responseMission.data.missions;
    if (!MissionsRaw) {
      console.error("Impossible de récupérer les missions:", responseMission.data);
      return;
    }

    const lambert93 = "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs";
    const wgs84 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs";

    const lesMissions: MissionAvecPoint[] = [];

    for (const u of MissionsRaw.filter((m: any) => m.statut === "EN COURS")) {
      // Appel séquentiel pour chaque point
      const responsePoint = await axios.get(API_ENDPOINTS.POINT_EAU_BY_ID(u.id_point));
      const point = responsePoint.data;

      let latitude = 0;
      let longitude = 0;

      if (point) {
        [longitude, latitude] = proj4(lambert93, wgs84, [point.longitude, point.latitude]);
      }

      lesMissions.push({
        id_mission: String(u.id_mission),
        id_point: String(u.id_point),
        nom_mission: u.nom_mission,
        commentaire: u.commentaire,
        date_creation: u.date_creation,
        address: u.itineraire,
        latitude,
        longitude,
      });
    }

    setMissions(lesMissions);
  } catch (error) {
    console.error("Erreur lors du chargement des missions :", error);
    Alert.alert("Erreur", "Impossible de récupérer les missions.");
  }finally {
    setChargement(false);
  }
};


  const terminerMission = async (id_mission : string) => {
    // Avant l'appel API, pour vérifier les valeurs
    console.log("Vérification de l'id à envoyer pour update\n");
    console.log("Id mission: ",id_mission);

    try {
    
      const response = await axios.put(API_ENDPOINTS.MISSION_UPDATE(Number(id_mission)), {
        statut: "TERMINER",
        date_fin: new Date().toISOString(),
      },
      {headers: {
        Authorization: `Bearer ${token}`,
      }}    
    );
    
    router.push({
        pathname: '/succes',
        params: { title: 'Mission terminé avec succès', page:"missions" }
        });
    } catch (error) {
        console.error(error);
        alert('Erreur lors de la fin de la mission');
    }
  };


  return (
    <>    

    
    <View style={styles.container}>

    <View style={styles.hautBleu}>
      <Text style={styles.textTittre}>Nom</Text>
      <Text style={styles.textTittre}>Commentaire</Text>
      <Text style={styles.textTittre}>Date</Text>
      <Text style={styles.textTittre}>Partir</Text>
    </View>


      <View style={styles.tableContainer}>
        <FlatList
          data={missions}
          renderItem={renderItem}
          keyExtractor={(item) => item.id_mission}
        />
      </View>

    </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center'
  },
  vert:{
    backgroundColor:'#4CAF50',
    paddingHorizontal: 5,
    paddingVertical:2,
    borderRadius:10,
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
    flexDirection: 'row', 
    padding: 15, 
    borderBottomWidth: 1, 
    borderBottomColor: '#eee',
    marginBottom:2, 
  },
  cell: { 
    flex: 1 
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
  textTittre:{
    color: '#ffffff',
    fontSize: 17,
  },
});
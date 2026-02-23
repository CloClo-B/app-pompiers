import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, Alert, Pressable, ScrollView, TextInput } from 'react-native';
import HautPage from '@/app/hautPage';
import {useRouter } from 'expo-router';
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';
import { getToken } from '@/service/infosStocker';

const roue = require('@/assets/images/parametres.png');

// Modèle de données pour un Utilisateur
type User = {
  id: string;
  nom: string;
  prenom: string;
  role: string;
};


export default function HomeScreen() {
  const [recherche, setRecherche] = useState(''); 

  // boolean utiliser pour changer les couleurs des boutons + changer les valeurs du tableau 
  const [tout, setTout] = useState(true);
  const [publicR, setPublicR] = useState(false);
  const [pompier, setPompier] = useState(false);
  const [commandement, setCommandement] = useState(false);
  const [admin, setAdmin] = useState(false);
  const [choixRole, setChoixRole] = useState<string[]>(["public", "pompier", "commandement", "admin"]);

  useEffect(() => {
    getData();
  },[]);
  
  // récupérer le token 
  const getData = async () => {
    try {
      const value = await getToken();
      if(value !== null) {
        fetchUtilisateurs(value);
      }
    } catch(e) {
      console.log("erreur token affichage utilisateur");
    }
  }

  const [chargement, setChargement] = useState(true);
  const [utilisateur, setUtilisateur] = useState<User[]>([]);
  
  const router = useRouter();
  
  // Définit comment afficher chaque utilisateur dans la liste
  const renderItem = ({ item }: { item: User }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.nom}</Text>
      <Text style={styles.cell}>{item.prenom}</Text>
      <Text style={styles.cell}>{item.role}</Text>
      <TouchableOpacity onPress={() => router.push({ pathname: '/infoUtilisateur', params: { id: item.id } })}>
        <Image source={roue} style={styles.cellImage} />
      </TouchableOpacity>
    </View>
  );
  
  // Récupère liste des users
  const fetchUtilisateurs = async (token: string) => {
    if (!token) {
      alert("Token manquant, impossible d'afficher les missions en cours");
      return;
    }
    try {
      const response = await axios.get(API_ENDPOINTS.REGISTER, {
      headers: { Authorization: `Bearer ${token}` },
    });
      // affichage des données
      console.log("Données reçues:", response.data);
      
      const UtilisateurRaw = Array.isArray(response.data) ? response.data : response.data.utilisateurs;

      if (!UtilisateurRaw) {
        console.error("Impossible de récupérer les utlisateur:", response.data);
        setChargement(false);
        return;
      }
    
    // Mis en forme des Données des Users
    const lesUtilisateurs: User[] = UtilisateurRaw.map((u: any) => ({
      id: String(u.id_utilisateur),
      nom: u.nom,
      prenom: u.prenom,
      role: u.role,
    }));
    
    setUtilisateur(lesUtilisateurs);
  } catch (error) {
      console.error("Erreur lors du chargement des utilisateur :", error);
      Alert.alert("Erreur", "Impossible de récupérer les utilisateurs.");
    } finally {
      setChargement(false);
    }
  };
  

  // gerer les infos afficher en fonction des valeurs de recherche et des rôle
  const utilisateursFiltres = utilisateur.filter(
    u => (recherche === '' ||
    u.nom.toLowerCase().includes(recherche.toLowerCase()) ||
    u.prenom.toLowerCase().includes(recherche.toLowerCase())
    ) && (tout || choixRole.includes(u.role))
  );



  // changement de couleur en focntion du choix de role + actualisation du tableau
  const setChoix = (choix: string) => {
    let newPublic = publicR;
    let newPompier = pompier;
    let newCommandement = commandement;
    let newAdmin = admin;

    if (choix === "tout") {
      newPublic = false;
      newPompier = false;
      newCommandement = false;
      newAdmin = false;
      setTout(true);
    } else {
      setTout(false);

      if (choix === "public") newPublic = !publicR;
      if (choix === "pompier") newPompier = !pompier;
      if (choix === "commandement") newCommandement = !commandement;
      if (choix === "admin") newAdmin = !admin;
    }

    // Mettre à jour les boolean
    setPublicR(newPublic);
    setPompier(newPompier);
    setCommandement(newCommandement);
    setAdmin(newAdmin);

    // tableau a partir des nouveaux boolean
    const newChoixRole: string[] = [];
    if (newPublic) newChoixRole.push("public");
    if (newPompier) newChoixRole.push("pompier");
    if (newCommandement) newChoixRole.push("commandement");
    if (newAdmin) newChoixRole.push("admin");

    // Si tout décocher alors on met tout
    if (newChoixRole.length === 0) setTout(true);

    setChoixRole(newChoixRole);
    console.log(newChoixRole);
  };

  return (
    <>
    <View>
      <HautPage title="Utilisateurs" />
    </View>

    <View style={styles.container}>

    <View>
      <Text style={styles.titre2}>Liste des utilisateurs</Text>
    </View>
    

    {/* filtre recherche utlisateur avec nom ou prénom */}
    <TextInput value={recherche} onChangeText={setRecherche} style={styles.recherche} placeholder="Rechercher un utilisateur" />
    

    {/* filtre en fonction des roles */}
    <View style={styles.filtreR}>  
      {/* sroll horizontale  */}
      <ScrollView horizontal showsHorizontalScrollIndicator={true} style={styles.scrollHorizontal} contentContainerStyle={styles.espaceLaBar} >

        {/* différents choix possibles  */}
        <Pressable style={[styles.ListeR, tout ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => setChoix("tout")}>
          <Text style={tout ? styles.txtActif : styles.txtInactif}>Tout</Text>
        </Pressable>
        <Pressable style={[styles.ListeR, publicR ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => setChoix("public")}>
          <Text style={publicR ? styles.txtActif : styles.txtInactif}>Public</Text>
        </Pressable>
            <Pressable style={[styles.ListeR, pompier ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => setChoix("pompier")}>
          <Text style={pompier ? styles.txtActif : styles.txtInactif}>Pompier</Text>
        </Pressable>
            <Pressable style={[styles.ListeR, commandement ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => setChoix("commandement")}>
          <Text style={commandement ? styles.txtActif : styles.txtInactif}>Commandement</Text>
        </Pressable>
            <Pressable style={[styles.ListeR, admin ? styles.bouttonActif : styles.bouttonInactif]} onPress={() => setChoix("admin")}>
          <Text style={admin ? styles.txtActif : styles.txtInactif}>Admin</Text>
        </Pressable>
      </ScrollView>
    </View>



      {/* En-téte du tableau */}
      <View style={styles.hautBleu}>
        <Text style={styles.textTittre}>Nom</Text>
        <Text style={styles.textTittre}>Prénom</Text>
        <Text style={styles.textTittre}>Rôle</Text>
        <Text style={styles.textTittre}>info</Text>
      </View>

      {/* Liste déroulante*/}
      <View style={styles.tableContainer}>
        <FlatList
          data={utilisateursFiltres}
          renderItem={renderItem}
          keyExtractor={(item) => item.id}
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
  header: { 
    flexDirection: 'row', 
    backgroundColor: '#3498db', 
    padding: 8 
  },
  headerCell: { 
    flex: 1, 
    color: 'white', 
    fontWeight: 'bold' 
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
    borderBottomColor: '#eee' 
  },
  cell: { 
    flex: 1 
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
  textTittre:{
    color: '#ffffff',
    fontSize: 17,
  },
  titre2: {
    textAlign: 'center',
    color: '#1D3557',
    fontSize: 25,
    marginBottom: 20,
  },

  scrollHorizontal:{
    width: '100%',
    paddingHorizontal:15,
  },
  
  
  
  // filtre
  espaceLaBar: {
    paddingBottom: 18, 
    alignItems: 'center',
  },
  recherche: {
    width: '100%',
    height: 45,
    backgroundColor: '#D4D4D4',
    paddingHorizontal: 10,
    marginBottom:15,
    borderRadius: 30,
  },
  filtreR:{
    flexDirection: 'row',
    paddingBottom:10,
  },
  ListeR:{
    marginHorizontal:5,
    paddingHorizontal: 7,
    paddingVertical: 5,
    borderRadius: 20,
  },
  /* couleurs bouton état */
  bouttonActif:{
    backgroundColor: '#1D3557',
  },

  bouttonInactif:{
    backgroundColor: '#E7E7E7',
  },

  /* texte */
  txtActif:{
    color: '#ffffff',
  },
  txtInactif:{
    color: '#1D3557',
  }


});
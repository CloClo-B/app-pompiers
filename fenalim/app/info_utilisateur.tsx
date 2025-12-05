import React from "react";
import { View, Text, StyleSheet, Button, TouchableOpacity } from "react-native";
import HautPage from './hautPage';

export default function UserDetails() {
  return (

    <>

      <View>
        <HautPage title="Utilisateurs" />
      </View>
      
      
      <View style={styles.container}>

        <View>
          <Text style={styles.titre2}>Liste des utilisateurs de l'application</Text>
        </View>

        <View style={styles.card}>

          {/* Card de l'utilisateur */}
          <Text style={styles.titre}>Jean Dupont</Text>

          {/* Infos exemple en statique*/}
          <View style={{ gap: 10 }}>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>ID :</Text> 12345</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Rôle :</Text> Administrateur</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Email :</Text> jean.dupont@test.com</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Dernière connexion :</Text> 02/12/2025</Text>
            <Text><Text style={{ fontWeight:'bold', fontSize: 18 }}>Date de création :</Text> 14/07/2024</Text>
          </View>

          
          {/* BOUTONS */}
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 10 }}>
            <TouchableOpacity style={[styles.boutton, { backgroundColor: '#457B9D', width: 150, height: 45 }]}>
                <Text style={{color:'#ffffff'}}>FERMER</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.boutton, { backgroundColor: '#457B9D', width: 150, height: 45 }]}>
                <Text style={{color:'#ffffff'}}>APPLIQUER</Text>
            </TouchableOpacity>
          </View>


        </View>
      </View>

    </>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  },
  card: {
    width: 340,      
    height: 370,      
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
  infoBloc: {
    gap: 13,
  },
  btnRow: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 15
  },
  btn: {
    flex: 1
  },
  tout:{
    alignSelf: 'center',
    alignItems: "center",
    marginTop: 20,
  },
  boutton:{
    justifyContent: 'center',
    alignItems: 'center',    
    borderRadius: 30,
  },
  titre2: {
    textAlign: 'center',
    color: '#1D3557',
    fontSize: 25,
    marginBottom: 30,
  }
});
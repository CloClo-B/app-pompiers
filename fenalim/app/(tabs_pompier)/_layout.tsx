import { Image, StyleSheet } from 'react-native';

import { Tabs } from 'expo-router';
import React from 'react';

import { HapticTab } from '@/components/haptic-tab';
import { useColorScheme } from '@/hooks/use-color-scheme';

// attention à bien mettre le même nom de fichier que ici sinon erreur

export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        
        tabBarActiveTintColor: '#ffffff', // couleur actif
        tabBarInactiveTintColor: '#B0B0B0', // couleur inactif
        headerShown: false,
        tabBarButton: HapticTab,
        
        //Couleur de fond
        tabBarStyle: {
          backgroundColor: '#1D3557',
          //  height:75,  //  hauteur de la barre pas obligé à voir par la suite
        },

        //taille du texte
        tabBarLabelStyle: {
          fontSize: 9,
          fontWeight: '600',
          textAlign: 'center', 
        },
      }}>


      <Tabs.Screen
        name="acceuil_pompier"
        options={{
          title: 'ACCUEIL',
          tabBarIcon: ({ focused }) => (
            <Image
              source={require('@/assets/images/maison.png')}
              style={styles.taille_images}
              resizeMode="contain"
            />
          ),
        }}
      />
        <Tabs.Screen
         name="point_eau"
         options={{
           title: "POINT D'EAU",
           tabBarIcon: ({ focused }) => (
             <Image
               source={require('@/assets/images/bouche_incendie.png')}
              style={styles.taille_images}
               resizeMode="contain"
             />
           ),
         }}
       />
       <Tabs.Screen
        name="mission"
        options={{
          title: 'MISSION',
          tabBarIcon: ({ focused }) => (
            <Image
              source={require('@/assets/images/epingle_mission.png')}
              style={styles.taille_images}
              resizeMode="contain"
            />
          ),
        }}
      />
      <Tabs.Screen
        name="compte"
        options={{
          title: 'MON COMPTE',
          tabBarIcon: ({ focused }) => (
            <Image
              source={require('@/assets/images/mon_compte.png')}
              style={styles.taille_images}
              resizeMode="contain"
            />
          ),
        }}
      />
    </Tabs>
  );
}

const styles = StyleSheet.create({

  taille_images: {
    width: 25,
    height: 25,
  },
});
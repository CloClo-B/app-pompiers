import { router } from 'expo-router';

// Ces fonctions servent à rediriger automatiquement l'utilisateur vers la bonne page en fonction de son role (admin, pompier, commandement, admin)

// Envoie vers les points d'eau
export const naviguerPointEau = (role: string) => {
  switch(role) {
    case 'admin':
      router.navigate('/(tabs_admin)/point_eau');
      break;
    case 'commandement':
      router.navigate('/(tabs_commandement)/point_eau');
      break;
    case 'pompier':
      router.navigate('/(tabs_pompier)/point_eau');
      break;
    case 'public':
      router.navigate('/(tabs_public)/acceuil');
      break;
  }
};

// Envoie vers les missions
export const naviguerMission = (role: string) => {
  switch(role) {
    case 'admin':
      router.navigate('/(tabs_admin)/mission');
      break;
    case 'commandement':
      router.navigate('/(tabs_commandement)/mission');
      break;
    case 'pompier':
      router.navigate('/(tabs_pompier)/mission');
      break;
  }
};

// Envoie vers la page d'accueil
export const naviguerAccueil = (role: string) => {
  switch(role) {
    case 'admin':
      router.navigate('/(tabs_admin)/acceuil_admin');
      break;
    case 'commandement':
      router.navigate('/(tabs_commandement)/acceuil_commandement');
      break;
    case 'pompier':
      router.navigate('/(tabs_pompier)/acceuil_pompier');
      break;
    case 'public':
      router.navigate('/(tabs_public)/acceuil');
    break;
  }
};

import { router } from 'expo-router';

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

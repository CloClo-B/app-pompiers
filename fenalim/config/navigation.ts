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
    case 'pompier':
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
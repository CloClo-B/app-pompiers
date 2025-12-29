import AsyncStorage from "@react-native-async-storage/async-storage";


export const getData = async () => {
  try {
    const value = await AsyncStorage.getItem('@role');
    if (value !== null) {
      return value;
    }
    return null;
  } catch (e) {
    console.log("erreur token affichage utilisateur");
    return null;
  }
};

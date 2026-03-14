import AsyncStorage from "@react-native-async-storage/async-storage";


// Cette fonction enregistre le token de l'utilisateur dans la mémoire du téléphone
export const setToken = async (token: string) => {
  try {
    await AsyncStorage.setItem('@token', token)
  } catch (e) {
    console.log("erreur stockage token")
  }
};

// Cette fonction enregistre le rôle de l'utilisateur dans la mémoire du téléphone
export const setRole = async (role: string) => {
  try {
    await AsyncStorage.setItem('@role', role)
  } catch (e) {
    console.log("erreur stockage tole")
  }
};


// Cette fonction récupère le rôle de l'utilisateur qui a été enregistré dans la mémoire du téléphone
export const getRole = async () => {
  try {
    const value = await AsyncStorage.getItem('@role');
    if (value !== null) {
      return value;
    }
    return null;
  } catch (e) {
    console.log("erreur utilisateur");
    return null;
  }
};


// Cette fonction récupère le token de l'utilisateur qui a été enregistré dans la mémoire du téléphone
export const getToken = async () => {
  try {
    const value = await AsyncStorage.getItem('@token');
    if (value !== null) {
      return value;
    }
    return null;
  } catch (e) {
    console.log("erreur utilisateur");
    return null;
  }
};

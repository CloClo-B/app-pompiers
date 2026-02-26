import axios from "axios";
// permet de savoir le role d'un utilisateur pour naviguer
export const getUserInfo = async (token: string) => {
  console.log("getUserInfo appelé avec token :", token);
  try {
    const response = await axios.get("http://192.168.1.178:8000/utilisateurs/infoRole", {
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log("Réponse /infoRole :", response.data.role);

    return response.data.role; 
  } catch (error) {
    console.error("Erreur lors de la récupération de l'utilisateur :", error);
    return null;
  }
};

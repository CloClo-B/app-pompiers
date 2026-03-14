// fichier qui centralise les requetes pour les signalements
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';

// creer un nouveau signalement avec les donée recu dans le formdata
export const createSignalement = async (token: string, formData: FormData) => {
    const reponse = await axios.post(API_ENDPOINTS.SIGNALEMENTS, formData, {
        headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
        }
    });
};

// renvoie tout les signalement
export const getAllSignalement = async (token: string) => {
    const reponse = await axios.get(API_ENDPOINTS.SIGNALEMENTS, {
    headers: {
        Authorization: `Bearer ${token}`,
    },
    });
  return reponse.data;
};

// renvoie un signalemente en fonction de l'index dans le tableau
export const getSignalementByIndex = async (token: string, id_s: string) => {
      const reponse = await axios.get(API_ENDPOINTS.SIGNALEMENT_BY_ID_SIGNALEMENT(id_s), {
        headers: { Authorization: `Bearer ${token}` },
      });
  return reponse.data;
};

// supprime un signalement par son ID
export const deleteSignalement = async (token: string , id_point:string) => {
      const reponse = await axios.delete(API_ENDPOINTS.SIGNALEMENT_SUPPRIMER(id_point), {
        headers: { Authorization: `Bearer ${token}` },
      });
};
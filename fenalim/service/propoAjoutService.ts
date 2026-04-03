// fichier qui centralise les requetes pour les propositions d'ajoute de point d'eau
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';

// creer une nouvelle proposition avec les donée recu dans le formdata
export const createProposition = async (token: string, formData: FormData) => {
    const reponse = await axios.post(API_ENDPOINTS.PROPOSITIONAJOUT, formData, {
        headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
        }
    });
};

// renvoie tout les propositions
export const getAllProposition = async (token: string) => {
    const reponse = await axios.get(API_ENDPOINTS.PROPOSITIONAJOUT, {
    headers: {
        Authorization: `Bearer ${token}`,
    },
    });
  return reponse.data;
};

// renvoie tout les propositions avec le minimum d'info pour ne pas surcharger le reseau
export const getAllPropositionMin = async (token: string) => {
    const reponse = await axios.get(API_ENDPOINTS.PROPOSITIONAJOUTMIN, {
    headers: {
        Authorization: `Bearer ${token}`,
    },
    });
  return reponse.data;
};

// renvoie une proposition en fonction de l'index dans le tableau
export const getPropositionByID = async (token: string, id: number) => {
      const reponse = await axios.get(API_ENDPOINTS.PROPOSITION_BY_ID(id), {
        headers: { Authorization: `Bearer ${token}` },
      });
  return reponse.data;
};

// supprime une proposition par son ID
export const deleteProposition = async (token: string , id_point:number) => {
      const reponse = await axios.delete(API_ENDPOINTS.PROPOSITION_SUPPRIMER(id_point), {
        headers: { Authorization: `Bearer ${token}` },
      });
};
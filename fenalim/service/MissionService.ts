// fichier qui centralise les requetes pour les missions
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';


// renvoie toutes les missions
export const getAllMissions = async (token: string) => {
    const reponse = await axios.get(API_ENDPOINTS.MISSIONS, {
        headers: { Authorization: `Bearer ${token}` },
    });
  return reponse.data;
};


// creer une nouvelle mission
export const CreateMission = async (token: string, nomMission: string, IDPoint:string, commentaire: string, itineraire : string) => {
    const reponse = await axios.post(API_ENDPOINTS.MISSIONS, {
        nom_mission: nomMission,        
        id_point: parseInt(IDPoint),
        commentaire: commentaire, 
        itineraire: itineraire,

    },
    {
        headers: {Authorization: `Bearer ${token}`,},
    });
  return reponse.data;
};


// supprimme une mission via son ID
export const deleteMissionById = async (token: string, id_mission: number) => {
      const reponse = await axios.delete(API_ENDPOINTS.MISSION_DELETE(Number(id_mission)),  {
        headers: { Authorization: `Bearer ${token}` },
    });
};
// récupere une mission via son ID
export const getMissionById = async(token: string, id_m: number) =>{
    const reponse = await axios.get(API_ENDPOINTS.MISSION_BY_ID(id_m), {
        headers: { Authorization: `Bearer ${token}` },
    });
    return reponse.data;
};

// passe une mission à l'etat de terminer 
export const updateMission = async(token: string, id_mission: string) =>{
    const response = await axios.put(API_ENDPOINTS.MISSION_UPDATE(Number(id_mission)), {
    statut: "TERMINER",
    date_fin: new Date().toISOString(),
    },
    {headers: {Authorization: `Bearer ${token}`,}
    });
};
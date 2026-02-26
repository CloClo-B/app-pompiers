// fichier qui centralise les requetes pour les points d'eau
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';



// créer un nouveau point d'eau
export const createPointEau = async (
  token: string,
  numeroPEI: string,
  // nom: string,
  valueStatut: string,
  valueType: string,
  insee5: string,
  valueAcces: string,
  valueDispo: string,
  refCarto: string,
  pression: string,
  debit: string,
  volumeMin: string,
  longitude: string,
  latitude: string,
) => {
  const reponse = await axios.post(API_ENDPOINTS.POINTS_EAU, {
    numero_pei: parseInt(numeroPEI),
    // nom: '',           discuter avec le client pour savoir si réelement nécéssaire
    statut: valueStatut,
    type_nature: valueType,
    insee5: insee5, 
    accessibilite: valueAcces,
    disponibilite: valueDispo,
    carto_ref: parseInt(refCarto)  ? parseInt(refCarto) : null ,
    press_deb: parseFloat(pression.replace(',', '.')),
    debit_1_bar: parseFloat(debit.replace(',', '.')),
    vol_eau_mi: parseFloat(volumeMin.replace(',', '.')),
    longitude: parseFloat(longitude.replace(',', '.')),
    latitude: parseFloat(latitude.replace(',', '.')),
  },
  {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};




// renvoie tout les points d'eau
export const getAllPointEau = async () => {
    const reponse = await axios.get(API_ENDPOINTS.POINTS_EAU);
  return reponse.data;
};

// renvoie les infos d'un point en fonction de son id 
export const getPointEauByID = async (token: string, idPoint: string) => {
    const reponse = await axios.get(API_ENDPOINTS.POINT_EAU_BY_ID(idPoint),
    {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return reponse.data;
};

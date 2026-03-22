// fichier qui centralise les requetes pour les signalements utilisateur
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';



// creer un nouveau signalement utilisateur avec les donée recu
export const CreatesignalerUtilisateur = async(token: string, mail_utilisateur_signal: string, raison: string = "") => {

  const response = await axios.post(API_ENDPOINTS.SIGNALERUTILISATEUR, {
    mail_utilisateur: mail_utilisateur_signal,
    raison: raison
  },
  {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

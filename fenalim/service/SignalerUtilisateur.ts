// fichier qui centralise les requetes pour les signalements utilisateur
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';



// creer un nouveau signalement utilisateur avec les donée recu
export const CreatesignalerUtilisateur = async(token: string, mail_utilisateur_signal: string, signalement_ou_propoition: string, id_s_ou_p: number, raison: string = "") => {

  const response = await axios.post(API_ENDPOINTS.SIGNALERUTILISATEUR, {
    mail_utilisateur: mail_utilisateur_signal,
    raison: raison,
    signalement_ou_propoition: signalement_ou_propoition,
    id_s_ou_p: id_s_ou_p
  },
  {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

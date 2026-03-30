// Fichier de centralisation des URL pour l'application (frontend)

// IP A CHANGER
export const API_URL = 'http://192.168.1.178:8000';


// Liste de tous les points d'accès utilisés par l'application pour accéder a l'API
export const API_ENDPOINTS = {
  LOGIN: `${API_URL}/utilisateurs/login`,
  REGISTER: `${API_URL}/utilisateurs/`,
  LOGOUT: `${API_URL}/utilisateurs/logout`,
  
  GET_UTILISATEUR_MINIMUM: `${API_URL}/utilisateurs/minimum`,
  GET_USER_INFO: `${API_URL}/utilisateurs/me`,
  UPDATE_USER_INFO: `${API_URL}/utilisateurs/me`,
  CHANGE_PASSWORD: `${API_URL}/utilisateurs/me/change-password`,
  DELETE_ACCOUNT: `${API_URL}/utilisateurs/me`,

  USERS_LIST: `${API_URL}/utilisateurs/`,
  USER_BY_ID: (id: number) => `${API_URL}/utilisateurs/${id}`,
  

  POINTS_EAU: `${API_URL}/points-eau/`,
  POINTS_EAU_LIGHT: `${API_URL}/points-eau/light/`,
  POINT_EAU_BY_NUMERO_PEI: (id: string) => `${API_URL}/points-eau/${id}`,
  POINT_EAU_UPDATE: (id: number) => `${API_URL}/points-eau/update/${id}`,


  MISSIONS: `${API_URL}/missions/`,
  MISSION_BY_ID: (id: number) => `${API_URL}/missions/${id}`,
  MISSION_UPDATE: (id: number) => `${API_URL}/missions/update/${id}`,
  MISSION_DELETE: (id: number) => `${API_URL}/missions/supprimer/${id}`,


  SIGNALEMENTS: `${API_URL}/signaler/`,
  SIGNALEMENT_BY_ID_SIGNALEMENT: (id: string) => `${API_URL}/signaler/id_s/${id}`,
  SIGNALEMENT_BY_ID_POINT: (id: string) => `${API_URL}/signaler/id_p/${id}`,
  SIGNALEMENT_BY_ID: (id: string) => `${API_URL}/signaler/${id}`,
  SIGNALEMENT_SUPPRIMER: (id: string) => `${API_URL}/signaler/suprimmer/${id}`,
  GET_IMAGE_SIGNALEMENT: (id: string) => `${API_URL}/${id}`,


  PROPOSITIONAJOUT: `${API_URL}/propositionAjout/`,
  PROPOSITIONAJOUTMIN: `${API_URL}/propositionAjout/getmin`,
  PROPOSITION_BY_ID: (id: number) => `${API_URL}/propositionAjout/id/${id}`,
  PROPOSITION_SUPPRIMER: (id: number) => `${API_URL}/propositionAjout/suprimmer/${id}`,
  GET_IMAGE_PROPOSITION: (id: string) => `${API_URL}/${id}`,


  SIGNALERUTILISATEUR: `${API_URL}/signaler_utilisateur/`,

  

  CAPTCHA: `${API_URL}/submit-form`,
  
  
  HISTORIQUE: `${API_URL}/historiques/`,


};
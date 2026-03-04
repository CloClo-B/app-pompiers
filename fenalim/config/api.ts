// Fichier de centralisation des URL pour l'application (frontend)

// IP A CHANGER
export const API_URL = 'http://192.168.1.19:8000';


// Liste de tous les points d'accès utilisés par l'application pour accéder a l'API
export const API_ENDPOINTS = {
  LOGIN: `${API_URL}/utilisateurs/login`,
  REGISTER: `${API_URL}/utilisateurs/`,
  LOGOUT: `${API_URL}/utilisateurs/logout`,
  
  GET_USER_INFO: `${API_URL}/utilisateurs/me`,
  UPDATE_USER_INFO: `${API_URL}/utilisateurs/me`,
  CHANGE_PASSWORD: `${API_URL}/utilisateurs/me/change-password`,
  DELETE_ACCOUNT: `${API_URL}/utilisateurs/me`,

  USERS_LIST: `${API_URL}/utilisateurs/`,
  USER_BY_ID: (id: number) => `${API_URL}/utilisateurs/${id}`,
  

  POINTS_EAU: `${API_URL}/points-eau/`,
  POINT_EAU_BY_ID: (id: string) => `${API_URL}/points-eau/${id}`,
  

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


  HISTORIQUE: `${API_URL}/historiques/`,


};
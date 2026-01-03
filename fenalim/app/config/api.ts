// Fichier de centralisation des URL pour les fichiers frontend

// IP A CHANGER
export const API_URL = 'http://192.168.2.215:8000';


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
  

  SIGNALEMENTS: `${API_URL}/signaler/`,
  SIGNALEMENT_BY_ID: (id: string) => `${API_URL}/signaler/${id}`,
  
  HISTORIQUE: `${API_URL}/historiques/`,
};
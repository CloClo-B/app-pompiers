import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_ENDPOINTS } from '../config/api';

export interface UserData {
  id_utilisateur: number;
  nom: string;
  prenom: string;
  telephone: string;
  email: string;
  role: 'public' | 'pompier' | 'commandement' | 'admin';
  date_creation: string;
  derniere_connexion?: string;
}

export interface LoginResponse {
  id_utilisateur: number;
  token: string;
  role: string;
}

class AuthService {
  // Sauvegarder le token
  async saveToken(token: string): Promise<void> {
    try {
      await AsyncStorage.setItem('@token', token);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde du token:', error);
      throw error;
    }
  }

  // Récupérer le token
  async getToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem('@token');
    } catch (error) {
      console.error('Erreur lors de la récupération du token:', error);
      return null;
    }
  }

  // Supprimer le token
  async removeToken(): Promise<void> {
    try {
      await AsyncStorage.removeItem('@token');
    } catch (error) {
      console.error('Erreur lors de la suppression du token:', error);
      throw error;
    }
  }

  // Login
  async login(email: string, password: string): Promise<LoginResponse | null> {
    try {
      const response = await fetch(API_ENDPOINTS.LOGIN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          mot_de_passe: password,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erreur de connexion');
      }

      const data: LoginResponse = await response.json();
      await this.saveToken(data.token);
      return data;
    } catch (error) {
      console.error('Erreur login:', error);
      throw error;
    }
  }

  // Récupérer les informations de l'utilisateur
// Dans authService.ts
async getUserInfo(): Promise<UserData | null> {
  try {
    const token = await this.getToken();
    if (!token) return null;

    const response = await fetch(API_ENDPOINTS.GET_USER_INFO, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // AJOUTE CES LOGS POUR VOIR LA VÉRITÉ
      console.log("--- DEBUG API ---");
      console.log("Status:", response.status);
      const text = await response.text(); 
      console.log("Réponse serveur:", text);

      if (response.status === 401) {
        await this.removeToken();
        return null; 
      }
      // On ne "throw" plus, on renvoie null pour laisser l'utilisateur aller au login
      return null; 
    }

    return await response.json();
  } catch (error) {
    console.error('Erreur réseau:', error);
    return null;
  }
}

  // Mettre à jour les informations de l'utilisateur
  async updateUserInfo(data: {
    nom?: string;
    prenom?: string;
    email?: string;
    telephone?: string;
  }): Promise<UserData | null> {
    try {
      const token = await this.getToken();
      if (!token) {
        throw new Error('Aucun token trouvé');
      }

      const response = await fetch(API_ENDPOINTS.UPDATE_USER_INFO, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        if (response.status === 401) {
          await this.removeToken();
          throw new Error('Token expiré');
        }
        const error = await response.json();
        throw new Error(error.detail || 'Erreur lors de la mise à jour');
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur updateUserInfo:', error);
      throw error;
    }
  }

  // Changer le mot de passe
  async changePassword(
    oldPassword: string,
    newPassword: string,
    confirmNewPassword: string
  ): Promise<boolean> {
    try {
      const token = await this.getToken();
      if (!token) {
        throw new Error('Aucun token trouvé');
      }

      const response = await fetch(API_ENDPOINTS.CHANGE_PASSWORD, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          old_password: oldPassword,
          new_password: newPassword,
          confirm_new_password: confirmNewPassword,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erreur lors du changement de mot de passe');
      }

      return true;
    } catch (error) {
      console.error('Erreur changePassword:', error);
      throw error;
    }
  }

  // Se déconnecter
  async logout(userId?: number): Promise<void> {
    try {
      if (userId) {
        const token = await this.getToken();
        if (token) {
          await fetch(API_ENDPOINTS.LOGOUT, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id_utilisateur: userId,
            }),
          });
        }
      }
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    } finally {
      await this.removeToken();
    }
  }

  // Inscription
  async register(userData: {
    nom: string;
    prenom: string;
    email: string;
    telephone: string;
    mot_de_passe: string;
    confirm_password: string;
    role?: string;
  }): Promise<LoginResponse | null> {
    try {
      const response = await fetch(API_ENDPOINTS.REGISTER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erreur lors de l\'inscription');
      }

      const data: LoginResponse = await response.json();
      await this.saveToken(data.token);
      return data;
    } catch (error) {
      console.error('Erreur register:', error);
      throw error;
    }
  }
}

export default new AuthService();
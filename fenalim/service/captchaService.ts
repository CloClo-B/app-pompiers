
// fichier qui centralise les requetes pour le captcha
import axios from 'axios';
import { API_ENDPOINTS } from '@/config/api';

// envoyer le token Turnstile au backend pour validation
export const ValidationCaptcha = async (captchaToken: string) => {
  const formData = new URLSearchParams();
  formData.append("cf-turnstile-response", captchaToken);

  const reponse = await axios.post(`${API_ENDPOINTS.CAPTCHA}`, formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return reponse.data;
};
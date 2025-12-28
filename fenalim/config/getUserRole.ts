import * as SecureStore from 'expo-secure-store';

export async function getUserRole(): Promise<string | null> {
  //  décoder le payload en base64
  function decodeBase64(str: string) {
    return decodeURIComponent(
      Array.prototype.map
        .call(
          Buffer.from(str, 'base64').toString('binary'),
          (c: string) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        )
        .join('')
    );
  }

  const token = await SecureStore.getItemAsync('token');
  if (!token) return null;

  try {
    const payload = JSON.parse(decodeBase64(token.split('.')[1])); 
    return payload.role; //rôle de l'utilisateur
  } catch (e) {
    console.log("Erreur décodage token:", e);
    return null;
  }
}

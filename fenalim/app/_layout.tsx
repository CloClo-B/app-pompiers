import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';
import { SafeAreaView } from 'react-native-safe-area-context';


import { useColorScheme } from '@/hooks/use-color-scheme';

export const unstable_settings = {
  anchor: '(tabs)',
};

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#1D3557' }}>


    {/* 
      gestureEnabled pour eviter de faire retour en arriere en glissant 
      headerShown pour eviter d'avoir la bar en haut qui affiche le retour
    */}
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        <Stack.Screen name="index" options={{ headerShown: false, gestureEnabled: false}} />
        <Stack.Screen name="(tabs_public)" options={{ headerShown: false, gestureEnabled: false}} />
        <Stack.Screen name="(tabs_pompier)" options={{ headerShown: false, gestureEnabled: false}} />
        <Stack.Screen name="(tabs_commandement)" options={{ headerShown: false, gestureEnabled: false}} />
        <Stack.Screen name="(tabs_admin)" options={{ headerShown: false, gestureEnabled: false}} />
        <Stack.Screen name="connexion" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="inscription" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="succes" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="mdp_oublie" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="createurs" options={{ headerShown: false, gestureEnabled: false }} />
        
        <Stack.Screen name="infoUtilisateur" options={{ headerShown: false }} />
        <Stack.Screen name="infoSignalement" options={{ headerShown: false}} />
        <Stack.Screen name="marquerResolu" options={{ headerShown: false}} />
        <Stack.Screen name="infoMissionTerminer" options={{ headerShown: false}} />
        <Stack.Screen name="creerSignalement" options={{ headerShown: false }} />
        <Stack.Screen name="creerMissionCarte" options={{ headerShown: false }} />
        <Stack.Screen name="UpdatePointEau" options={{ headerShown: false }} />
        <Stack.Screen name="creerPropositionAjout" options={{ headerShown: false }} />
        <Stack.Screen name="infoProposition" options={{ headerShown: false }} />
        <Stack.Screen name="creerPoint" options={{ headerShown: false }} />


      </Stack>
      <StatusBar style="auto" />
    </ThemeProvider>
    </SafeAreaView>

  );
}

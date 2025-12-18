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

    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        <Stack.Screen name="index" options={{ headerShown: false, gestureEnabled: false}} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false, gestureEnabled: false}} />
        <Stack.Screen name="connexion" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="inscription" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="creation_point_succes" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="creationSucces" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="infoUtilisateur" options={{ headerShown: false, gestureEnabled: false }} />

      </Stack>
      <StatusBar style="auto" />
    </ThemeProvider>
    </SafeAreaView>

  );
}

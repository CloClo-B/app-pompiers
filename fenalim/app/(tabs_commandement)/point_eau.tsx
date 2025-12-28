import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import {View } from 'react-native';

import HautPage from '../hautPage';
import PointSignale from '../pointSignale';

export default function HomeScreen() {
  const { page: pageR } = useLocalSearchParams<{ page?: string }>();

  const [choix, setChoix] = useState("signale"); 

  useEffect(() => {
    if (pageR) {
      setChoix(pageR);
    }
  }, [pageR]);

  return (
    <>
    <View>
      <HautPage title="Point d’eau signalé" />
    </View>
      <View style={{ flex: 1}}>
        <PointSignale />
      </View>
    </>
  );
}

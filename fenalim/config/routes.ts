export type Role = 'public' | 'pompier' | 'commandement' | 'admin';

export type Route = {
  name: string;
  path: string;
  roles: Role[]; // rôles qui peuvent accéder à la page
};

export const routes: Route[] = [
  { name: 'Accueil', path: '/(tabs)/acceuil', roles: ['public', 'pompier', 'commandement', 'admin'] },
  { name: 'Utilisateur', path: '/(tabs)/utilisateur', roles: ['public', 'admin'] },
];

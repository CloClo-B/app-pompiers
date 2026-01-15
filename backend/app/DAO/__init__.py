"""
Module DAO pour l'accès aux données
Centralise tous les DAOs pour un import facile
"""

# Import des modules DAO en tant que modules
from . import DAOHistorique as historique_dao
from . import DAOMissions as mission_dao
from . import DAOPointsEau as point_eau_dao
from . import DAOSignaler as signaler_dao
from . import DAOUtilisateurs as utilisateur_dao

# Export explicite pour faciliter les imports
__all__ = [
    'historique_dao',
    'mission_dao',
    'point_eau_dao',
    'signaler_dao',
    'utilisateur_dao',
]
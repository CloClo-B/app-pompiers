from fastapi import HTTPException, Depends
from ..token_jwt import getTokenUser

#Identifie les roles qui ont accès à la route demandée
def rolesChecker(*roles_access):

    #Verification du/des roles de l'utilisateur en fonction de ceux demandés pour cette route 
    def validityRole(user = Depends(getTokenUser)):
        if user.role not in roles_access:
            raise HTTPException(status_code=403, detail="Accès refusé")
        return user

    return validityRole

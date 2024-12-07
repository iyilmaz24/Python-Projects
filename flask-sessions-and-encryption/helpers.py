

def getDisplayUsers(AesCipher, Users):
    users = []
    
    for user in Users:
        newUser = {}
        newUser['Username'] = AesCipher.decrypt(user['Username'])
        newUser['Name'] = user['Name']
        newUser['Age'] = user['Age']
        newUser['PhNum'] = AesCipher.decrypt(user['PhNum'])
        newUser['SecurityLevel'] = user['SecurityLevel']
        newUser['LoginPassword'] = AesCipher.decrypt(user['LoginPassword'])
        users.append(newUser)
        
    return users    
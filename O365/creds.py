import json

CREDS_FILE = 'examples/auth.secret'

def getCredentials(userid):
    with open(CREDS_FILE) as f:
        credentials = json.load(f)

    if userid in credentials:
        return(credentials[userid]['username'], credentials[userid]['password'])
    
    return (None, None)
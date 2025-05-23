import os
from flask import Flask, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure OAuth 2.0
CLIENT_SECRETS_FILE = "client_secrets.json"
REDIRECT_URI = "http://localhost:5000/oauth2callback"

# Include all scopes that Google adds during OAuth flow
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    return """
    <h1>Authentication Successful!</h1>
    <p>You have successfully authenticated with YouTube.</p>
    <p>Your credentials are stored in the session.</p>
    """

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    session['credentials'] = credentials.to_json()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # This allows OAuth 2.0 credentials to be used in HTTP requests
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True) 
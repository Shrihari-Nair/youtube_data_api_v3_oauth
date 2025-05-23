import os
import json
from flask import Flask, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure OAuth 2.0
CLIENT_SECRETS_FILE = "client_secrets.json"
CREDENTIALS_FILE = "youtube_credentials.json"
REDIRECT_URI = "http://localhost:5000/oauth2callback"

# Include all scopes that Google adds during OAuth flow
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def save_credentials(credentials):
    """Save credentials to a JSON file."""
    try:
        creds_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(creds_dict, f)
    except Exception as e:
        print(f"Error saving credentials: {e}")

def load_credentials():
    """Load credentials from JSON file if it exists."""
    try:
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading credentials: {e}")
    return None

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    # Load and display stored credentials
    stored_creds = load_credentials()
    
    # Basic success message
    html = """
    <h1>Authentication Successful!</h1>
    <p>You have successfully authenticated with YouTube.</p>
    """
    
    # Add credential information if available
    if stored_creds and isinstance(stored_creds, dict):
        if 'token' in stored_creds and stored_creds['token']:
            html += f"<p>Access Token: {stored_creds['token'][:20]}...</p>"
        if 'refresh_token' in stored_creds and stored_creds['refresh_token']:
            html += f"<p>Refresh Token: {stored_creds['refresh_token'][:20]}...</p>"
        html += f"<p>Your credentials are stored in {CREDENTIALS_FILE}</p>"
    else:
        html += "<p>Your credentials are stored in the session.</p>"
    
    return html

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
    
    # Save credentials to file
    save_credentials(credentials)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # This allows OAuth 2.0 credentials to be used in HTTP requests
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True) 
import os
import pickle
from flask import Flask, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email'
]

# Configure OAuth 2.0
CLIENT_SECRETS_FILE = "client_secrets.json"
REDIRECT_URI = "http://localhost:5000/oauth2callback"

def get_authenticated_service(credentials):
    """Gets an authenticated YouTube API service."""
    return build('youtube', 'v3', credentials=credentials)

def get_my_playlists(youtube):
    """Retrieves the authenticated user's playlists."""
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    return response.get('items', [])

def get_my_subscriptions(youtube):
    """Retrieves the authenticated user's subscriptions."""
    request = youtube.subscriptions().list(
        part="snippet",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    return response.get('items', [])

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    # Get credentials from session
    credentials = pickle.loads(session['credentials'])
    
    # Refresh credentials if expired
    if credentials.expired:
        credentials.refresh(Request())
        session['credentials'] = pickle.dumps(credentials)
    
    # Get YouTube service
    youtube = get_authenticated_service(credentials)
    
    # Get user's data
    playlists = get_my_playlists(youtube)
    subscriptions = get_my_subscriptions(youtube)
    
    # Create HTML response
    html = "<h1>Your YouTube Data</h1>"
    
    html += "<h2>Your Playlists:</h2>"
    for playlist in playlists:
        html += f"<p>Playlist: {playlist['snippet']['title']}</p>"
    
    html += "<h2>Your Subscriptions:</h2>"
    for subscription in subscriptions:
        html += f"<p>Channel: {subscription['snippet']['title']}</p>"
    
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
    session['credentials'] = pickle.dumps(credentials)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # This allows OAuth 2.0 credentials to be used in HTTP requests
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True) 
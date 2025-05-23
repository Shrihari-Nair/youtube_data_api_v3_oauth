import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

def get_authenticated_service():
    """Gets an authenticated YouTube API service."""
    credentials = None
    
    # The file token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

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

def main():
    # Get authenticated service
    youtube = get_authenticated_service()
    
    # Example: Get user's playlists
    print("\nFetching your playlists...")
    playlists = get_my_playlists(youtube)
    for playlist in playlists:
        print(f"Playlist: {playlist['snippet']['title']}")
    
    # Example: Get user's subscriptions
    print("\nFetching your subscriptions...")
    subscriptions = get_my_subscriptions(youtube)
    for subscription in subscriptions:
        print(f"Channel: {subscription['snippet']['title']}")

if __name__ == '__main__':
    main() 
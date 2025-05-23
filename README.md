# YouTube Data API v3 Web OAuth Example

This project demonstrates how to use the YouTube Data API v3 with OAuth 2.0 authentication in a web application using Flask. It includes secure credential storage and robust error handling.

## Setup Instructions

1. First, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up OAuth 2.0 credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Go to "Credentials"
   - Click "Create Credentials" and select "OAuth client ID"
   - Choose "Web application" as the application type
   - Add `http://localhost:5000/oauth2callback` as an authorized redirect URI
   - Download the client secrets file and save it as `client_secrets.json` in this directory

3. Run the Flask application:
   ```bash
   python youtube_api.py
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Authentication Flow

The first time you visit the application, it will:
1. Redirect you to Google's OAuth consent screen
2. Ask you to sign in to your Google account
3. Request permission to access your YouTube data
4. Store your credentials securely
5. Redirect you back to the application showing your authentication status

## Credential Storage

The application stores credentials in two ways:
1. **Session Storage**: Temporary storage in Flask session (cleared when server stops)
2. **File Storage**: Persistent storage in `youtube_credentials.json`

The stored credentials include:
- Access Token
- Refresh Token
- Token URI
- Client ID
- Client Secret
- Scopes

## Security Features

- Credentials are stored securely in a JSON file
- Error handling for missing or invalid credentials
- Safe display of tokens (only first 20 characters shown)
- Session-based authentication state management
- Proper scope management for OAuth 2.0

## Development Notes

For development purposes, the application:
- Uses HTTP instead of HTTPS (not recommended for production)
- Runs in debug mode
- Uses a random secret key

For production use, you should:
- Use HTTPS
- Set a proper secret key
- Remove the `OAUTHLIB_INSECURE_TRANSPORT` setting
- Implement proper session management
- Add proper error handling
- Use environment variables for sensitive data

## Using Stored Credentials

The stored credentials in `youtube_credentials.json` can be used in other applications:
1. Read the JSON file
2. Create a new credentials object using the stored information
3. Use those credentials to make API calls

Example of using stored credentials:
```python
import json
from google.oauth2.credentials import Credentials

# Load credentials from file
with open('youtube_credentials.json', 'r') as f:
    creds_dict = json.load(f)

# Create credentials object
credentials = Credentials(
    token=creds_dict['token'],
    refresh_token=creds_dict['refresh_token'],
    token_uri=creds_dict['token_uri'],
    client_id=creds_dict['client_id'],
    client_secret=creds_dict['client_secret'],
    scopes=creds_dict['scopes']
)
```

## Features

The web application demonstrates:
- OAuth 2.0 web flow authentication
- Fetching user's playlists
- Fetching user's subscriptions
- Session-based credential management

You can modify the application to perform other YouTube API operations by adding new routes and API calls.

## Security Notes

- Keep your `client_secrets.json` file secure and never commit it to version control
- The application uses Flask sessions to store credentials temporarily
- For production use:
  - Use HTTPS
  - Set a proper secret key
  - Remove the `OAUTHLIB_INSECURE_TRANSPORT` setting
  - Implement proper session management
  - Add proper error handling 
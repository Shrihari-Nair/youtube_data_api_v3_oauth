# YouTube Data API v3 Web OAuth Example

This project demonstrates how to use the YouTube Data API v3 with OAuth 2.0 authentication in a web application using Flask.

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

The first time you visit the application, it will:
1. Redirect you to Google's OAuth consent screen
2. Ask you to sign in to your Google account
3. Request permission to access your YouTube data
4. Redirect you back to the application showing your YouTube data

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
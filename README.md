# YouTube Data API v3 OAuth Example

This project demonstrates how to use the YouTube Data API v3 with OAuth 2.0 authentication in Python.

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
   - Choose "Desktop application" as the application type
   - Download the client secrets file and save it as `client_secrets.json` in this directory

3. Run the script:
   ```bash
   python youtube_api.py
   ```

The first time you run the script, it will:
1. Open your default web browser
2. Ask you to sign in to your Google account
3. Request permission to access your YouTube data
4. Create a `token.pickle` file to store your credentials for future use

## Features

The example script demonstrates:
- OAuth 2.0 authentication
- Fetching user's playlists
- Fetching user's subscriptions

You can modify the script to perform other YouTube API operations by adding new functions and API calls.

## Security Note

- Keep your `client_secrets.json` and `token.pickle` files secure and never commit them to version control
- The `token.pickle` file contains your access tokens and should be treated as sensitive information 
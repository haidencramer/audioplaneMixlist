import os
import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
import uvicorn
from backend.main import app  # Import the FastAPI app from backend.main

# Initialize Firebase Admin SDK
cred = credentials.Certificate("backend/firebase-credentials.json")  # Adjust the path to your Firebase credentials file
firebase_admin.initialize_app(cred)

# Define the Cloud Function main entry point
def firebase_function(request):
    """
    Firebase HTTP function to serve FastAPI with Uvicorn.
    """
    if request.method == "OPTIONS":
        return 'ok'  # Handle OPTIONS preflight request
    
    # Start Uvicorn server with FastAPI
    return uvicorn.run(app, host="0.0.0.0", port=8080)

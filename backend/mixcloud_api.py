import requests
from sqlalchemy.orm import Session
from .models import Playlist, Mix
from .database import get_session
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Mixcloud API endpoint
MIXCLOUD_URL = "https://api.mixcloud.com"

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_mixcloud_data(query: str):
    endpoint = f"/search/?q={query}&type=cloudcast"
    url = f"{MIXCLOUD_URL}{endpoint}"
    all_data = []

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data.get('data', []))
            url = data.get('paging', {}).get('next')
        else:
            logger.error(f"Error fetching data from Mixcloud: {response.status_code} - {response.text}")
            return None

    return all_data

def populate_database_with_mixes(query=""):
    data = fetch_mixcloud_data(query)

    if data:
        session: Session = get_session()
        try:
            for item in data:
                mix_title = item.get('name', '')
                mix_url = item.get('url', '')
                playlist_id = 1  # Replace with valid playlist ID logic

                existing_mix = session.query(Mix).filter_by(mixcloud_url=mix_url).first()
                if not existing_mix:
                    new_mix = Mix(mixcloud_url=mix_url, title=mix_title, playlist_id=playlist_id)
                    session.add(new_mix)

            session.commit()
            logger.info(f"Successfully added {len(data)} mixes to the database.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error populating database: {e}")
        finally:
            session.close()

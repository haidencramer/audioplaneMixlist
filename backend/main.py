from fastapi import FastAPI, Request, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .models import Playlist, Mix
from .database import create_db_and_tables, get_session
from sqlmodel import select
from dotenv import load_dotenv
from .mixcloud_api import populate_database_with_mixes
import os

# Load environment variables from .env
load_dotenv()

# Get Mixcloud API Key
MIXCLOUD_API_KEY = os.getenv('MIXCLOUD_API_KEY')
if not MIXCLOUD_API_KEY:
    raise ValueError("MIXCLOUD_API_KEY not found in environment variables.")

# Create FastAPI app
app = FastAPI()

# Mount static files (served from backend/static)
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Set up Jinja2 templates in backend/templates
templates = Jinja2Templates(directory="backend/templates")

# Create DB and tables if they don't exist
create_db_and_tables()

# Homepage - show playlists
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    with get_session() as session:
        playlists = session.exec(select(Playlist)).all()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "playlists": playlists
        })

# Create a new playlist
@app.post("/create-playlist", response_class=HTMLResponse)
def create_playlist(request: Request, name: str = Form(...)):
    if not name.strip():
        with get_session() as session:
            playlists = session.exec(select(Playlist)).all()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "playlists": playlists,
            "error_message": "Playlist name cannot be empty"
        })

    with get_session() as session:
        playlist = Playlist(name=name)
        session.add(playlist)
        session.commit()
        return RedirectResponse("/", status_code=302)

# Search mixes
@app.get("/search", response_class=HTMLResponse)
def search(request: Request, q: str = ''):
    with get_session() as session:
        mixes = session.exec(select(Mix).where(Mix.title.ilike(f"%{q}%"))).all()
        playlists = session.exec(select(Playlist)).all()
        return templates.TemplateResponse("search.html", {
            "request": request,
            "search_results": mixes,
            "search_query": q,
            "playlists": playlists
        })

# Add a mix to a playlist
@app.get("/add-to-playlist/{mix_id}", response_class=HTMLResponse)
def add_to_playlist(request: Request, mix_id: int = Path(...), playlist_id: int = 1):
    with get_session() as session:
        mix = session.get(Mix, mix_id)
        if not mix:
            return HTMLResponse(content="Mix not found", status_code=404)

        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            playlist = Playlist(id=playlist_id, name="Default Playlist")
            session.add(playlist)
            session.commit()
            session.refresh(playlist)

        mix.playlist_id = playlist.id
        session.add(mix)
        session.commit()

    return RedirectResponse("/", status_code=302)

# Playlist popup details
@app.get("/playlist/{playlist_id}/popup", response_class=HTMLResponse)
def playlist_popup(request: Request, playlist_id: int):
    with get_session() as session:
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            return HTMLResponse(content="Playlist not found", status_code=404)

        mixes = session.exec(select(Mix).where(Mix.playlist_id == playlist.id)).all()

    return templates.TemplateResponse("playlist_popup.html", {
        "request": request,
        "playlist": playlist,
        "mixes": mixes
    })

# models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Mix(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mixcloud_url: str
    title: str
    playlist_id: Optional[int] = Field(default=None, foreign_key="playlist.id")

    
    playlist: Optional["Playlist"] = Relationship(back_populates="mixes")

class Playlist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    mixes: List[Mix] = Relationship(back_populates="playlist")
    
from datetime import datetime
from skater import Skater
import sqlite3

skaters = []
class Event:

    def __init__(self, id: int, name:str, track_id: int, date: str, distance: str, duration: float, laps:int, winner: str, category: str) -> None:
        self.id = id 
        self.name = name
        self.track_id = track_id
        self.date = self.parse_date(date).strftime('%Y-%m-%d')
        self.distance = distance
        self.duration = duration
        self.laps = laps 
        self.winner = winner
        self.category = category

    def parse_date(self, date_str):
        if date_str is None:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return datetime.strptime(date_str, "%Y-%m-%d")

    def add_skater(self, skater):
        return skaters.append(skater)

    def get_skaters(self) -> list[Skater]:
        conn = sqlite3.connect('iceskatingapp.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT s.* FROM skaters s JOIN event_skaters es ON s.id = es.skater_id WHERE es.event_id = ?', (self.id,))
            rows = cursor.fetchall()

        skaters = [Skater(*row) for row in rows]
        return skaters
    
    def get_track(self):
        from track import Track
        conn = sqlite3.connect('iceskatingapp.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tracks WHERE id = ?', (self.track_id,))
            row = cursor.fetchone()
        if row:
            return Track(*row)
        return None

    def convert_date(self, to_format: str) -> str:
        date_object = datetime.strptime(self.date, '%Y-%m-%d')
        return date_object.strftime(to_format)
    
    def convert_duration(self, to_format: str) -> str:
        minutes = int(self.duration // 60)
        seconds = self.duration % 60
        formatted_duration = to_format.replace('%M', str(minutes)).replace('%S', f'{seconds:.1f}')
        return formatted_duration
    
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))


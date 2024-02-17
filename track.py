import sqlite3


class Track:
    def __init__(self, id: int, name: str, city: str, country: str, outdoor: bool, altitude: int) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.country = country
        self.outdoor = outdoor
        self.altitude = altitude

    def get_events(self):
        from event import Event
        import sqlite3
        conn = sqlite3.connect('iceskatingapp.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events WHERE track_id = ?', (self.id,))
            rows = cursor.fetchall()

        events = [Event(*row) for row in rows]
        return events
    
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))


db_path = "iceskatingapp.db"
conn = sqlite3.connect(db_path)
conn.close()
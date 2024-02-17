from datetime import datetime, date

class Skater:
    def __init__(self, id: int, first_name: str, last_name: str, nationality: str, gender: str, date_of_birth: str) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

    def get_age(self, on_date: date = date.today()) -> int:
        age = on_date.year - self.date_of_birth.year
        if (on_date.month, on_date.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def get_events(self) -> list:
        from event import Event
        import sqlite3
        conn = sqlite3.connect('iceskatingapp.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.id, e.name, e.track_id, e.date, e.distance, e.duration, e.laps, e.winner, e.category
                FROM events e
                INNER JOIN event_skaters es ON e.id = es.event_id
                WHERE es.skater_id = ?
            ''', (self.id,))
            event_rows = cursor.fetchall()

        return [Event(*row) for row in event_rows]

    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
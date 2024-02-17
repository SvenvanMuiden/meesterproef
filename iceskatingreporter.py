from track import Track
from event import Event
from skater import Skater
from datetime import datetime
import sqlite3
import csv 

from skater import Skater
from track import Track
from event import Event


class Reporter:
    def __init__(self):
        self.conn = sqlite3.connect('iceskatingapp.db')

    def total_amount_of_skaters(self) -> int:
        with self.conn:  
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM skaters')
            return cursor.fetchone()[0]

    def highest_track(self) -> Track:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM tracks ORDER BY altitude DESC LIMIT 1')
            row = cursor.fetchone()
        if row:
            return Track(*row)  
        return None

    def longest_and_shortest_event(self) -> tuple[Event, Event]:
        with self.conn:
            cursor = self.conn.cursor()

            
            query_columns = "id, name, track_id, date, distance, duration, laps, winner, category"

            cursor.execute(f'SELECT {query_columns} FROM events ORDER BY duration DESC LIMIT 1')
            longest_event_row = cursor.fetchone()
            longest_event = Event(*longest_event_row) if longest_event_row else None

            cursor.execute(f'SELECT {query_columns} FROM events ORDER BY duration ASC LIMIT 1')
            shortest_event_row = cursor.fetchone()
            shortest_event = Event(*shortest_event_row) if shortest_event_row else None

            return (longest_event, shortest_event)

    def events_with_most_laps_for_track(self, track_id: int) -> tuple[Event, ...]:
        with self.conn:
            cursor = self.conn.cursor()

            cursor.execute('SELECT MAX(laps) FROM events WHERE track_id = ?', (track_id,))
            max_laps_row = cursor.fetchone()
            max_laps = max_laps_row[0] if max_laps_row else 0

            if max_laps:
                cursor.execute('SELECT * FROM events WHERE track_id = ? AND laps = ?', (track_id, max_laps))
                rows = cursor.fetchall()

                events = [Event(*row) for row in rows]
                return tuple(events)
            else:
                return ()

    def skaters_with_most_events(self, only_wins: bool = False) -> Skater:
        with self.conn as conn:
            cursor = conn.cursor()
            
            if only_wins:
                cursor.execute('''
                    SELECT s.*, COUNT(e.id) as event_count
                    FROM skaters s
                    JOIN events e ON s.id = e.winner
                    GROUP BY s.id
                    ORDER BY event_count DESC
                    LIMIT 1
                ''')
            else:
                cursor.execute('''
                    SELECT s.*, COUNT(es.event_id) as event_count
                    FROM skaters s
                    JOIN event_skaters es ON s.id = es.skater_id
                    GROUP BY s.id
                    ORDER BY event_count DESC
                    LIMIT 1
                ''')
        
        row = cursor.fetchone()
        if row:
            skater = Skater(*row[:-1])  
            return (skater,)
        else:
            return None

    def tracks_with_most_events(self) -> tuple[Track, ...]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, t.name, t.city, t.country, t.outdoor, t.altitude, COUNT(e.id) as event_count
                FROM tracks t
                LEFT JOIN events e ON t.id = e.track_id
                GROUP BY t.id
                ORDER BY event_count DESC
                LIMIT 1
            ''')
            row = cursor.fetchone()
            if row:
                most_events_track = Track(*row[:-1])  
                return (most_events_track,)
            else:
                return ()

    def get_first_event(self, outdoor_only: bool = False) -> Event:
        with self.conn as conn:
            cursor = conn.cursor()

            if outdoor_only:
                query = '''
                    SELECT t.id, t.name, t.city, t.country, t.outdoor, t.altitude
                    FROM events e
                    JOIN tracks t ON e.track_id = t.id
                    WHERE t.outdoor = 1
                    ORDER BY e.date DESC
                    LIMIT 1
                '''
            else:
                query = '''
                    SELECT t.id, t.name, t.city, t.country, t.outdoor, t.altitude
                    FROM events e
                    JOIN tracks t ON e.track_id = t.id
                    ORDER BY e.date DESC
                    LIMIT 1
                '''

            cursor.execute(query)
            row = cursor.fetchone()

            if row:
                return Track(*row)
            else:
                return None

    def get_latest_event(self, outdoor_only: bool = False) -> Event:
        with self.conn as conn:
            cursor = conn.cursor()

            if outdoor_only:
                query = '''
                    SELECT t.id, t.name, t.city, t.country, t.outdoor, t.altitude
                    FROM events e
                    JOIN tracks t ON e.track_id = t.id
                    WHERE t.outdoor = 1
                    ORDER BY e.date DESC
                    LIMIT 1
                '''
            else:
                query = '''
                    SELECT t.id, t.name, t.city, t.country, t.outdoor, t.altitude
                    FROM events e
                    JOIN tracks t ON e.track_id = t.id
                    ORDER BY e.date DESC
                    LIMIT 1
                '''
            
            cursor.execute(query)
            row = cursor.fetchone()

            if row:
                return Track(*row)
            else:
                return None

    def get_skaters_that_skated_track_between(self, track: Track, start: datetime, end: datetime, to_csv: bool = False) -> tuple:
        conn = sqlite3.connect('iceskatingapp.db')
        cursor = conn.cursor()
        
        start_date = start.strftime("%Y-%m-%d")
        end_date = end.strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT DISTINCT s.id, s.first_name, s.last_name, s.nationality, s.gender, s.date_of_birth
            FROM event_skaters AS es
            JOIN skaters AS s ON es.skater_id = s.id
            JOIN events AS e ON es.event_id = e.id
            WHERE e.track_id = ? AND e.date BETWEEN ? AND ?
            ORDER BY s.id ASC
        """, (track.id, start_date, end_date))
        
        skaters_data = cursor.fetchall()
        conn.close()
        
        skaters = [Skater(*data) for data in skaters_data]
        
        if to_csv:
            csv_filename = f"Skaters on Track {track.name} between {start_date} and {end_date}.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["id", "first_name", "last_name", "nationality", "gender", "date_of_birth"])
                for skater in skaters:
                    csv_writer.writerow([skater.id, skater.first_name, skater.last_name, skater.nationality, skater.gender, skater.date_of_birth.strftime("%Y-%m-%d")])

        return tuple(skaters)

    def get_tracks_in_country(self, country: str, to_csv: bool = False) -> tuple[Track, ...]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, city, country, outdoor, altitude
                FROM tracks
                WHERE country = ?
            ''', (country,))
            rows = cursor.fetchall()
            
        track_objects = tuple(Track(*row) for row in rows)  
        
        if to_csv:
            csv_filename = f"Tracks in country {country}.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['id', 'name', 'city', 'country', 'outdoor', 'altitude'])
                csv_writer.writerows(row for row in rows)
            

        return track_objects
        
    def get_skaters_with_nationality(self, nationality: str, to_csv: bool = False) -> tuple[Skater, ...]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, first_name, last_name, nationality, gender, date_of_birth
                FROM skaters
                WHERE nationality = ?
            ''', (nationality,))
            rows = cursor.fetchall()

        if to_csv:
            csv_filename = f"Skaters with nationality {nationality}.csv"
            with open(csv_filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['id', 'first_name', 'last_name', 'nationality', 'gender', 'date_of_birth'])
                csv_writer.writerows(rows)
            return ()
        else:
            return tuple(Skater(*row) for row in rows)

import json
import sqlite3
import sys
import os


def load_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)


def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skaters (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            nationality TEXT,
            gender TEXT,
            date_of_birth TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            city TEXT,
            country TEXT,
            outdoor BOOLEAN,
            altitude INTEGER
        )
    ''')  

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT,
            track_id INTEGER,
            date TEXT,
            distance INTEGER,
            duration TEXT,
            laps INTEGER,
            winner INTEGER,  
            category TEXT,
            FOREIGN KEY (track_id) REFERENCES tracks(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_skaters (
            event_id INTEGER,
            skater_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (skater_id) REFERENCES skaters(id)
        )
    ''')


def initialize_database(conn, json_data):
    cursor = conn.cursor()
    create_tables(cursor)

    cursor.execute('SELECT COUNT(*) FROM skaters')
    if cursor.fetchone()[0] == 0:
        populate_database(cursor, json_data)

    conn.commit()
    cursor.close()


def populate_database(cursor, json_data):
    processed_skaters = set()
    processed_tracks = set()

    for event in json_data:
        track = event['track']
        if track['id'] not in processed_tracks:
            cursor.execute(
                "INSERT INTO tracks (id, name, city, country, outdoor, altitude) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    track['id'],
                    track['name'],
                    track['city'],
                    track['country'],
                    track['isOutdoor'],
                    track['altitude']
                )
            )
            processed_tracks.add(track['id'])
        duration_str = event['results'][0]['time'] if event['results'] else None
        winner_id = event['results'][0]['skater']['id'] if event['results'] else None
        cursor.execute(
            "INSERT INTO events (id, name, track_id, date, distance, duration, laps, winner, category) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event['id'],
                event['title'],
                track['id'],
                event['start'],
                event['distance']['distance'],
                duration_str,
                event['distance']['lapCount'],
                winner_id,
                event['category']
            )
        )
        for result in event['results']:
            skater = result['skater']
            if skater['id'] not in processed_skaters:
                cursor.execute(
                    "INSERT INTO skaters (id, first_name, last_name, nationality, gender, date_of_birth) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        skater['id'],
                        skater['firstName'],
                        skater['lastName'],
                        skater['country'],
                        skater['gender'],
                        skater['dateOfBirth']
                    )
                )
                processed_skaters.add(skater['id'])

            cursor.execute(
                "INSERT INTO event_skaters (event_id, skater_id) "
                "VALUES (?, ?)",
                (
                    event['id'],
                    skater['id']
                )
            )


def main():
    db_path = 'iceskatingapp.db'
    json_file = 'events.json'

    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(json_file):
        print(f"JSON file {json_file} does not exist.")
        sys.exit(1)

    json_data = load_json(json_file)
    
    conn = sqlite3.connect(db_path)
    initialize_database(conn, json_data)
    conn.close()


if __name__ == "__main__":
    main()
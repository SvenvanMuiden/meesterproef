import unittest
from datetime import date
from skater import Skater
from event import Event
from track import Track


class TestSkatingApp(unittest.TestCase):

    def test_age_of_skater(self):
        skater = Skater(1, "John", "Doe", "USA", "M", "2000-01-01")
        self.assertEqual(skater.get_age(date(2024, 1, 1)), 24)

    def test_get_events_of_skater(self):
        skater = Skater(1, "John", "Doe", "USA", "M", "2000-01-01")
        events = skater.get_events()
        self.assertIsInstance(events, list)

    def test_get_events_of_track(self):
        track = Track(1, "Ice Arena", "New York", "USA", False, 10)
        events = track.get_events()
        self.assertIsInstance(events, list)

    def test_event_date_conversion(self):
        event = Event(1, "Championship", 1, "2023-12-25T15:30:00Z", "500m", 90.0, 5, "John Doe", "Sprint")
        self.assertEqual(event.convert_date("%B %d, %Y"), "December 25, 2023")

    def test_event_duration_conversion(self):
        event = Event(1, "Championship", 1, "2023-12-25", "500m", 79.0, 5, "John Doe", "Sprint")
        self.assertEqual(event.convert_duration("%M minutes %S seconds"), "1 minutes 19.0 seconds")


if __name__ == '__main__':
    unittest.main()

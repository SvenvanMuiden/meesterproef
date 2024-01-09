from datetime import datetime


class Event:

    def __init__(self, id: int, name:str, track_id: int, date: str, duration: float, laps:int, winner: str, category: str) -> None:
        self.id = id 
        self.name = name
        self.track_id = track_id
        self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        self.duration = duration
        self.laps = laps 
        self.winner = winner
        self.category = category
        self.skaters = []

    def add_skater(self, skater):
        self.skaters.append(skater)

    def get_skaters(self) -> list:
        return self.skaters
    
    def get_track(self):
        pass

    def convert_date(self, to_format: str) -> str:
        return self.date.strftime(to_format)
    
    def convert_duration(self, to_format: str) -> str:
        minutes = int(self.duration // 60)
        seconds = self.duration % 60
        # Format the duration string based on the to_format argument
        formatted_duration = to_format.replace('%M', str(minutes)).replace('%S', f'{seconds:.3f}')

        return formatted_duration
    
    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
from event import Event

class Track:
    def __init__(self, id: int, name: str, city: str, country: str, outdoor: bool, altitude: int) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.country = country
        self.outdoor = outdoor
        self.altitude = altitude

    def get_events(self):
        pass
    
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
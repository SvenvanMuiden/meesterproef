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

    def get_events(self):
        # This method will depend on how event data is linked to skaters in your application
        # For example, it might involve querying a database or accessing a data structure
        pass

    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
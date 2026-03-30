from datetime import datetime


class Owner:
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id
        self.pets: list["Pet"] = []
        self.availability_windows: list[str] = []

    def add_pet(self, pet: "Pet") -> None:
        pass

    def remove_pet(self, pet: "Pet") -> None:
        pass

    def get_pets(self) -> list["Pet"]:
        pass


class Pet:
    def __init__(self, name: str, species: str, age: int, owner: Owner):
        self.name = name
        self.species = species
        self.age = age
        self.owner = owner
        self.walks_per_day: int = 1
        self.feeding_times: list[str] = []
        self.special_notes: str = ""

    def get_daily_needs(self) -> list["Task"]:
        pass


class Task:
    def __init__(
        self,
        name: str,
        type: str,
        description: str,
        duration: float,
        priority: str,
        deadline: datetime,
        associated_pet: Pet,
        is_recurring: bool = False,
    ):
        self.name = name
        self.type = type
        self.description = description
        self.duration = duration
        self.priority = priority
        self.deadline = deadline
        self.associated_pet = associated_pet
        self.is_recurring = is_recurring
        self.completed = False

    def mark_complete(self) -> None:
        pass

    def perform(self) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.tasks: list[Task] = []
        self.owner = owner

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def schedule_walk(self, pet: Pet, deadline: datetime) -> None:
        pass

    def get_today_tasks(self) -> list[Task]:
        pass

    def generate_schedule(self) -> list[Task]:
        pass

    def get_next_task(self) -> Task:
        pass

    def filter_by_pet(self, pet: Pet) -> list[Task]:
        pass

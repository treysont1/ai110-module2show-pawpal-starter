from datetime import datetime

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Owner:
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id
        self.pets: list["Pet"] = []
        self.availability_windows: list[str] = []

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to this owner and set the pet's owner reference."""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from this owner's list if present."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> list["Pet"]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list["Task"]:
        """Return a flat list of every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Pet:
    def __init__(self, name: str, species: str, age: int, owner: Owner):
        self.name = name
        self.species = species
        self.age = age
        self.owner = owner
        self.walks_per_day: int = 1
        self.feeding_times: list[str] = []
        self.special_notes: str = ""
        self.tasks: list["Task"] = []

    def add_task(self, task: "Task") -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_daily_needs(self) -> list["Task"]:
        """Auto-generate suggested tasks for today based on this pet's needs."""
        today = datetime.now()
        needs = []

        for i in range(self.walks_per_day):
            hour = 8 + i * (8 // max(self.walks_per_day, 1))
            needs.append(Task(
                name="Walk",
                type="walk",
                description=f"Walk {self.name}",
                duration=30.0,
                priority="medium",
                deadline=today.replace(hour=hour, minute=0, second=0, microsecond=0),
                associated_pet=self,
                is_recurring=True,
            ))

        for time_str in self.feeding_times:
            needs.append(Task(
                name="Feed",
                type="feed",
                description=f"Feed {self.name} at {time_str}",
                duration=10.0,
                priority="high",
                deadline=today,
                associated_pet=self,
                is_recurring=True,
            ))

        return needs


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
        """Mark this task as completed and print a confirmation message."""
        self.completed = True
        print(f"Task '{self.name}' for {self.associated_pet.name} marked complete.")

    def perform(self) -> None:
        """Execute this task by printing its action and marking it complete."""
        print(f"Performing '{self.name}' for {self.associated_pet.name}...")
        self.mark_complete()


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def _all_tasks(self) -> list[Task]:
        """Retrieve all tasks across every pet the owner has."""
        return [task for pet in self.owner.get_pets() for task in pet.tasks]

    def add_task(self, task: Task) -> None:
        """Route a task into its associated pet's task list."""
        task.associated_pet.add_task(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from its associated pet's task list if present."""
        pet_tasks = task.associated_pet.tasks
        if task in pet_tasks:
            pet_tasks.remove(task)

    def schedule_walk(self, pet: Pet, deadline: datetime) -> None:
        """Create a walk task for the given pet and add it to the schedule."""
        task = Task(
            name="Walk",
            type="walk",
            description=f"Walk {pet.name}",
            duration=30.0,
            priority="medium",
            deadline=deadline,
            associated_pet=pet,
        )
        self.add_task(task)

    def get_today_tasks(self) -> list[Task]:
        """Return all incomplete tasks whose deadline falls on today's date."""
        today = datetime.now().date()
        return [
            t for t in self._all_tasks()
            if t.deadline.date() == today and not t.completed
        ]

    def generate_schedule(self) -> list[Task]:
        """Return all pending tasks sorted by priority then deadline."""
        pending = [t for t in self._all_tasks() if not t.completed]
        return sorted(
            pending,
            key=lambda t: (PRIORITY_ORDER.get(t.priority.lower(), 1), t.deadline),
        )

    def get_next_task(self) -> Task | None:
        """Return the highest-priority pending task, or None if none exist."""
        schedule = self.generate_schedule()
        return schedule[0] if schedule else None

    def filter_by_pet(self, pet: Pet) -> list[Task]:
        """Return all tasks associated with a specific pet."""
        return list(pet.tasks)

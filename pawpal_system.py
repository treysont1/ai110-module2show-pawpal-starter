from datetime import datetime, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
_SORT_KEY = lambda t: (PRIORITY_ORDER.get(t.priority.lower(), 1), t.deadline, t.name)


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list["Pet"] = []
        self.availability_windows: list[str] = []
        self._pet_lookup: dict[str, "Pet"] = {}

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to this owner and set the pet's owner reference."""
        if pet in self.pets:
            return
        pet.owner = self
        self.pets.append(pet)
        self._pet_lookup[pet.name] = pet

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from this owner's list if present."""
        if pet in self.pets:
            self.pets.remove(pet)
            self._pet_lookup.pop(pet.name, None)

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

        WALK_DURATION = {"dog": 30.0, "cat": 0.0, "other": 15.0}
        walk_duration = WALK_DURATION.get(self.species, 15.0)

        # Puppies/kittens (under 1 year) need more frequent walks/feeds
        walks = self.walks_per_day
        if self.age < 1:
            walks = max(walks, 4)

        for i in range(walks):
            if walk_duration == 0.0:
                continue
            hour = 8 + i * (12 // walks)
            needs.append(Task(
                name="Walk",
                type="walk",
                description=f"Walk {self.name}",
                duration=walk_duration,
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
        frequency: str = "daily",
    ):
        self.name = name
        self.type = type
        self.description = description
        self.duration = duration
        self.priority = priority
        self.deadline = deadline
        self.associated_pet = associated_pet
        self.is_recurring = is_recurring
        self.frequency = frequency  # "daily" or "weekly"
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
        return self.owner.get_all_tasks()

    def has_conflict(self, task: Task) -> bool:
        """Return True if task's time window overlaps any existing incomplete task."""
        return any(
            not e.completed
            and task.deadline - timedelta(minutes=task.duration) < e.deadline
            and task.deadline > e.deadline - timedelta(minutes=e.duration)
            for e in self._all_tasks()
            if e is not task
        )

    def add_task(self, task: Task) -> None:
        """Route a task into its associated pet's task list, ignoring duplicates.

        Prints a warning if the task's time window overlaps an existing task.
        """
        pet_tasks = task.associated_pet.tasks
        if task in pet_tasks:
            return
        if self.has_conflict(task):
            print(f"WARNING: '{task.name}' ({task.associated_pet.name}) overlaps an existing task.")
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
        """Return all pending tasks sorted by priority, deadline, then name."""
        pending = [t for t in self._all_tasks() if not t.completed]
        return sorted(pending, key=_SORT_KEY)

    def get_next_task(self) -> Task | None:
        """Return the highest-priority pending task, or None if none exist."""
        pending = [t for t in self._all_tasks() if not t.completed]
        return min(pending, key=_SORT_KEY, default=None)

    def filter_by_pet(self, pet: Pet) -> list[Task]:
        """Return all tasks associated with a specific pet."""
        return list(pet.tasks)

    def filter_by_pet_name(self, name: str) -> list[Task]:
        """Return all tasks for the pet with the given name, sorted by priority then deadline."""
        pet = self.owner._pet_lookup.get(name)
        if not pet:
            return []
        return sorted(pet.tasks, key=_SORT_KEY)

    def filter_by_completion(self, completed: bool) -> list[Task]:
        """Return all tasks matching the given completion status, sorted by priority then deadline."""
        tasks = [t for t in self._all_tasks() if t.completed == completed]
        return sorted(tasks, key=_SORT_KEY)

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and, if recurring, schedule the next occurrence.

        Returns the newly created next-occurrence Task, or None if not recurring.
        """
        task.mark_complete()
        if not task.is_recurring:
            return None
        delta = timedelta(weeks=1) if task.frequency == "weekly" else timedelta(days=1)
        next_task = Task(
            name=task.name,
            type=task.type,
            description=task.description,
            duration=task.duration,
            priority=task.priority,
            deadline=task.deadline + delta,
            associated_pet=task.associated_pet,
            is_recurring=True,
            frequency=task.frequency,
        )
        self.add_task(next_task)
        return next_task

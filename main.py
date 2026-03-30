from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Alex")

dog = Pet(name="Buddy", species="dog", age=3, owner=owner)
cat = Pet(name="Whiskers", species="cat", age=5, owner=owner)

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner=owner)

today = datetime.now()

# --- Add tasks OUT OF ORDER (low priority first, late deadline first) ---
scheduler.add_task(Task(
    name="Playtime",
    type="play",
    description="Play with Whiskers using the feather toy",
    duration=15.0,
    priority="low",
    deadline=today.replace(hour=18, minute=0, second=0, microsecond=0),
    associated_pet=cat,
))

scheduler.add_task(Task(
    name="Vet Checkup",
    type="vet",
    description="Annual checkup for Buddy",
    duration=60.0,
    priority="high",
    deadline=today.replace(hour=14, minute=0, second=0, microsecond=0),
    associated_pet=dog,
    is_recurring=True,
    frequency="weekly",
))

scheduler.add_task(Task(
    name="Afternoon Feed",
    type="feed",
    description="Feed Whiskers her afternoon meal",
    duration=5.0,
    priority="high",
    deadline=today.replace(hour=13, minute=0, second=0, microsecond=0),
    associated_pet=cat,
    is_recurring=True,
    frequency="daily",
))

scheduler.add_task(Task(
    name="Walk",
    type="walk",
    description="Take Buddy for a walk around the block",
    duration=30.0,
    priority="medium",
    deadline=today.replace(hour=9, minute=30, second=0, microsecond=0),
    associated_pet=dog,
    is_recurring=True,
    frequency="daily",
))

scheduler.add_task(Task(
    name="Morning Feed",
    type="feed",
    description="Feed Buddy his morning kibble",
    duration=10.0,
    priority="high",
    deadline=today.replace(hour=8, minute=0, second=0, microsecond=0),
    associated_pet=dog,
    is_recurring=True,
    frequency="daily",
))


def print_tasks(tasks, label):
    print(f"\n{'=' * 45}")
    print(f"  {label}")
    print(f"{'=' * 45}")
    if not tasks:
        print("  (none)")
        return
    for i, task in enumerate(tasks, 1):
        status = "Done" if task.completed else "Pending"
        print(f"{i}. [{task.deadline.strftime('%I:%M %p')}] {task.name} ({task.associated_pet.name})")
        print(f"   Priority: {task.priority}  |  Duration: {task.duration} min  |  Status: {status}")


# --- 1. Sorted schedule (priority → deadline → name) ---
print_tasks(scheduler.generate_schedule(), "SORTED SCHEDULE (priority > deadline > name)")

# --- 2. Filter by pet name ---
print_tasks(scheduler.filter_by_pet_name("Buddy"), "FILTER BY PET NAME: Buddy")
print_tasks(scheduler.filter_by_pet_name("Whiskers"), "FILTER BY PET NAME: Whiskers")

# --- 3. Filter by completion status (all pending before any completions) ---
print_tasks(scheduler.filter_by_completion(False), "FILTER: INCOMPLETE TASKS")
print_tasks(scheduler.filter_by_completion(True), "FILTER: COMPLETED TASKS")

# --- 4. Complete a recurring task and verify next occurrence is scheduled ---
walk_task = scheduler.filter_by_pet_name("Buddy")[1]  # Walk is 2nd Buddy task by list order
next_walk = scheduler.complete_task(walk_task)

print(f"\n{'=' * 45}")
print("  COMPLETE RECURRING TASK: Walk")
print(f"{'=' * 45}")
print(f"  Completed: {walk_task.name} @ {walk_task.deadline.strftime('%I:%M %p on %A %b %d')}")
if next_walk:
    print(f"  Next occurrence scheduled: {next_walk.name} @ {next_walk.deadline.strftime('%I:%M %p on %A %b %d')}")

# --- 5. Re-check completed vs incomplete after marking done ---
print_tasks(scheduler.filter_by_completion(False), "FILTER: INCOMPLETE TASKS (after completing Walk)")
print_tasks(scheduler.filter_by_completion(True), "FILTER: COMPLETED TASKS (after completing Walk)")

print()

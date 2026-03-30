from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Alex", id="owner_001")

dog = Pet(name="Buddy", species="Dog", age=3, owner=owner)
cat = Pet(name="Whiskers", species="Cat", age=5, owner=owner)

owner.add_pet(dog)
owner.add_pet(cat)

# --- Tasks ---
today = datetime.now()

scheduler = Scheduler(owner=owner)

scheduler.add_task(Task(
    name="Morning Feed",
    type="feed",
    description="Feed Buddy his morning kibble",
    duration=10.0,
    priority="high",
    deadline=today.replace(hour=8, minute=0, second=0, microsecond=0),
    associated_pet=dog,
    is_recurring=True,
))

scheduler.add_task(Task(
    name="Walk",
    type="walk",
    description="Take Buddy for a walk around the block",
    duration=30.0,
    priority="medium",
    deadline=today.replace(hour=9, minute=30, second=0, microsecond=0),
    associated_pet=dog,
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
))

scheduler.add_task(Task(
    name="Playtime",
    type="play",
    description="Play with Whiskers using the feather toy",
    duration=15.0,
    priority="low",
    deadline=today.replace(hour=18, minute=0, second=0, microsecond=0),
    associated_pet=cat,
))

# --- Print Today's Schedule ---
print("=" * 40)
print("       TODAY'S SCHEDULE")
print("=" * 40)

tasks = scheduler.get_today_tasks()

if not tasks:
    print("No tasks scheduled for today.")
else:
    for i, task in enumerate(tasks, start=1):
        status = "Done" if task.completed else "Pending"
        print(f"{i}. [{task.deadline.strftime('%I:%M %p')}] {task.name} ({task.associated_pet.name})")
        print(f"   {task.description}")
        print(f"   Priority: {task.priority}  |  Duration: {task.duration} min  |  Status: {status}")
        print()

print("=" * 40)

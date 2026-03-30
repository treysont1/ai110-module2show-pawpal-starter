import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


@pytest.fixture
def owner_with_pet():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", species="dog", age=3, owner=owner)
    owner.add_pet(pet)
    return owner, pet


@pytest.fixture
def scheduler(owner_with_pet):
    owner, _ = owner_with_pet
    return Scheduler(owner)


@pytest.fixture
def base_deadline():
    return datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)


@pytest.fixture
def sample_task(owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    return Task(
        name="Walk",
        type="walk",
        description="Walk the dog",
        duration=30.0,
        priority="medium",
        deadline=base_deadline,
        associated_pet=pet,
    )


# --- Core behavior: mark complete ---

def test_mark_complete_changes_status(sample_task):
    assert sample_task.completed is False
    sample_task.mark_complete()
    assert sample_task.completed is True


def test_add_task_increases_pet_task_count(owner_with_pet, sample_task):
    _, pet = owner_with_pet
    initial_count = len(pet.tasks)
    pet.add_task(sample_task)
    assert len(pet.tasks) == initial_count + 1


# --- Core behavior: conflict detection ---

def test_has_conflict_overlapping_tasks(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t1 = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet)
    scheduler.add_task(t1)

    # starts 15 min before t1 ends — overlaps
    t2 = Task("Feed", "feed", "", 30.0, "high", base_deadline - timedelta(minutes=15), pet)
    assert scheduler.has_conflict(t2) is True


def test_has_conflict_non_overlapping_tasks(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t1 = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet)
    scheduler.add_task(t1)

    # starts after t1 ends — no overlap
    t2 = Task("Feed", "feed", "", 30.0, "high", base_deadline + timedelta(hours=2), pet)
    assert scheduler.has_conflict(t2) is False


def test_has_conflict_completed_task_ignored(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t1 = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet)
    t1.completed = True
    scheduler.add_task(t1)

    t2 = Task("Feed", "feed", "", 30.0, "high", base_deadline, pet)
    assert scheduler.has_conflict(t2) is False


def test_no_self_conflict(scheduler, owner_with_pet, base_deadline):
    """A task already in the list should not conflict with itself."""
    _, pet = owner_with_pet
    t1 = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet)
    scheduler.add_task(t1)
    assert scheduler.has_conflict(t1) is False


# --- Core behavior: generate_schedule ordering ---

def test_generate_schedule_chronological_order(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t1 = Task("Groom", "groom", "", 20.0, "low", base_deadline + timedelta(hours=1), pet)
    t2 = Task("Med", "med", "", 10.0, "high", base_deadline + timedelta(hours=2), pet)
    t3 = Task("Feed", "feed", "", 10.0, "medium", base_deadline + timedelta(hours=3), pet)
    for t in (t1, t2, t3):
        pet.add_task(t)

    schedule = scheduler.generate_schedule()
    assert schedule == [t1, t2, t3]


def test_generate_schedule_priority_tiebreak_same_deadline(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    low = Task("Groom", "groom", "", 20.0, "low", base_deadline, pet)
    high = Task("Med", "med", "", 10.0, "high", base_deadline, pet)
    for t in (low, high):
        pet.add_task(t)

    schedule = scheduler.generate_schedule()
    assert schedule[0] is high


def test_generate_schedule_deadline_tiebreak(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    later = Task("B", "walk", "", 30.0, "medium", base_deadline + timedelta(hours=2), pet)
    earlier = Task("A", "walk", "", 30.0, "medium", base_deadline + timedelta(hours=1), pet)
    for t in (later, earlier):
        pet.add_task(t)

    schedule = scheduler.generate_schedule()
    assert schedule[0] is earlier


def test_generate_schedule_empty_when_all_complete(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet)
    t.completed = True
    pet.add_task(t)
    assert scheduler.generate_schedule() == []


# --- Core behavior: get_next_task ---

def test_get_next_task_returns_earliest_deadline(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    later = Task("Groom", "groom", "", 20.0, "low", base_deadline + timedelta(hours=2), pet)
    sooner = Task("Med", "med", "", 10.0, "high", base_deadline + timedelta(hours=1), pet)
    for t in (later, sooner):
        pet.add_task(t)

    assert scheduler.get_next_task() is sooner


def test_get_next_task_returns_none_when_empty(scheduler):
    assert scheduler.get_next_task() is None


def test_get_next_task_returns_none_when_all_complete(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet)
    t.completed = True
    pet.add_task(t)
    assert scheduler.get_next_task() is None


# --- Core behavior: complete_task recurrence ---

def test_complete_task_daily_recurrence(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet, is_recurring=True, frequency="daily")
    pet.add_task(t)

    next_task = scheduler.complete_task(t)
    assert next_task is not None
    assert next_task.deadline == base_deadline + timedelta(days=1)
    assert next_task in pet.tasks


def test_complete_task_weekly_recurrence(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t = Task("Groom", "groom", "", 60.0, "low", base_deadline, pet, is_recurring=True, frequency="weekly")
    pet.add_task(t)

    next_task = scheduler.complete_task(t)
    assert next_task.deadline == base_deadline + timedelta(weeks=1)


def test_complete_task_non_recurring_returns_none(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    t = Task("Vet", "vet", "", 60.0, "high", base_deadline, pet, is_recurring=False)
    pet.add_task(t)

    assert scheduler.complete_task(t) is None


def test_complete_task_twice_creates_two_recurrences(scheduler, owner_with_pet, base_deadline):
    """Calling complete_task twice on the same task produces two future tasks."""
    _, pet = owner_with_pet
    t = Task("Walk", "walk", "", 30.0, "medium", base_deadline, pet, is_recurring=True, frequency="daily")
    pet.add_task(t)

    scheduler.complete_task(t)
    scheduler.complete_task(t)
    future_tasks = [task for task in pet.tasks if task is not t]
    assert len(future_tasks) == 2


# --- Core behavior: get_daily_needs species/age ---

def test_get_daily_needs_cat_no_walks(owner_with_pet):
    owner, _ = owner_with_pet
    cat = Pet(name="Whiskers", species="cat", age=2, owner=owner)
    cat.walks_per_day = 1
    needs = cat.get_daily_needs()
    walk_tasks = [t for t in needs if t.type == "walk"]
    assert walk_tasks == []


def test_get_daily_needs_dog_produces_walks(owner_with_pet):
    _, pet = owner_with_pet  # species="dog"
    pet.walks_per_day = 2
    needs = pet.get_daily_needs()
    walk_tasks = [t for t in needs if t.type == "walk"]
    assert len(walk_tasks) == 2


def test_get_daily_needs_young_pet_min_four_walks(owner_with_pet):
    owner, _ = owner_with_pet
    puppy = Pet(name="Pup", species="dog", age=0, owner=owner)
    puppy.walks_per_day = 1
    needs = puppy.get_daily_needs()
    walk_tasks = [t for t in needs if t.type == "walk"]
    assert len(walk_tasks) >= 4


def test_get_daily_needs_feeding_times_produce_high_priority_tasks(owner_with_pet):
    _, pet = owner_with_pet
    pet.feeding_times = ["8:00", "18:00"]
    needs = pet.get_daily_needs()
    feed_tasks = [t for t in needs if t.type == "feed"]
    assert len(feed_tasks) == 2
    assert all(t.priority == "high" for t in feed_tasks)


# --- Edge case: unknown priority ---

def test_unknown_priority_treated_as_medium(scheduler, owner_with_pet, base_deadline):
    _, pet = owner_with_pet
    # same deadline — unknown priority falls back to 1 (medium), so tiebreak is by name
    unknown = Task("A", "other", "", 10.0, "urgent", base_deadline, pet)
    known_medium = Task("B", "other", "", 10.0, "medium", base_deadline, pet)
    for t in (unknown, known_medium):
        pet.add_task(t)

    schedule = scheduler.generate_schedule()
    # both sort value 1; "A" < "B" alphabetically
    assert schedule[0] is unknown


# --- Edge case: pet with no tasks ---

def test_filter_by_pet_name_no_tasks(scheduler, owner_with_pet):
    owner, _ = owner_with_pet
    empty_pet = Pet(name="Ghost", species="cat", age=1, owner=owner)
    owner.add_pet(empty_pet)
    assert scheduler.filter_by_pet_name("Ghost") == []


def test_filter_by_pet_name_unknown_pet(scheduler):
    assert scheduler.filter_by_pet_name("Nobody") == []

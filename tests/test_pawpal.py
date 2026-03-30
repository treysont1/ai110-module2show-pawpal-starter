import pytest
from datetime import datetime
from pawpal_system import Owner, Pet, Task


@pytest.fixture
def sample_task(owner_with_pet):
    _, pet = owner_with_pet
    return Task(
        name="Walk",
        type="walk",
        description="Walk the dog",
        duration=30.0,
        priority="medium",
        deadline=datetime.now(),
        associated_pet=pet,
    )


@pytest.fixture
def owner_with_pet():
    owner = Owner(name="Alex", id="owner_001")
    pet = Pet(name="Buddy", species="Dog", age=3, owner=owner)
    owner.add_pet(pet)
    return owner, pet


def test_mark_complete_changes_status(sample_task):
    assert sample_task.completed is False
    sample_task.mark_complete()
    assert sample_task.completed is True


def test_add_task_increases_pet_task_count(owner_with_pet, sample_task):
    _, pet = owner_with_pet
    initial_count = len(pet.tasks)
    pet.add_task(sample_task)
    assert len(pet.tasks) == initial_count + 1

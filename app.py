import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# --- Owner setup ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if st.button("Create Owner"):
    owner = Owner(name=owner_name)
    scheduler = Scheduler(owner=owner)
    st.session_state.owner = owner
    st.session_state.scheduler = scheduler
    st.success(f"Owner '{owner_name}' created.")

if st.session_state.owner is None:
    st.info("Create an owner above to get started.")
    st.stop()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    pet = Pet(name=pet_name, species=species, age=age, owner=owner)
    owner.add_pet(pet)
    st.success(f"Added {species} '{pet_name}' to {owner.name}'s pets.")

if owner.get_pets():
    st.write("Current pets:", [p.name for p in owner.get_pets()])

st.divider()

# --- Schedule a Task ---
st.subheader("Schedule a Task")

if not owner.get_pets():
    st.info("Add a pet before scheduling tasks.")
else:
    pet_names = [p.name for p in owner.get_pets()]

    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_type = st.selectbox("Type", ["walk", "feed", "play", "vet", "other"])
        selected_pet_name = st.selectbox("For which pet?", pet_names)
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        deadline_time = st.time_input("Deadline", value=datetime.now().replace(hour=9, minute=0))

    if st.button("Add Task"):
        selected_pet = owner._pet_lookup[selected_pet_name]
        deadline = datetime.combine(datetime.today(), deadline_time)
        task = Task(
            name=task_title,
            type=task_type,
            description=task_title,
            duration=float(duration),
            priority=priority,
            deadline=deadline,
            associated_pet=selected_pet,
        )
        if scheduler.has_conflict(task):
            st.warning(
                f"'{task_title}' overlaps an existing task for {selected_pet_name}. "
                "It was added but check the schedule for conflicts."
            )
        scheduler.add_task(task)
        st.success(f"Task '{task_title}' added for {selected_pet_name}.")

st.divider()

# --- Today's Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    today = datetime.now().date()
    today_tasks = [t for t in scheduler.generate_schedule() if t.deadline.date() == today]

    if not today_tasks:
        st.info("No tasks scheduled for today.")
    else:
        priority_badge = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}

        rows = [
            {
                "Time": t.deadline.strftime("%I:%M %p"),
                "Task": t.name,
                "Pet": t.associated_pet.name,
                "Priority": priority_badge.get(t.priority.lower(), t.priority),
                "Duration (min)": int(t.duration),
            }
            for t in today_tasks
        ]

        st.dataframe(rows, use_container_width=True, hide_index=True)
        st.caption(f"{len(today_tasks)} task(s) — sorted chronologically, priority breaks ties.")

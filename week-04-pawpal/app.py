import warnings
from datetime import datetime, time
from pawpal_system import User, Household, Pet, Task, Notification
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# ── Session State ──────────────────────────────────────────────────────────────
# Every key we need is initialized here so reruns never hit a KeyError.
defaults = {
    "household":        None,
    "tasks":            [],
    "notifications":    [],
    "task_counter":     1,
    "notif_counter":    1,
    "member_counter":   2,   # owner is always u1
    "pinging_task_id":  None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── Helpers ────────────────────────────────────────────────────────────────────
def time_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    return "Good evening"


def reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# SETUP PHASE — shown only before a household exists
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.household is None:
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.title("🐾 PawPal+")
        st.caption("Let's get you set up.")
        st.divider()

        with st.form("setup_form"):
            st.subheader("Create your household")
            col1, col2 = st.columns(2)
            with col1:
                owner_name     = st.text_input("Your name",       placeholder="Sarah")
                owner_email    = st.text_input("Email",           placeholder="sarah@email.com")
            with col2:
                owner_phone    = st.text_input("Phone",           placeholder="555-1001")
                household_name = st.text_input("Household name",  placeholder="The Santos House")

            go = st.form_submit_button("Get started →", use_container_width=True)

        if go:
            if not all([owner_name, owner_email, owner_phone, household_name]):
                st.error("Please fill in all fields.")
            else:
                owner = User(
                    userId="u1",
                    name=owner_name,
                    email=owner_email,
                    phone=owner_phone,
                    availability={
                        day: ["08:00-20:00"]
                        for day in ["Monday","Tuesday","Wednesday",
                                    "Thursday","Friday","Saturday","Sunday"]
                    },
                )
                st.session_state.household = Household(
                    householdId="h1",
                    name=household_name,
                    members=[owner],
                    pets=[],
                )
                st.rerun()
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PHASE — everything below only renders once household exists
# ══════════════════════════════════════════════════════════════════════════════
household  = st.session_state.household
owner      = household.members[0]
pet_lookup = {p.petId: p.name for p in household.pets}


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## 🏠 {household.name}")
    st.divider()

    # Owner bio
    st.markdown("**👤 Owner**")
    st.markdown(f"### {owner.name}")
    st.caption(f"📧 {owner.email}")
    st.caption(f"📞 {owner.phone}")
    st.divider()

    # Pets list
    st.markdown("**🐾 Pets**")
    if household.pets:
        for pet in household.pets:
            with st.expander(pet.name):
                st.write(f"**Breed:** {pet.breed}")
                st.write(f"**Age:** {pet.age}")
                st.write(f"**Vet:** {pet.vetName or '—'}")
                st.write(f"**Vet phone:** {pet.vetPhone or '—'}")
    else:
        st.caption("No pets yet.")

    with st.expander("+ Add a pet"):
        with st.form("sidebar_pet_form"):
            s_pet_name  = st.text_input("Name",      placeholder="Mochi")
            s_pet_breed = st.text_input("Breed",     placeholder="Shiba Inu")
            s_pet_age   = st.number_input("Age", min_value=0, max_value=30, value=1)
            s_vet_name  = st.text_input("Vet name",  placeholder="Dr. Kim (optional)")
            s_vet_phone = st.text_input("Vet phone", placeholder="555-9001 (optional)")
            add_pet_btn = st.form_submit_button("Add pet", use_container_width=True)

        if add_pet_btn and s_pet_name:
            pid = f"p{len(household.pets) + 1}"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                new_pet = Pet(
                    petId=pid, name=s_pet_name, breed=s_pet_breed,
                    age=int(s_pet_age), householdId="",
                    vetName=s_vet_name or None, vetPhone=s_vet_phone or None,
                )
            new_pet.addPet(household)
            if not s_vet_name or not s_vet_phone:
                st.warning(f"No vet info for {s_pet_name} — recommended.")
            else:
                st.success(f"{s_pet_name} added!")
            st.rerun()

    st.divider()

    # Members list
    st.markdown("**👥 Members**")
    for m in household.members:
        st.caption(f"• {m.name}")

    with st.expander("+ Add member"):
        with st.form("add_member_form"):
            m_name  = st.text_input("Name",  placeholder="Alex")
            m_email = st.text_input("Email", placeholder="alex@email.com")
            m_phone = st.text_input("Phone", placeholder="555-2002")
            add_m   = st.form_submit_button("Add member", use_container_width=True)

        if add_m and m_name:
            uid = f"u{st.session_state.member_counter}"
            st.session_state.member_counter += 1
            new_member = User(
                userId=uid, name=m_name, email=m_email, phone=m_phone,
                availability={
                    day: ["08:00-20:00"]
                    for day in ["Monday","Tuesday","Wednesday",
                                "Thursday","Friday","Saturday","Sunday"]
                },
            )
            household.addMember(new_member)
            st.success(f"{m_name} added to household!")
            st.rerun()

    # Switch at the very bottom of the sidebar
    st.divider()
    if st.button("🔄 Switch Household / User", use_container_width=True):
        reset()


# ── MAIN: Greeting ─────────────────────────────────────────────────────────────
st.markdown(f"## {time_greeting()}, {owner.name}! 🐾")
st.caption(f"{datetime.today().strftime('%A, %B %d, %Y')}  ·  {household.name}")
st.divider()


# ── MAIN: Tasks ────────────────────────────────────────────────────────────────
st.subheader("Today's Tasks")

with st.expander("+ Add a task"):
    if not household.pets:
        st.info("Add a pet from the sidebar first.")
    else:
        pet_options    = {p.name: p for p in household.pets}
        member_options = {m.name: m for m in household.members}

        with st.form("add_task_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                task_type    = st.text_input("Task type", placeholder="Morning Walk")
                selected_pet = st.selectbox("Pet", list(pet_options.keys()))
            with col2:
                task_time   = st.time_input("Scheduled time", value=time(8, 0))
                assigned_to = st.selectbox("Assign to", list(member_options.keys()))

            add_task = st.form_submit_button("Add Task", use_container_width=True)

        if add_task and task_type:
            dt = datetime.today().replace(
                hour=task_time.hour, minute=task_time.minute, second=0, microsecond=0
            )
            new_task = Task(
                taskId=f"t{st.session_state.task_counter}",
                petId=pet_options[selected_pet].petId,
                taskType=task_type,
                scheduledTime=dt,
                assignedTo=member_options[assigned_to],
                status="scheduled",
            )
            st.session_state.tasks.append(new_task)
            st.session_state.task_counter += 1
            st.rerun()

sorted_tasks = sorted(st.session_state.tasks, key=lambda t: t.scheduledTime)

if not sorted_tasks:
    st.info("No tasks yet — add one above.")
else:
    # Header row
    h1, h2, h3, h4, h5, h6, h7, h8 = st.columns([2, 3, 2, 2, 2, 2, 3, 1])
    for col, label in zip(
        [h1, h2, h3, h4, h5, h6, h7, h8],
        ["Time", "Task", "Pet", "Assigned to", "Status", "Complete", "Ping", ""],
    ):
        col.markdown(f"**{label}**")
    st.divider()

    for task in sorted_tasks:
        with st.container(border=True):
            c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([2, 3, 2, 2, 2, 2, 3, 1])
            c1.write(task.scheduledTime.strftime("%I:%M %p"))
            c2.write(task.taskType)
            c3.write(pet_lookup.get(task.petId, "?"))
            c4.write(task.assignedTo.name)

            if task.status == "completed":
                c5.success("Done ✅")
            else:
                c5.warning(task.status)

            # Mark complete
            if task.status != "completed":
                if c6.button("✅ Complete", key=f"complete_{task.taskId}"):
                    task.markCompleted()
                    st.rerun()

            # Ping column — shows live notification status if one exists, button otherwise
            other_members = [m for m in household.members if m.userId != task.assignedTo.userId]
            task_notif = next(
                (n for n in reversed(st.session_state.notifications) if n.taskId == task.taskId),
                None,
            )
            if task_notif:
                if task_notif.status == "sent":
                    c7.info("⏳ Pending")
                elif task_notif.status == "accepted":
                    c7.success("✅ Accepted")
                elif task_notif.status == "declined":
                    c7.error("❌ Declined")
            elif other_members and task.status != "completed":
                if c7.button("📣 Ping member", key=f"ping_{task.taskId}"):
                    st.session_state.pinging_task_id = task.taskId
                    st.rerun()

            # Delete
            if c8.button("🗑️", key=f"delete_{task.taskId}"):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks if t.taskId != task.taskId
                ]
                st.rerun()


# ── MAIN: Ping Form ────────────────────────────────────────────────────────────
if st.session_state.pinging_task_id:
    task_to_ping = next(
        (t for t in st.session_state.tasks if t.taskId == st.session_state.pinging_task_id),
        None,
    )
    if task_to_ping:
        other_members  = [m for m in household.members if m.userId != task_to_ping.assignedTo.userId]
        member_options = {m.name: m for m in other_members}

        st.divider()
        st.subheader(f"📣 Ping about: {task_to_ping.taskType}")

        with st.form("ping_form"):
            to_member = st.selectbox("Send to", list(member_options.keys()))
            message   = st.text_area(
                "Message",
                placeholder=f"Hey, can you take care of the {task_to_ping.taskType}?",
            )
            col_send, col_cancel = st.columns(2)
            send   = col_send.form_submit_button("Send ping",  use_container_width=True)
            cancel = col_cancel.form_submit_button("Cancel",   use_container_width=True)

        if send and message:
            notif = Notification(
                pingId=f"n{st.session_state.notif_counter}",
                taskId=task_to_ping.taskId,
                fromUser=owner,
                toUser=member_options[to_member],
                message=message,
                status="pending",
                createdAt=datetime.now(),
            )
            notif.sendPing()
            st.session_state.notifications.append(notif)
            st.session_state.notif_counter += 1
            st.session_state.pinging_task_id = None
            st.rerun()

        if cancel:
            st.session_state.pinging_task_id = None
            st.rerun()


# ── MAIN: Notifications ────────────────────────────────────────────────────────
if st.session_state.notifications:
    st.divider()
    st.subheader("📬 Notifications")
    for notif in reversed(st.session_state.notifications):
        task_name = next(
            (t.taskType for t in st.session_state.tasks if t.taskId == notif.taskId),
            "Unknown task",
        )
        with st.expander(f"To {notif.toUser.name}  ·  {task_name}  ·  {notif.status}"):
            st.write(f"**From:** {notif.fromUser.name}")
            st.write(f"**Message:** {notif.message}")
            st.write(f"**Sent:** {notif.createdAt.strftime('%I:%M %p')}")

            if notif.status == "sent":
                col_a, col_d, _ = st.columns([1, 1, 2])
                if col_a.button("Accept",  key=f"accept_{notif.pingId}"):
                    notif.acceptPing()
                    st.rerun()
                if col_d.button("Decline", key=f"decline_{notif.pingId}"):
                    notif.declinePing()
                    st.rerun()

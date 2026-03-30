import warnings
from datetime import datetime, time
from pawpal_system import User, Household, Pet, Task, Notification, Scheduler
import streamlit as st

st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
    background: #FFFAF7;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #FBF0EA !important;
    border-right: 1px solid #EDD8CC;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container {
    padding-top: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

/* ── Hero banner ── */
.hero-banner {
    background: #F0997B;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    top: -60px; right: 120px;
}
.hero-banner::after {
    content: '';
    position: absolute;
    width: 130px; height: 130px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    top: 20px; right: 30px;
}
.hero-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
}
.hero-greeting {
    font-size: 1.5rem;
    font-weight: 500;
    color: #fff;
    margin: 0;
}
.hero-sub {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.75);
    margin: 4px 0 0;
}
.hero-stats {
    display: flex;
    gap: 10px;
    margin-top: 14px;
}
.stat-pill {
    background: rgba(255,255,255,0.2);
    border-radius: 99px;
    padding: 5px 14px;
    font-size: 0.75rem;
    color: #fff;
    display: inline-flex;
    align-items: center;
    gap: 7px;
}
.stat-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
}

/* ── Section title ── */
.section-title {
    font-size: 0.8rem;
    font-weight: 500;
    color: #3A2E2A;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}

/* ── Column headers ── */
.col-headers {
    display: grid;
    grid-template-columns: 90px 1fr 90px 130px 140px;
    gap: 10px;
    padding: 0 14px;
    margin-bottom: 6px;
}
.col-h {
    font-size: 0.68rem;
    color: #C4B4AC;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Task row cards ── */
.task-row {
    display: grid;
    grid-template-columns: 90px 1fr 90px 130px 140px;
    gap: 10px;
    align-items: center;
    padding: 12px 14px;
    border-radius: 12px;
    margin-bottom: 8px;
    font-size: 0.85rem;
}
.tr-sage   { background: #EAF3DE; }
.tr-blush  { background: #FBEAF0; }
.tr-amber  { background: #FDF3E3; }
.tr-coral  { background: #FAECE7; }

.task-time { font-size: 0.78rem; color: #888780; font-variant-numeric: tabular-nums; }
.task-name { font-weight: 500; color: #2C2C2A; }
.task-pet  { color: #7A6560; font-size: 0.78rem; }
.task-assignee {
    display: flex; align-items: center; gap: 7px;
    color: #7A6560; font-size: 0.78rem;
}
.av {
    width: 20px; height: 20px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.6rem; font-weight: 500; flex-shrink: 0;
}
.av-p { background: #B5D4F4; color: #0C447C; }
.av-u { background: #FAEEDA; color: #633806; }

/* ── Status pills ── */
.status-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 11px; border-radius: 99px;
    font-size: 0.72rem; font-weight: 500;
}
.sp-sched  { background: #FAC775; color: #633806; }
.sp-done   { background: #C0DD97; color: #27500A; }
.sp-missed { background: #F5C4B3; color: #712B13; }
.sdot { width: 5px; height: 5px; border-radius: 50%; display: inline-block; }

/* ── Sidebar nav items ── */
.nav-item {
    display: flex; align-items: center; gap: 9px;
    padding: 8px 10px; border-radius: 10px;
    font-size: 0.85rem; color: #7A6560;
    cursor: pointer; margin-bottom: 4px;
}
.nav-item.active {
    background: #F0997B; color: #fff; font-weight: 500;
}
.nav-muted { color: #C4B4AC; font-size: 0.78rem; }
.sidebar-label {
    font-size: 0.65rem; color: #B4A49C;
    letter-spacing: 0.07em; text-transform: uppercase;
    padding: 0 4px; margin-bottom: 8px; margin-top: 4px;
    display: block;
}

/* ── Form styling ── */
[data-testid="stForm"] {
    background: #fff;
    border: 1px solid #EDD8CC;
    border-radius: 14px;
    padding: 1rem 1.25rem;
}
[data-testid="stForm"] label {
    font-size: 0.75rem !important;
    color: #B4A49C !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stForm"] input,
[data-testid="stForm"] select,
[data-testid="stForm"] [data-baseweb="select"] {
    border-radius: 8px !important;
    border-color: #E0D0C8 !important;
    background: #FFFAF7 !important;
    font-size: 0.85rem !important;
}
[data-testid="stFormSubmitButton"] button {
    background: #F0997B !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 0.4rem 1.5rem !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    background: #E8855F !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
defaults = {
    "household":        None,
    "tasks":            [],
    "notifications":    [],
    "task_counter":     1,
    "notif_counter":    1,
    "member_counter":   2,
    "pinging_task_id":  None,
    "pet_form_counter": 0,
    "pet_warning":      None,
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
# SETUP PHASE
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
# DASHBOARD PHASE
# ══════════════════════════════════════════════════════════════════════════════
household  = st.session_state.household
owner      = household.members[0]
pet_lookup = {p.petId: p.name for p in household.pets}

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;">
        <div style="width:32px;height:32px;border-radius:50%;background:#F0997B;
                    display:flex;align-items:center;justify-content:center;font-size:15px;">🏠</div>
        <span style="font-size:0.9rem;font-weight:500;color:#3A2E2A;">{household.name}</span>
    </div>
    """, unsafe_allow_html=True)

    # Members
    st.markdown('<span class="sidebar-label">Members</span>', unsafe_allow_html=True)
    for m in household.members:
        initials = m.name[0].upper()
        is_active = (m.userId == owner.userId)
        active_class = "active" if is_active else ""
        st.markdown(f"""
        <div class="nav-item {active_class}">
            <div class="av av-p">{initials}</div> {m.name}
        </div>
        """, unsafe_allow_html=True)

    with st.expander("+ Add member", expanded=False):
        with st.form("add_member_form_sidebar"):
            m_name  = st.text_input("Name",  placeholder="Alex", key="sidebar_member_name")
            m_email = st.text_input("Email", placeholder="alex@email.com", key="sidebar_member_email")
            m_phone = st.text_input("Phone", placeholder="555-2002", key="sidebar_member_phone")
            add_m   = st.form_submit_button("Add", use_container_width=True)

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
            st.success(f"{m_name} added!")
            st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Pets
    st.markdown('<span class="sidebar-label">Pets</span>', unsafe_allow_html=True)
    for p in household.pets:
        initials = p.name[0].upper()
        st.markdown(f"""
        <div class="nav-item">
            <div class="av av-u">{initials}</div> {p.name}
        </div>
        """, unsafe_allow_html=True)

    with st.expander("+ Add a pet", expanded=False):
        fc = st.session_state.pet_form_counter
        with st.form(f"sidebar_pet_form_{fc}"):
            s_pet_name  = st.text_input("Name",      placeholder="Mochi", key=f"pet_name_{fc}")
            s_pet_breed = st.text_input("Breed",     placeholder="Shiba Inu", key=f"pet_breed_{fc}")
            s_pet_age   = st.number_input("Age", min_value=0, max_value=30, value=1, key=f"pet_age_{fc}")
            s_vet_name  = st.text_input("Vet name",  placeholder="Dr. Kim", key=f"vet_name_{fc}")
            s_vet_phone = st.text_input("Vet phone", placeholder="555-9001", key=f"vet_phone_{fc}")
            add_pet_btn = st.form_submit_button("Add", use_container_width=True)

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
                st.session_state.pet_warning = f"⚠️ {s_pet_name} added, but incomplete vet info."
            st.session_state.pet_form_counter += 1
            st.rerun()

    if st.session_state.pet_warning:
        st.warning(st.session_state.pet_warning)
        st.session_state.pet_warning = None

    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Switch household", use_container_width=True):
        reset()


# ── MAIN: Hero ─────────────────────────────────────────────────────────────────
scheduler = Scheduler(household=household, tasks=st.session_state.tasks)
sorted_tasks = scheduler.sort_by_time()
done_count      = sum(1 for t in sorted_tasks if t.status == "completed")
scheduled_count = sum(1 for t in sorted_tasks if t.status == "scheduled")
today_str       = datetime.now().strftime("%A, %B %d · %Y")

st.markdown(f"""
<div class="hero-banner">
  <div class="hero-inner">
    <div>
      <p class="hero-greeting">{time_greeting()}, {owner.name}! 🐾</p>
      <p class="hero-sub">{today_str} · {household.name}</p>
      <div class="hero-stats">
        <span class="stat-pill">
          <span class="stat-dot" style="background:#C0DD97;"></span>{done_count} done
        </span>
        <span class="stat-pill">
          <span class="stat-dot" style="background:#FAC775;"></span>{scheduled_count} scheduled
        </span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN: Add Task Form ────────────────────────────────────────────────────────
with st.expander("＋  Add a task", expanded=False):
    if not household.pets:
        st.info("Add a pet from the sidebar first.")
    else:
        pet_options    = {p.name: p for p in household.pets}
        member_options = {m.name: m for m in household.members}

        with st.form("add_task_form"):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                task_type = st.text_input("Task type", placeholder="e.g. Morning Walk")
            with c2:
                task_time = st.time_input("Time", value=time(8, 0))
            with c3:
                selected_pet = st.selectbox("Pet", list(pet_options.keys()))
            with c4:
                assigned_to = st.selectbox("Assign to", list(member_options.keys()))

            add_task = st.form_submit_button("Save task", use_container_width=True)

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

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── MAIN: Task List ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Today\'s schedule</div>', unsafe_allow_html=True)

if not sorted_tasks:
    st.markdown("""
    <div style="text-align:center;padding:2rem;color:#C4B4AC;font-size:0.85rem;
                border:1px dashed #EDD8CC;border-radius:12px;">
        No tasks yet — add one above
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="col-headers">
        <span class="col-h">Time</span>
        <span class="col-h">Task</span>
        <span class="col-h">Pet</span>
        <span class="col-h">Assigned to</span>
        <span class="col-h">Status</span>
    </div>
    """, unsafe_allow_html=True)

    row_colors = ["tr-sage", "tr-blush", "tr-amber", "tr-coral"]
    status_pill_map = {
        "scheduled": '<span class="status-pill sp-sched"><span class="sdot" style="background:#BA7517;"></span>Scheduled</span>',
        "completed": '<span class="status-pill sp-done"><span class="sdot" style="background:#3B6D11;"></span>Done</span>',
    }

    for i, task in enumerate(sorted_tasks):
        color_class = row_colors[i % len(row_colors)]
        pill_html   = status_pill_map.get(task.status, "")
        initials    = task.assignedTo.name[0].upper()
        pet_name    = pet_lookup.get(task.petId, "?")

        st.markdown(f"""
        <div class="task-row {color_class}">
            <span class="task-time">{task.scheduledTime.strftime('%I:%M %p')}</span>
            <span class="task-name">{task.taskType}</span>
            <span class="task-pet">{pet_name}</span>
            <div class="task-assignee">
                <div class="av av-p">{initials}</div>
                {task.assignedTo.name}
            </div>
            <div>{pill_html}</div>
        </div>
        """, unsafe_allow_html=True)

        col_action1, col_action2 = st.columns([10, 1])
        with col_action2:
            if task.status != "completed":
                if st.button("✓", key=f"complete_{task.taskId}", help="Mark complete"):
                    task.markCompleted()
                    st.rerun()
            else:
                if st.button("✕", key=f"delete_{task.taskId}", help="Delete"):
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
            message   = st.text_area("Message", placeholder="Can you help with this task?")
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
                    for task in st.session_state.tasks:
                        if task.taskId == notif.taskId:
                            task.reassignTask(notif.toUser)
                            st.success(f"✅ Task reassigned to {notif.toUser.name}!")
                            break
                    st.rerun()
                if col_d.button("Decline", key=f"decline_{notif.pingId}"):
                    notif.declinePing()
                    st.rerun()

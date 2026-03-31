import warnings
from datetime import datetime, time
from pawpal_system import User, Household, Pet, Task, Notification, Scheduler
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Move sidebar to the right ─────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] {
    direction: rtl;
    left: auto !important;
    right: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    direction: ltr;
}
[data-testid="stSidebarCollapsedControl"] {
    left: auto !important;
    right: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500&display=swap');

html { font-size: 16px; }
body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'DM Sans', sans-serif !important;
    background: #FFFAF7 !important;
    font-size: 16px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #FBF0EA !important;
    border-right: 1px solid #EDD8CC !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
/* sidebar toggle always visible */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
    width: 240px !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container {
    padding-top: 0 !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

/* ── Setup card ── */
.setup-card {
    background: #fff;
    border: 1px solid #EDD8CC;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-top: 2rem;
}
.setup-title {
    font-size: 1.6rem;
    font-weight: 500;
    color: #2C2C2A;
    margin-bottom: 0.25rem;
    font-family: 'DM Sans', sans-serif;
}
.setup-sub {
    font-size: 0.9rem;
    color: #B4A49C;
    margin-bottom: 1.5rem;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hero banner ── */
.hero-banner {
    background: #F0997B;
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    top: -70px; right: 140px;
}
.hero-banner::after {
    content: '';
    position: absolute;
    width: 140px; height: 140px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    top: 20px; right: 30px;
}
.hero-inner { position: relative; }
.hero-greeting {
    font-size: 1.75rem;
    font-weight: 500;
    color: #fff;
    margin: 0;
    line-height: 1.2;
    font-family: 'DM Sans', sans-serif;
}
.hero-sub {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.8);
    margin: 6px 0 0;
    font-family: 'DM Sans', sans-serif;
}
.hero-stats { display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }
.stat-pill {
    background: rgba(255,255,255,0.2);
    border-radius: 99px;
    padding: 6px 16px;
    font-size: 0.85rem;
    color: #fff;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'DM Sans', sans-serif;
}
.stat-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

/* ── Section title ── */
.section-title {
    font-size: 0.72rem;
    font-weight: 500;
    color: #3A2E2A;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Column headers ── */
.col-headers {
    display: grid;
    grid-template-columns: 90px 1fr 70px 110px 120px;
    gap: 10px;
    padding: 0 16px;
    margin-bottom: 6px;
}
.col-h {
    font-size: 0.7rem;
    color: #C4B4AC;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-family: 'DM Sans', sans-serif;
}

/* ── Task row cards ── */
.task-row {
    display: grid;
    grid-template-columns: 90px 1fr 70px 110px 120px;
    gap: 10px;
    align-items: center;
    padding: 13px 16px;
    border-radius: 12px;
    margin-bottom: 7px;
    font-size: 0.95rem;
    font-family: 'DM Sans', sans-serif;
}
.tr-sage  { background: #EAF3DE; }
.tr-blush { background: #FBEAF0; }
.tr-amber { background: #FDF3E3; }
.tr-coral { background: #FAECE7; }

/* ── Unified row backgrounds (columns inside stHorizontalBlock) ── */
[data-testid="stHorizontalBlock"]:has(.row-sage)  { background: #EAF3DE !important; border-radius: 12px; padding: 10px 12px; margin-bottom: 7px; }
[data-testid="stHorizontalBlock"]:has(.row-blush) { background: #FBEAF0 !important; border-radius: 12px; padding: 10px 12px; margin-bottom: 7px; }
[data-testid="stHorizontalBlock"]:has(.row-amber) { background: #FDF3E3 !important; border-radius: 12px; padding: 10px 12px; margin-bottom: 7px; }
[data-testid="stHorizontalBlock"]:has(.row-coral) { background: #FAECE7 !important; border-radius: 12px; padding: 10px 12px; margin-bottom: 7px; }
/* Align items vertically within unified rows */
[data-testid="stHorizontalBlock"]:has([class^="row-"]) [data-testid="column"] { display: flex; align-items: center; }
/* Make selectbox inside row transparent */
[data-testid="stHorizontalBlock"]:has([class^="row-"]) [data-testid="stSelectbox"] [data-baseweb="select"] > div { background: transparent !important; }

.task-time  { font-size: 0.875rem; color: #888780; font-variant-numeric: tabular-nums; }
.task-name  { font-size: 0.95rem; font-weight: 500; color: #2C2C2A; }
.task-recur { font-size: 0.8rem; color: #B4A49C; }
.task-pet   { font-size: 0.875rem; color: #7A6560; }
.task-assignee {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.875rem; color: #7A6560;
}
.av {
    width: 22px; height: 22px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.65rem; font-weight: 500; flex-shrink: 0;
}
.av-p { background: #B5D4F4; color: #0C447C; }
.av-u { background: #FAEEDA; color: #633806; }

/* ── Status pills ── */
.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 11px; border-radius: 99px;
    font-size: 0.78rem; font-weight: 500;
    font-family: 'DM Sans', sans-serif;
    white-space: nowrap;
}
.sp-sched   { background: #FAC775; color: #633806; }
.sp-done    { background: #C0DD97; color: #27500A; }
.sp-pending { background: #B5D4F4; color: #0C447C; }
.sp-accept  { background: #C0DD97; color: #27500A; }
.sp-decline { background: #F5C4B3; color: #712B13; }
.sdot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; }

/* ── Conflict banner ── */
.conflict-banner {
    background: #FDF3E3;
    border: 1px solid #FAC775;
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 0.875rem;
    color: #633806;
    margin-bottom: 12px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar nav ── */
.nav-item {
    display: flex; align-items: center; gap: 9px;
    padding: 8px 10px; border-radius: 10px;
    font-size: 0.875rem; color: #7A6560;
    cursor: pointer; margin-bottom: 3px;
    font-family: 'DM Sans', sans-serif;
}
.nav-item.active { background: #F0997B; color: #fff; font-weight: 500; }
.sidebar-label {
    font-size: 0.68rem; color: #B4A49C;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 0 4px; margin-bottom: 6px; margin-top: 4px;
    display: block; font-family: 'DM Sans', sans-serif;
}

/* ── Form styling ── */
[data-testid="stForm"] {
    background: #fff !important;
    border: 1px solid #EDD8CC !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.5rem !important;
}
[data-testid="stForm"] label {
    font-size: 0.78rem !important;
    color: #B4A49C !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stForm"] input,
[data-testid="stForm"] select {
    border-radius: 8px !important;
    border-color: #E0D0C8 !important;
    background: #FFFAF7 !important;
    font-size: 0.95rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stFormSubmitButton"] button {
    background: #F0997B !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.75rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stFormSubmitButton"] button:hover { background: #E8855F !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid #EDD8CC !important;
    border-radius: 12px !important;
    background: #fff !important;
    margin-bottom: 0.75rem;
}
[data-testid="stExpander"] summary {
    font-size: 0.9rem !important;
    color: #7A6560 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Ping form ── */
.ping-card {
    background: #fff;
    border: 1px solid #EDD8CC;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
}
.ping-title {
    font-size: 1rem; font-weight: 500; color: #2C2C2A;
    margin-bottom: 0.75rem;
    font-family: 'DM Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
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
    if hour < 12:   return "Good morning"
    elif hour < 17: return "Good afternoon"
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
        st.markdown("""
        <div style="text-align:center;margin-top:3rem;margin-bottom:1rem;">
            <div style="width:56px;height:56px;border-radius:50%;background:#F0997B;
                        display:inline-flex;align-items:center;justify-content:center;
                        font-size:1.75rem;margin-bottom:0.75rem;">🐾</div>
            <div style="font-size:1.75rem;font-weight:500;color:#2C2C2A;
                        font-family:'DM Sans',sans-serif;">PawPal+</div>
            <div style="font-size:0.9rem;color:#B4A49C;margin-top:4px;
                        font-family:'DM Sans',sans-serif;">
                Let's set up your household.
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("setup_form"):
            col1, col2 = st.columns(2)
            with col1:
                owner_name     = st.text_input("Your name",      placeholder="Sarah")
                owner_email    = st.text_input("Email",          placeholder="sarah@email.com")
            with col2:
                owner_phone    = st.text_input("Phone",          placeholder="555-1001")
                household_name = st.text_input("Household name", placeholder="The Santos House")

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
    # Household header
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.25rem;">
        <div style="width:32px;height:32px;border-radius:50%;background:#F0997B;
                    display:flex;align-items:center;justify-content:center;font-size:15px;">🏠</div>
        <span style="font-size:0.95rem;font-weight:500;color:#3A2E2A;
                     font-family:'DM Sans',sans-serif;">{household.name}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Members ──
    st.markdown('<span class="sidebar-label">Members</span>', unsafe_allow_html=True)
    for m in household.members:
        is_owner = m.userId == owner.userId
        label = f"👑 {m.name}" if is_owner else f"👤 {m.name}"
        with st.expander(label):
            st.write(f"**Email:** {m.email or '—'}")
            st.write(f"**Phone:** {m.phone or '—'}")
            if not is_owner:
                if st.button("Remove member", key=f"rm_member_{m.userId}",
                             use_container_width=True):
                    household.removeMember(m.userId)
                    st.rerun()

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
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Pets ──
    st.markdown('<span class="sidebar-label">Pets</span>', unsafe_allow_html=True)
    if not household.pets:
        st.markdown('<div style="font-size:0.82rem;color:#C4B4AC;padding:4px 10px;'
                    'font-family:\'DM Sans\',sans-serif;">No pets yet.</div>',
                    unsafe_allow_html=True)

    for pet in household.pets:
        with st.expander(f"🐾 {pet.name}"):
            st.write(f"**Breed:** {pet.breed or '—'}")
            st.write(f"**Age:** {pet.age}")
            st.write(f"**Vet:** {pet.vetName or '—'}")
            st.write(f"**Vet phone:** {pet.vetPhone or '—'}")
            if st.button("Remove pet", key=f"rm_pet_{pet.petId}",
                         use_container_width=True):
                pet.removePet(household)
                st.rerun()

    # Persistent vet warning (survives rerun)
    if st.session_state.pet_warning:
        st.warning(st.session_state.pet_warning)
        st.session_state.pet_warning = None

    with st.expander("+ Add a pet"):
        fc = st.session_state.pet_form_counter
        with st.form(f"sidebar_pet_form_{fc}"):
            s_pet_name  = st.text_input("Name",      placeholder="Mochi",    key=f"pn_{fc}")
            s_pet_breed = st.text_input("Breed",     placeholder="Shiba Inu",key=f"pb_{fc}")
            s_pet_age   = st.number_input("Age", min_value=0, max_value=30,
                                          value=1,                            key=f"pa_{fc}")
            s_vet_name  = st.text_input("Vet name",  placeholder="Dr. Kim (optional)", key=f"vn_{fc}")
            s_vet_phone = st.text_input("Vet phone", placeholder="555-9001 (optional)",key=f"vp_{fc}")
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
                st.session_state.pet_warning = (
                    f"⚠️ {s_pet_name} added, but vet info is incomplete — recommended."
                )
            st.session_state.pet_form_counter += 1
            st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("🔄 Switch Household / User", use_container_width=True):
        reset()


# ── MAIN: Hero banner ──────────────────────────────────────────────────────────
tasks = st.session_state.tasks

done_count      = sum(1 for t in tasks if t.status == "completed")
scheduled_count = sum(1 for t in tasks if t.status == "scheduled")

greeting  = time_greeting()
today_str = datetime.today().strftime("%A, %B %d") + f"  ·  {household.name}"

st.markdown(f"""
<div class="hero-banner">
  <div class="hero-inner">
    <p class="hero-greeting">{greeting}, {owner.name}! 🐾</p>
    <p class="hero-sub">{today_str}</p>
    <div class="hero-stats">
      <span class="stat-pill">
        <span class="stat-dot" style="background:#C0DD97;"></span>{done_count} done
      </span>
      <span class="stat-pill">
        <span class="stat-dot" style="background:#FAC775;"></span>{scheduled_count} scheduled
      </span>
      <span class="stat-pill">
        <span class="stat-dot" style="background:#B5D4F4;"></span>{len(household.pets)} pet{"s" if len(household.pets) != 1 else ""}
      </span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── MAIN: Add task expander ────────────────────────────────────────────────────
with st.expander("＋  Add a task"):
    if not household.pets:
        st.info("Add a pet from the sidebar first.")
    else:
        pet_options    = {p.name: p for p in household.pets}
        member_options = {m.name: m for m in household.members}

        with st.form("add_task_form", clear_on_submit=True):
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                task_type = st.text_input("Task type", placeholder="Morning Walk")
            with c2:
                task_time_val = st.time_input("Scheduled time", value=time(8, 0))
            with c3:
                selected_pet = st.selectbox("Pet", list(pet_options.keys()))
            with c4:
                assigned_to = st.selectbox("Assign to", list(member_options.keys()))
            with c5:
                task_recurrence = st.selectbox("Recurrence", ["None", "daily", "weekly"])

            if st.form_submit_button("Save task") and task_type:
                dt = datetime.today().replace(
                    hour=task_time_val.hour,
                    minute=task_time_val.minute,
                    second=0, microsecond=0,
                )
                new_task = Task(
                    taskId=f"t{st.session_state.task_counter}",
                    petId=pet_options[selected_pet].petId,
                    taskType=task_type,
                    scheduledTime=dt,
                    assignedTo=member_options[assigned_to],
                    status="scheduled",
                    recurrence=None if task_recurrence == "None" else task_recurrence,
                )
                st.session_state.tasks.append(new_task)
                st.session_state.task_counter += 1
                st.rerun()

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


# ── MAIN: Sort & Filter ────────────────────────────────────────────────────────
scheduler = Scheduler(household=household, tasks=st.session_state.tasks)

# Conflict detection
conflicts = scheduler.detect_conflicts()
if conflicts:
    conflict_lines = "".join(f"<div>• {c}</div>" for c in conflicts)
    st.markdown(f"""
    <div class="conflict-banner">
        ⚠️ <strong>Scheduling conflicts detected</strong>{conflict_lines}
    </div>
    """, unsafe_allow_html=True)

col_sort, col_filter, col_filter_val = st.columns([1, 1, 1])
with col_sort:
    sort_option = st.selectbox(
        "Sort by",
        ["Time (earliest first)", "Time (latest first)", "Assignee", "Pet"],
        key="sort_select",
        label_visibility="collapsed",
    )
with col_filter:
    filter_option = st.selectbox(
        "Filter by",
        ["All", "Scheduled", "Completed", "By Pet", "By Member"],
        key="filter_select",
        label_visibility="collapsed",
    )
filter_value = None
with col_filter_val:
    if filter_option == "By Pet" and household.pets:
        filter_value = st.selectbox("Select pet",    [p.name for p in household.pets],
                                    key="filter_pet",    label_visibility="collapsed")
    elif filter_option == "By Member":
        filter_value = st.selectbox("Select member", [m.name for m in household.members],
                                    key="filter_member", label_visibility="collapsed")

# Apply sort
if sort_option == "Time (earliest first)":
    display_tasks = scheduler.sort_by_time()
elif sort_option == "Time (latest first)":
    display_tasks = list(reversed(scheduler.sort_by_time()))
elif sort_option == "Assignee":
    display_tasks = sorted(scheduler.tasks, key=lambda t: t.assignedTo.name)
elif sort_option == "Pet":
    display_tasks = sorted(scheduler.tasks, key=lambda t: pet_lookup.get(t.petId, ""))
else:
    display_tasks = scheduler.sort_by_time()

# Apply filter
if filter_option == "Scheduled":
    display_tasks = [t for t in display_tasks if t.status == "scheduled"]
elif filter_option == "Completed":
    display_tasks = [t for t in display_tasks if t.status == "completed"]
elif filter_option == "By Pet" and filter_value:
    pid = next((p.petId for p in household.pets if p.name == filter_value), None)
    display_tasks = [t for t in display_tasks if t.petId == pid]
elif filter_option == "By Member" and filter_value:
    display_tasks = [t for t in display_tasks if t.assignedTo.name == filter_value]


# ── MAIN: Task table ───────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Today\'s schedule</div>', unsafe_allow_html=True)

if not display_tasks:
    st.markdown("""
    <div style="text-align:center;padding:2.5rem;color:#C4B4AC;font-size:1rem;
                border:1px dashed #EDD8CC;border-radius:12px;
                font-family:'DM Sans',sans-serif;">
        No tasks match — add one above or adjust filters.
    </div>
    """, unsafe_allow_html=True)
else:
    # Column headers
    hdr_cols = st.columns([1.2, 3, 0.9, 1.3, 1.5, 1.8, 0.5])
    for ci, label in enumerate(["Time", "Task", "Recur", "Pet", "Assigned to", "Status", ""]):
        with hdr_cols[ci]:
            st.markdown(f'<span class="col-h">{label}</span>', unsafe_allow_html=True)

    row_colors = ["sage", "blush", "amber", "coral"]

    for i, task in enumerate(display_tasks):
        color_name   = row_colors[i % len(row_colors)]
        pet_name     = pet_lookup.get(task.petId, "?")
        initials     = task.assignedTo.name[0].upper()
        recur_label  = task.recurrence.capitalize() if task.recurrence else "—"

        other_members = [m for m in household.members
                         if m.userId != task.assignedTo.userId]
        task_notif    = next(
            (n for n in reversed(st.session_state.notifications)
             if n.taskId == task.taskId),
            None,
        )

        c_time, c_task, c_recur, c_pet, c_assign, c_status, c_del = st.columns([1.2, 3, 0.9, 1.3, 1.5, 1.8, 0.5])

        with c_time:
            st.markdown(
                f'<span class="row-{color_name}" style="display:none"></span>'
                f'<span class="task-time">{task.scheduledTime.strftime("%I:%M %p")}</span>',
                unsafe_allow_html=True,
            )
        with c_task:
            st.markdown(f'<span class="task-name">{task.taskType}</span>', unsafe_allow_html=True)
        with c_recur:
            st.markdown(f'<span class="task-recur">{recur_label}</span>', unsafe_allow_html=True)
        with c_pet:
            st.markdown(f'<span class="task-pet">{pet_name}</span>', unsafe_allow_html=True)
        with c_assign:
            st.markdown(
                f'<div class="task-assignee"><div class="av av-p">{initials}</div>'
                f'{task.assignedTo.name}</div>',
                unsafe_allow_html=True,
            )

        with c_status:
            if task.status == "completed":
                st.markdown('<span class="status-pill sp-done"><span class="sdot" style="background:#3B6D11;"></span>Done</span>', unsafe_allow_html=True)
            elif task_notif and task_notif.status == "accepted":
                st.markdown('<span class="status-pill sp-accept"><span class="sdot" style="background:#3B6D11;"></span>Accepted</span>', unsafe_allow_html=True)
            elif task_notif and task_notif.status == "declined":
                st.markdown('<span class="status-pill sp-decline"><span class="sdot" style="background:#712B13;"></span>Declined</span>', unsafe_allow_html=True)
            elif task_notif and task_notif.status == "sent":
                st.markdown('<span class="status-pill sp-pending"><span class="sdot" style="background:#0C447C;"></span>Pending</span>', unsafe_allow_html=True)
            else:
                options = ["Scheduled", "Completed", "Missed"]
                if other_members:
                    options.append("Ping 📣")
                new_status = st.selectbox(
                    "Status",
                    options,
                    key=f"status_{task.taskId}",
                    label_visibility="collapsed",
                )
                if new_status == "Completed":
                    if task.recurrence:
                        new_id = f"t{st.session_state.task_counter}"
                        scheduler.complete_and_recur(task, new_id)
                        st.session_state.task_counter += 1
                    else:
                        task.markCompleted()
                    st.rerun()
                elif new_status == "Missed":
                    task.status = "missed"
                    st.rerun()
                elif new_status == "Ping 📣":
                    st.session_state.pinging_task_id = task.taskId
                    st.rerun()

        with c_del:
            if st.button("✕", key=f"del_{i}", help="Delete task"):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks
                    if t.taskId != task.taskId
                ]
                st.rerun()


# ── MAIN: Ping form ────────────────────────────────────────────────────────────
if st.session_state.pinging_task_id:
    task_to_ping = next(
        (t for t in st.session_state.tasks
         if t.taskId == st.session_state.pinging_task_id),
        None,
    )
    if task_to_ping:
        other_members  = [m for m in household.members
                          if m.userId != task_to_ping.assignedTo.userId]
        member_options = {m.name: m for m in other_members}

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">📣 Ping about: {task_to_ping.taskType}</div>',
                    unsafe_allow_html=True)

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
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Notifications</div>', unsafe_allow_html=True)

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
                    # Reassign task to accepting member
                    for task in st.session_state.tasks:
                        if task.taskId == notif.taskId:
                            task.reassignTask(notif.toUser)
                            break
                    st.rerun()
                if col_d.button("Decline", key=f"decline_{notif.pingId}"):
                    notif.declinePing()
                    st.rerun()

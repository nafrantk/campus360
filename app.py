import json
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# CAMPUS360 — STUDENT DEVELOPMENT PLATFORM
# --------------------------------------------------
st.set_page_config(
    page_title="Campus360",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "student_performance_updated_1000.csv"
STATE_FILE = BASE_DIR / "campus360_data.json"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --canvas:#F6F5F0; --surface:#FFFFFF; --forest:#203C35; --sage:#D3E4B8; --muted:#737C74; --border:#E5E7DF; }
.stApp { background:var(--canvas); color:var(--forest); font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebar"] { background:#fff; border-right:1px solid var(--border); }
[data-testid="stSidebar"] > div:first-child { padding-top:1.2rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:var(--forest) !important; letter-spacing:-.5px; }
h1 { font-size:2.1rem !important; font-weight:800 !important; }
[data-testid="stMetric"] { background:#fff; border:1px solid var(--border); border-radius:16px; padding:18px !important; }
[data-testid="stMetricLabel"] { color:var(--muted) !important; }
[data-testid="stMetricValue"] { color:var(--forest) !important; font-family:'Manrope',sans-serif; font-weight:800; }
div.stButton > button, div.stFormSubmitButton > button { border-radius:10px; font-weight:600; min-height:42px; }
div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"] { background:var(--forest); color:white; border:1px solid var(--forest); }
div[data-testid="stVerticalBlockBorderWrapper"] { border-color:var(--border); border-radius:16px; }
[data-testid="stProgressBar"] > div > div { background:#78977E; border-radius:20px; }
hr { border-color:var(--border); }
@media (max-width:768px) { h1 { font-size:1.7rem !important; } [data-testid="stMetric"] { padding:12px !important; } }
</style>
""", unsafe_allow_html=True)


def default_state():
    return {
        "student": {
            "name": "Student", "student_id": "", "course": "BSc Data Science",
            "year": "Second Year", "goal": "Become a Data Scientist", "attendance": 85,
        },
        "subjects": [
            {"name": "Python Programming", "marks": 78, "attendance": 92},
            {"name": "Statistics", "marks": 62, "attendance": 80},
            {"name": "Machine Learning", "marks": 55, "attendance": 75},
            {"name": "Database Systems", "marks": 72, "attendance": 88},
        ],
        "tasks": [
            {"title": "Python mini project", "subject": "Python Programming", "due": "2026-11-05", "done": False},
            {"title": "Statistics assignment", "subject": "Statistics", "due": "2026-11-08", "done": False},
        ],
        "skills": {"Python": 3, "Statistics": 2, "SQL": 2, "Communication": 3, "Machine Learning": 1},
        "papers": [],
    }


def load_state():
    if STATE_FILE.exists():
        try:
            loaded = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            base = default_state()
            for key in base:
                if key in loaded:
                    base[key] = loaded[key]
            return base
        except (json.JSONDecodeError, OSError, TypeError):
            pass
    return default_state()


def save_state():
    STATE_FILE.write_text(json.dumps(st.session_state.campus, indent=2), encoding="utf-8")


if "campus" not in st.session_state:
    st.session_state.campus = load_state()
if "page_navigation" not in st.session_state:
    st.session_state.page_navigation = "Dashboard"
if "pending_navigation" not in st.session_state:
    st.session_state.pending_navigation = None

# Apply requested navigation before creating the radio widget.
if st.session_state.pending_navigation:
    st.session_state.page_navigation = st.session_state.pending_navigation
    st.session_state.pending_navigation = None

data = st.session_state.campus
student = data["student"]
subjects = data["subjects"]
tasks = data["tasks"]


def average_marks():
    if not subjects:
        return 0.0
    marks = [float(s.get("marks", 0) or 0) for s in subjects]
    return sum(marks) / len(marks)


def weak_subjects():
    return sorted(subjects, key=lambda s: float(s.get("marks", 0) or 0))[:3]


def heading(title, description):
    st.title(title)
    st.caption(description)


# Sidebar brand and navigation
st.sidebar.markdown("""
<div style="padding:4px 0 18px 0;">
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="background:#203C35;color:white;width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:22px;">🎓</div>
    <div>
      <div style="font-family:Manrope,sans-serif;font-size:25px;font-weight:800;letter-spacing:-1px;color:#203C35;">Campus360</div>
      <div style="font-size:10px;letter-spacing:1.2px;color:#737C74;">YOUR STUDENT SPACE</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("Your journey. All in one place.")

pages = ["Dashboard", "My Academics", "Tasks & Exams", "AI Study Mentor", "Skills & Career", "Ask Campus360", "My Profile"]
page = st.sidebar.radio("YOUR SPACE", pages, key="page_navigation")
st.sidebar.divider()
st.sidebar.caption("Prototype • Local student data")

# Dashboard
if page == "Dashboard":
    first_name = str(student.get("name", "Student")).strip().split()[0] or "Student"
    pending_tasks = [t for t in tasks if not t.get("done", False)]
    overdue_tasks = [t for t in pending_tasks if str(t.get("due", "")) < str(date.today())]
    avg = average_marks()
    attendance = float(student.get("attendance", 0) or 0)

    st.markdown(f"""
    <div style="padding:8px 0 20px 0;">
      <div style="color:#737C74;font-size:12px;letter-spacing:1.5px;font-weight:600;margin-bottom:10px;">{date.today().strftime('%A · %d %B %Y').upper()}</div>
      <div style="font-family:Manrope,sans-serif;font-size:clamp(27px,4vw,38px);font-weight:800;color:#203C35;letter-spacing:-1.5px;line-height:1.2;">Let's make today count, {first_name}.</div>
      <div style="margin-top:10px;color:#737C74;font-size:15px;">Your journey, your pace. Here's what needs your attention.</div>
    </div>
    """, unsafe_allow_html=True)

    if overdue_tasks:
        priority_title = "Let's clear an overdue task."
        priority_text = f"You have {len(overdue_tasks)} overdue task(s). Start by completing or rescheduling one."
        priority_icon = "↗"
    elif pending_tasks:
        priority_title = "One step forward."
        priority_text = f"You have {len(pending_tasks)} task(s) to work on. Choose one and make a little progress today."
        priority_icon = "✳"
    elif subjects and min(float(s.get("marks", 0) or 0) for s in subjects) < 60:
        weakest = min(subjects, key=lambda s: float(s.get("marks", 0) or 0))
        priority_title = f"Give {weakest['name']} some attention."
        priority_text = f"Your current mark is {float(weakest.get('marks', 0) or 0):.0f}%. A short, focused revision session is a good next step."
        priority_icon = "◎"
    else:
        priority_title = "Keep your momentum going."
        priority_text = "Review your goals, practise a skill, or explore a new topic today."
        priority_icon = "✳"

    st.markdown(f"""
    <div style="background:#203C35;border-radius:20px;padding:25px 27px;color:white;margin-bottom:22px;">
      <div style="color:#D3E4B8;font-size:11px;font-weight:700;letter-spacing:1.6px;margin-bottom:13px;">YOUR NEXT STEP</div>
      <div style="font-family:Manrope,sans-serif;font-size:23px;font-weight:800;letter-spacing:-.5px;margin-bottom:8px;">{priority_icon} &nbsp;{priority_title}</div>
      <div style="color:#E0E9E2;font-size:14px;line-height:1.7;max-width:650px;">{priority_text}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Your workspace")
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("＋  Add a task", use_container_width=True):
            st.session_state.pending_navigation = "Tasks & Exams"
            st.rerun()
    with a2:
        if st.button("✳  Study mentor", use_container_width=True):
            st.session_state.pending_navigation = "AI Study Mentor"
            st.rerun()
    with a3:
        if st.button("▤  View academics", use_container_width=True):
            st.session_state.pending_navigation = "My Academics"
            st.rerun()

    st.markdown("### Your progress")
    c1, c2, c3 = st.columns(3)
    c1.metric("Academic average", f"{avg:.1f}%")
    c2.metric("Overall attendance", f"{attendance:.0f}%")
    c3.metric("Tasks to do", len(pending_tasks), delta=f"{len(overdue_tasks)} overdue" if overdue_tasks else "No overdue tasks", delta_color="inverse" if overdue_tasks else "normal")

    left, right = st.columns([1.2, 1], gap="large")
    with left:
        st.markdown("### Academic snapshot")
        if subjects:
            chart = pd.DataFrame(subjects).copy()
            chart["marks"] = pd.to_numeric(chart["marks"], errors="coerce").fillna(0)
            st.bar_chart(chart.set_index("name")[["marks"]], height=260)
        else:
            st.info("Your academic journey starts here. Add subjects in My Academics.")
    with right:
        st.markdown("### What needs attention?")
        if subjects:
            for subject in weak_subjects():
                mark = max(0.0, min(100.0, float(subject.get("marks", 0) or 0)))
                st.markdown(f"**{subject['name']}**")
                st.progress(mark / 100)
                st.caption(f"{mark:.0f}% · Current recorded mark")
        if attendance < 75:
            st.warning("Your profile attendance is below 75%. Check your institution's official attendance requirements.")
    st.markdown("### Coming up")
    if pending_tasks:
        for task in sorted(pending_tasks, key=lambda t: str(t.get("due", "")))[:5]:
            with st.container(border=True):
                tc, dc = st.columns([3, 1])
                tc.markdown(f"**{task.get('title', 'Untitled task')}**")
                tc.caption(task.get("subject", "General"))
                dc.caption("DUE")
                dc.markdown(f"**{task.get('due', 'No date')}**")
                if str(task.get("due", "")) < str(date.today()):
                    st.caption("Overdue")
    else:
        st.success("You're all caught up on your recorded tasks. Why not set a new learning goal?")
    st.caption("Your dashboard reflects your saved prototype data. Keep your records updated for more relevant suggestions.")

# My Academics
elif page == "My Academics":
    heading("📚 My Academics", "Track marks, attendance, and supplementary papers.")
    st.subheader("Subject Performance")
    if subjects:
        frame = pd.DataFrame(subjects)
        edited = st.data_editor(frame, num_rows="dynamic", use_container_width=True, key="subject_editor", column_config={
            "marks": st.column_config.NumberColumn("Marks (%)", min_value=0, max_value=100, step=1),
            "attendance": st.column_config.NumberColumn("Attendance (%)", min_value=0, max_value=100, step=1),
        })
        if st.button("Save Academic Changes", type="primary"):
            cleaned = edited.fillna("").to_dict(orient="records")
            for row in cleaned:
                row["name"] = str(row.get("name", "")).strip()
                for field in ("marks", "attendance"):
                    try:
                        row[field] = float(row.get(field, 0) or 0)
                    except (TypeError, ValueError):
                        row[field] = 0.0
            data["subjects"] = [r for r in cleaned if r["name"]]
            save_state()
            st.success("Academic records saved.")
            st.rerun()
    else:
        st.info("Add a subject below to begin.")
    st.subheader("➕ Add a Subject")
    with st.form("add_subject"):
        subject_name = st.text_input("Subject name")
        marks = st.number_input("Marks (%)", 0, 100, 60)
        subject_attendance = st.number_input("Subject attendance (%)", 0, 100, 80)
        if st.form_submit_button("Add Subject"):
            if subject_name.strip():
                data["subjects"].append({"name": subject_name.strip(), "marks": marks, "attendance": subject_attendance})
                save_state()
                st.success("Subject added.")
                st.rerun()
            else:
                st.error("Please enter a subject name.")
    st.subheader("📄 Supplementary / Back Papers")
    with st.form("add_paper"):
        paper_name = st.text_input("Paper or subject")
        attempt = st.text_input("Attempt / semester")
        paper_status = st.selectbox("Status", ["Needs preparation", "Preparing", "Cleared"])
        if st.form_submit_button("Save Paper"):
            if paper_name.strip():
                data["papers"].append({"subject": paper_name.strip(), "attempt": attempt.strip(), "status": paper_status})
                save_state()
                st.success("Paper record saved.")
                st.rerun()
            else:
                st.error("Enter a paper name.")
    if data["papers"]:
        st.dataframe(pd.DataFrame(data["papers"]), use_container_width=True)

# Tasks & Exams
elif page == "Tasks & Exams":
    heading("🗓️ Tasks & Exams", "Organise assignments, projects, and revision.")
    with st.form("new_task"):
        title = st.text_input("Task or assignment")
        subject_options = [s["name"] for s in subjects] or ["General"]
        task_subject = st.selectbox("Subject", subject_options)
        due = st.date_input("Due date")
        if st.form_submit_button("Add Task", type="primary"):
            if title.strip():
                data["tasks"].append({"title": title.strip(), "subject": task_subject, "due": str(due), "done": False})
                save_state()
                st.success("Task added.")
                st.rerun()
            else:
                st.error("Enter a task title.")
    st.subheader("Your Task List")
    if not tasks:
        st.info("Your task list is empty.")
    for i, task in enumerate(tasks):
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(f"**{task.get('title', 'Untitled task')}**")
            col1.caption(f"{task.get('subject', 'General')} · Due {task.get('due', 'No date')}")
            col2.write("Completed" if task.get("done", False) else "Pending")
            if col3.button("Undo" if task.get("done", False) else "Complete", key=f"task_{i}"):
                task["done"] = not task.get("done", False)
                save_state()
                st.rerun()
    st.caption("Exam tip: schedule revision sessions before your exam date.")

# Study Mentor
elif page == "AI Study Mentor":
    heading("🧠 Study Mentor", "Study suggestions based on your saved academic records.")
    st.info("This first prototype uses transparent recommendation rules. It does not connect to an external generative AI model.")
    st.subheader("Your Academic Risk Signals")
    low_marks = [s for s in subjects if float(s.get("marks", 0) or 0) < 60]
    low_attendance = [s for s in subjects if float(s.get("attendance", 0) or 0) < 75]
    if low_marks:
        for s in low_marks:
            st.warning(f"{s['name']}: marks are {float(s.get('marks', 0) or 0):.0f}%. Review core concepts and practise questions.")
    else:
        st.success("No subjects are below the 60% prototype threshold.")
    for s in low_attendance:
        st.warning(f"{s['name']}: attendance is {float(s.get('attendance', 0) or 0):.0f}%. Check your institution's attendance requirements.")
    st.subheader("📝 Generate a 7-Day Study Plan")
    focus = st.selectbox("What would you like to focus on?", ["Weakest subjects", "Exam revision", "Build programming skills"])
    hours = st.slider("Available study time per day (hours)", 1, 8, 3)
    if st.button("Create My Study Plan", type="primary"):
        priorities = weak_subjects()
        plans = {
            "Build programming skills": ["Python fundamentals and exercises", "Practise lists, dictionaries, and functions", "Solve beginner coding problems", "Learn Pandas and data cleaning", "Explore charts and data visualisation", "Build a small data analysis project", "Review your work and document progress"],
            "Exam revision": ["List exam topics and identify gaps", "Revise key definitions and concepts", "Practise short-answer questions", "Solve past-paper style questions", "Review mistakes and difficult topics", "Take a timed practice test", "Review summaries and prepare questions"],
        }
        plan = []
        for day in range(1, 8):
            if focus in plans:
                activity = plans[focus][day - 1]
            elif priorities:
                target = priorities[(day - 1) % len(priorities)]["name"]
                activity = f"Study {target}: concepts, notes, and practice"
            else:
                activity = "Review class notes and practise questions"
            plan.append({"Day": f"Day {day}", "Study activity": activity, "Daily target": f"{hours} hour(s)"})
        st.dataframe(pd.DataFrame(plan), hide_index=True, use_container_width=True)
        st.caption("This is a suggested schedule, not a guarantee of academic outcomes.")
    st.subheader("🧩 Quick Knowledge Check")
    quiz_subject = st.selectbox("Choose a practice question", ["Python", "Statistics", "Machine Learning"])
    questions = {
        "Python": {"question": "Which Python structure stores key-value pairs?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Dictionary", "explanation": "A dictionary maps keys to values."},
        "Statistics": {"question": "What is the median?", "options": ["The largest value", "The middle value in ordered data", "The sum of values", "The most frequent value only"], "answer": "The middle value in ordered data", "explanation": "The median is the central value after sorting."},
        "Machine Learning": {"question": "What is supervised learning trained on?", "options": ["Only unlabelled data", "Labelled examples", "No data", "Random answers"], "answer": "Labelled examples", "explanation": "Supervised learning uses input examples with target labels."},
    }
    q = questions[quiz_subject]
    st.write(f"**{q['question']}**")
    answer = st.radio("Select your answer", q["options"], key="mentor_quiz")
    if st.button("Check Answer"):
        if answer == q["answer"]:
            st.success("Correct! " + q["explanation"])
        else:
            st.error("Not quite. " + q["explanation"])

# Skills & Career
elif page == "Skills & Career":
    heading("🚀 Skills & Career", "Build a skills profile and explore possible career directions.")
    st.info("Career suggestions are heuristic examples based on self-rated skills, not validated career assessments.")
    st.subheader("Rate Your Skills")
    skills = data["skills"]
    for skill in list(skills.keys()):
        skills[skill] = st.slider(skill, 0, 5, int(skills[skill]), help="0 = beginner or no experience; 5 = highly confident", key=f"skill_{skill}")
    if st.button("Save Skills"):
        save_state()
        st.success("Skills saved.")
    st.subheader("Your Skill Profile")
    st.bar_chart(pd.DataFrame({"Skill level (0–5)": skills}).T)
    py = skills.get("Python", 0)
    stats = skills.get("Statistics", 0)
    sql = skills.get("SQL", 0)
    ml = skills.get("Machine Learning", 0)
    comm = skills.get("Communication", 0)
    careers = [
        ("Data Analyst", (py + stats + sql) / 3, "Practise SQL, data cleaning, dashboards, and communicating findings."),
        ("Machine Learning Engineer", (py + stats + ml) / 3, "Strengthen Python, mathematics, model evaluation, and deployment."),
        ("Business Intelligence Analyst", (sql + stats + comm) / 3, "Build reporting projects, SQL skills, dashboards, and presentations."),
    ]
    careers.sort(key=lambda x: x[1], reverse=True)
    st.subheader("Career Exploration")
    for name, score, advice in careers:
        with st.container(border=True):
            st.subheader(name)
            st.write(f"Skill alignment indicator: **{score:.1f}/5**")
            st.progress(max(0.0, min(1.0, score / 5)))
            st.caption(advice)
    st.subheader("💼 Placement Preparation")
    st.markdown("- Build two or three projects you can explain clearly.\n- Practise Python, SQL, statistics, and problem-solving.\n- Prepare examples that demonstrate teamwork and communication.\n- Keep your résumé accurate and focused on evidence of your skills.")

# Ask Campus360
elif page == "Ask Campus360":
    heading("💬 Ask Campus360", "Ask questions about your current academic profile and study planning.")
    st.info("This initial assistant uses local rules and keywords. It is not yet a free-form chatbot.")
    question = st.text_input("What would you like help with?", placeholder="e.g. Which subject should I focus on?")
    if st.button("Get Guidance", type="primary"):
        if not question.strip():
            st.warning("Please type a question first.")
        else:
            qtext = question.lower()
            weak = weak_subjects()
            if any(w in qtext for w in ["weak", "improve", "marks", "subject"]):
                if weak:
                    first = weak[0]
                    st.write(f"**Suggested priority:** {first['name']} ({float(first.get('marks', 0) or 0):.0f}%).")
                    st.write("Review one concept at a time, solve practice questions, and track mistakes after each session.")
                else:
                    st.write("Add subjects in My Academics for personalised guidance.")
            elif any(w in qtext for w in ["attendance", "absent", "classes"]):
                st.write(f"Your profile attendance is {student.get('attendance', 0)}%. Check your institution's official attendance policy.")
            elif any(w in qtext for w in ["career", "job", "placement", "skill"]):
                st.write(f"Your current goal is: {student.get('goal', '')}. Visit Skills & Career to review your skill profile and career ideas.")
            elif any(w in qtext for w in ["plan", "study", "schedule", "exam"]):
                st.write("Open Study Mentor, choose a study focus, and generate a seven-day plan based on your selected priorities.")
            elif any(w in qtext for w in ["task", "assignment", "deadline"]):
                st.write(f"You have {sum(not t.get('done', False) for t in tasks)} pending task(s). Open Tasks & Exams to manage them.")
            else:
                st.write("I can currently help with weak subjects, attendance, study planning, tasks, skills, and career exploration. Try asking about one of those areas.")

# My Profile
elif page == "My Profile":
    heading("👤 My Profile", "Personalise your student development workspace.")
    year_options = ["First Year", "Second Year", "Third Year", "Fourth Year", "Other"]
    with st.form("profile_form"):
        name = st.text_input("Full name", student.get("name", "Student"))
        student_id = st.text_input("Student ID", student.get("student_id", ""))
        course = st.text_input("Course / programme", student.get("course", "BSc Data Science"))
        current_year = student.get("year", "Second Year")
        year = st.selectbox("Academic year", year_options, index=year_options.index(current_year) if current_year in year_options else 1)
        goal = st.text_input("Career goal", student.get("goal", ""))
        attendance = st.slider("Overall attendance (%)", 0, 100, int(student.get("attendance", 85)))
        if st.form_submit_button("Save My Profile", type="primary"):
            student.update({"name": name.strip() or "Student", "student_id": student_id.strip(), "course": course.strip(), "year": year, "goal": goal.strip(), "attendance": attendance})
            save_state()
            st.success("Profile saved.")
            st.rerun()
    st.subheader("Your Platform Data")
    st.write(f"**Subjects recorded:** {len(subjects)}")
    st.write(f"**Tasks recorded:** {len(tasks)}")
    st.write(f"**Supplementary papers:** {len(data['papers'])}")
    st.caption("Your prototype records are stored locally in campus360_data.json inside your project folder.")
    st.download_button("Download My Student Data", data=json.dumps(data, indent=2), file_name="campus360_student_data.json", mime="application/json")

# Dataset status
with st.sidebar.expander("📂 Dataset status"):
    if DATA_FILE.exists():
        st.success("Student CSV detected.")
        try:
            csv_data = pd.read_csv(DATA_FILE)
            st.caption(f"{len(csv_data):,} rows · {len(csv_data.columns)} columns")
            st.caption("CSV is available for future academic analytics.")
        except Exception as exc:
            st.warning(f"CSV could not be read: {exc}")
    else:
        st.warning("Student CSV not found in the project folder.")
        st.caption("Copy student_performance_updated_1000.csv into the same folder as app.py.")

st.divider()
st.caption("Campus360 · Student Development Prototype · Use verified institutional records for real academic decisions.")

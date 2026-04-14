import streamlit as st
import requests
import json

# 🔥 CHANGE THIS after backend deploy
API_BASE_URL = "https://attendance-backend.onrender.com"

st.set_page_config(
    page_title="College Attendance Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #0d1117; color: #c9d1d9;}
    .stApp {font-family: 'Inter', sans-serif;}
    #MainMenu, footer, header {visibility: hidden;}

    .login-box {
        max-width: 420px;
        margin: 4rem auto;
        padding: 2.5rem;
        background: #161b22;
        border-radius: 16px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .card {
        background: #161b22;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 1rem;
    }

    .progress {
        height: 8px;
        border-radius: 20px;
        background: #21262d;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)


# 🔗 Test backend connection
try:
    res = requests.get(API_BASE_URL)
    st.caption(f"Backend status: {res.text}")
except:
    st.caption("⚠️ Backend not reachable")


def login_student(roll_no, dob):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/login",
            json={"roll_no": roll_no, "dob": dob},
            timeout=5
        )
        return response.json()
    except:
        # Fallback to local JSON
        with open('college_data.json') as f:
            data = json.load(f)

        student = next((s for s in data['students'] if s['roll_no'] == roll_no), None)

        if not student or student['dob'] != dob:
            return {"success": False, "message": "Invalid Roll No or DOB"}

        total_attended = sum(a['attended'] for a in student['attendance'].values())
        total_classes = sum(a['total_classes'] for a in student['attendance'].values())

        overall = round((total_attended / total_classes) * 100, 2) if total_classes else 0

        return {
            "success": True,
            "student": student,
            "attendance_summary": {
                "overall_percentage": overall,
                "total_subjects": len(student['attendance']),
                "subjects_at_risk": sum(
                    1 for s in student['attendance'].values() if s['percentage'] < 75
                )
            },
            "subjects": student['attendance']
        }


def get_color(p):
    if p >= 75:
        return "#3fb950"
    elif p >= 65:
        return "#d29922"
    return "#f85149"


# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# 🔐 Login Page
if not st.session_state.authenticated:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🎓 Student Portal")
    st.caption("Login to view your attendance")

    roll = st.text_input("Roll Number").upper().strip()
    dob = st.text_input("Date of Birth (DD-MM-YYYY)", type="password")

    if st.button("Login", type="primary", use_container_width=True):
        if roll and dob:
            res = login_student(roll, dob)
            if res.get("success"):
                st.session_state.authenticated = True
                st.session_state.data = res
                st.rerun()
            else:
                st.error(res.get("message", "Login failed"))
        else:
            st.warning("Please fill all fields")

    st.markdown('</div>', unsafe_allow_html=True)


# 📊 Dashboard
else:
    data = st.session_state.data
    student = data['student']
    summary = data['attendance_summary']
    subjects = data['subjects']

    st.title(f"👋 Welcome, {student['name']}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Overall Attendance", f"{summary['overall_percentage']}%")

    with col2:
        st.metric("Total Subjects", summary['total_subjects'])

    with col3:
        st.metric("At Risk", summary['subjects_at_risk'])

    st.divider()

    for code, subj in subjects.items():
        pct = subj['percentage']
        color = get_color(pct)

        st.markdown(f"""
        <div class="card">
            <b>{code}</b> — {subj['subject_name']}<br>
            <small>{subj['attended']} / {subj['total_classes']} classes</small><br><br>
            <div class="progress">
                <div class="progress-fill" style="width:{pct}%; background:{color};"></div>
            </div>
            <small style="color:{color}"><b>{pct}%</b></small>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.data = None
        st.rerun()
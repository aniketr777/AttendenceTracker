import streamlit as st
import requests
import json
import pandas as pd
import math
import datetime

API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="College Attendance Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #0d1117; color: #c9d1d9;}
    .stApp {font-family: 'Inter', sans-serif;}
    #MainMenu, footer {visibility: hidden;}

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


# Backend connection check removed per user request


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
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Overview"


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


# 📊 Main Application
else:
    data = st.session_state.data
    student = data['student']
    summary = data['attendance_summary']
    subjects = data['subjects']

    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("🎓 Navigation")
    st.sidebar.write(f"Welcome back, **{student['name'].split()[0]}**!")
    
    st.sidebar.divider()
    
    if st.sidebar.button("Dashboard Overview", use_container_width=True):
        st.session_state.current_page = "Dashboard Overview"
    if st.sidebar.button("Student Profile", use_container_width=True):
        st.session_state.current_page = "Student Profile"
    if st.sidebar.button("Detailed Subjects", use_container_width=True):
        st.session_state.current_page = "Detailed Subjects"
    if st.sidebar.button("Daily Timetable", use_container_width=True):
        st.session_state.current_page = "Daily Timetable"
    if st.sidebar.button("Attendance History", use_container_width=True):
        st.session_state.current_page = "Attendance History"

    st.sidebar.divider()
    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.data = None
        st.session_state.current_page = "Dashboard Overview"
        st.rerun()

    page = st.session_state.current_page

    # ---------------- PAGE RENDERING ----------------

    if page == "Dashboard Overview":
        st.title(f"👋 Dashboard Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Attendance", f"{summary['overall_percentage']}%")
        with col2:
            st.metric("Total Subjects", summary['total_subjects'])
        with col3:
            st.metric("Subjects at Risk", summary['subjects_at_risk'])

        st.divider()
        st.subheader("Attendance by Subject")
        
        # Create DataFrame for Chart
        chart_data = []
        for code, subj in subjects.items():
            chart_data.append({
                "Subject": code,
                "Percentage": subj['percentage']
            })
        df = pd.DataFrame(chart_data)
        if not df.empty:
            st.bar_chart(df.set_index("Subject"))
            
    elif page == "Student Profile":
        st.title("👤 Student Profile")
        
        st.markdown(f"""
        <div class="card" style="padding: 2rem;">
            <h2>{student['name']}</h2>
            <hr style="border-top:1px solid #30363d;">
            <p><strong>Roll No:</strong> {student['roll_no']}</p>
            <p><strong>Department:</strong> {student['department']}</p>
            <p><strong>Semester:</strong> {student['semester']}</p>
            <p><strong>Batch:</strong> {student['batch']}</p>
            <p><strong>Email ID:</strong> <a href="mailto:{student['email']}" style="color: #58a6ff;">{student['email']}</a></p>
        </div>
        """, unsafe_allow_html=True)

    elif page == "Detailed Subjects":
        st.title("📚 Detailed Subject Breakdown")

        for code, subj in subjects.items():
            pct = subj['percentage']
            color = get_color(pct)
            
            # Calculate classes needed for 75%
            total = subj['total_classes']
            attended = subj['attended']
            classes_needed = 0
            if pct < 75:
                # required format: (attended + x) / (total + x) >= 0.75
                max_classes_needed = max(0, math.ceil((0.75 * total - attended) / 0.25))
                classes_needed = max_classes_needed

            advice_text = ""
            if classes_needed > 0:
                advice_text = f"<br><small style='color:#f85149'>⚠️ Action needed: Attend {classes_needed} more consecutive classes to hit 75%.</small>"
            else:
                can_bunk = math.floor((attended - 0.75 * total) / 0.75)
                if can_bunk > 0:
                     advice_text = f"<br><small style='color:#3fb950'>✅ Safe status: May miss up to {can_bunk} upcoming classes safely.</small>"
                else:
                     advice_text = f"<br><small style='color:#d29922'>⚠️ Caution: Cannot miss any classes to remain above 75%.</small>"

            st.markdown(f"""
            <div class="card">
                <b>{code}</b> — {subj['subject_name']}<br>
                <small>{subj['attended']} / {subj['total_classes']} classes attended</small>
                {advice_text}
                <br><br>
                <div class="progress">
                    <div class="progress-fill" style="width:{pct}%; background:{color};"></div>
                </div>
                <small style="color:{color}"><b>{pct}%</b></small>
            </div>
            """, unsafe_allow_html=True)


    elif page == "Daily Timetable":
        st.title("⏰ Daily Timetable")
        
        # Mock Timetable
        timetable = {
            0: [("09:00", "10:00", "CS301"), ("10:00", "11:00", "CS302"), ("11:15", "12:30", "CS303")],
            1: [("09:00", "10:00", "CS304"), ("10:00", "11:00", "CS301"), ("13:30", "14:30", "CS302")],
            2: [("10:00", "11:00", "CS303"), ("11:15", "12:30", "CS304"), ("14:30", "15:30", "CS301")],
            3: [("09:00", "10:00", "CS302"), ("10:00", "11:00", "CS303"), ("11:15", "12:30", "CS304")],
            4: [("09:00", "10:00", "CS301"), ("11:15", "12:30", "CS302"), ("13:30", "14:30", "CS304")],
        }
        
        now = datetime.datetime.now()
        today_weekday = now.weekday()
        
        if today_weekday in timetable:
            todays_classes = timetable[today_weekday]
            st.write(f"**Schedule for Today ({now.strftime('%A')}):**")
            
            # Determine Next Class
            next_class_idx = -1
            current_time_str = now.strftime("%H:%M")
            for i, (start, end, subj) in enumerate(todays_classes):
                if current_time_str < end:
                    next_class_idx = i
                    break
                    
            for i, (start, end, subj) in enumerate(todays_classes):
                is_next = (i == next_class_idx)
                bg_color = "rgba(63, 185, 80, 0.2)" if is_next else "#161b22"
                border_col = "#3fb950" if is_next else "#30363d"
                badge = "🔥 NEXT CLASS" if is_next else ""
                st.markdown(f"""
                <div style="background:{bg_color}; padding:10px; border-radius:8px; border:1px solid {border_col}; margin-bottom:8px; display:flex; justify-content:space-between;">
                    <div><strong>{start} - {end}</strong> | {subj}</div>
                    <div style="color:#3fb950; font-weight:bold; font-size:0.8em;">{badge}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No classes scheduled for today! 🎉")


    elif page == "Attendance History":
        st.title("📅 Recent Attendance Timeline")
        
        # Mocking last 10 dates of attendance history
        history_data = []
        base_date = datetime.date.today()
        for i in range(10):
            date = base_date - datetime.timedelta(days=i)
            if date.weekday() < 5: # Monday to Friday
                status = 'Present' if (hash(student['roll_no'] + str(date)) % 100) < 85 else 'Absent'
                subject_idx = (i + hash(student['roll_no'])) % len(subjects)
                subject_code = list(subjects.keys())[subject_idx]
                history_data.append({
                    "Date": date,
                    "Subject": subject_code,
                    "Status": status
                })
                
        history_data = sorted(history_data, key=lambda x: x['Date'], reverse=True)
        
        for item in history_data:
            color = "#3fb950" if item['Status'] == 'Present' else "#f85149"
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding-left: 10px; margin-bottom: 10px; background: #161b22; padding-top:5px; padding-bottom:5px; padding-right:10px; border-radius: 4px;">
                <small style="color:#8b949e">{item['Date'].strftime('%d %b %Y, %A')}</small><br>
                <strong>{item['Subject']}</strong>: <span style="color:{color}">{item['Status']}</span>
            </div>
            """, unsafe_allow_html=True)

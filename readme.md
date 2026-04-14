
# Create requirements.txt
requirements = '''
flask==3.0.0
flask-cors==4.0.0
streamlit==1.28.0
requests==2.31.0
pandas==2.1.0
'''

with open('/mnt/kimi/output/requirements.txt', 'w') as f:
    f.write(requirements)

# Create README with setup instructions
readme = '''
# 🎓 College Attendance Management System

A modern, dark-themed attendance portal for college students with Flask backend and Streamlit frontend.

## 📁 Project Structure

```
college-attendance/
├── app.py                 # Flask Backend API
├── dashboard.py           # Streamlit Frontend
├── college_data.json     # Student Database
├── requirements.txt      # Python Dependencies
├── config.toml          # Streamlit Theme Config
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Flask Backend

```bash
python app.py
```
The API will run on `http://localhost:5000`

### 3. Start the Streamlit Frontend

```bash
streamlit run dashboard.py
```
The UI will open in your browser at `http://localhost:8501`

## 🔑 Test Credentials

| Roll Number | Date of Birth | Name | Status |
|-------------|---------------|------|--------|
| 2023CS1001 | 06-04-2005 | Saanvi Joshi | Check attendance |
| 2023CS1002 | 17-08-2002 | Arnav Kumar | Check attendance |
| 2023CS1003 | 12-11-2005 | Arnav Gupta | Check attendance |
| 2023CS1004 | 07-12-2005 | Vihaan Patel | Check attendance |
| 2023CS1005 | 27-02-2003 | Myra Gupta | Check attendance |
| 2023CS1006 | 08-07-2005 | Ayaan Joshi | Check attendance |
| 2023CS1007 | 18-06-2004 | Myra Banerjee | Check attendance |
| 2023CS1008 | 28-11-2004 | Nikhil Desai | Check attendance |
| 2023CS1009 | 03-06-2003 | Karan Singh | Check attendance |
| 2023CS1010 | 26-07-2002 | Vihaan Joshi | Check attendance |
| ... | ... | ... | ... |
| 2023CS1020 | 02-01-2002 | Aadhya Malhotra | Check attendance |

## 🎨 Features

### Backend (Flask API)
- **POST /api/login** - Authenticate student with roll number and DOB
- **GET /api/student/<roll_no>/attendance** - Get detailed attendance
- **GET /api/subjects** - Get all subjects list
- **GET /api/health** - Health check endpoint

### Frontend (Streamlit)
- 🔐 Secure login with Roll Number + DOB
- 📊 Real-time attendance dashboard
- ⚠️ 75% attendance threshold warnings
- 🎨 Dark VS Code-like modern theme
- 📱 Responsive card-based layout
- 📈 Visual progress bars for each subject
- 🔔 Alert system for low attendance
- 📋 Tabular view with sorting
- 📤 Easy logout functionality

## 🎯 Attendance Rules

- **≥ 75%**: Good Standing (Green)
- **65-74%**: At Risk (Yellow/Orange)
- **< 65%**: Critical (Red)

## 🔧 Configuration

### API URL
Update the `API_BASE_URL` in `dashboard.py` if deploying:
```python
API_BASE_URL = "https://your-api-domain.com"  # Production
```

### Theme Customization
Edit `.streamlit/config.toml` to customize colors:
```toml
[theme]
primaryColor = "#58a6ff"
backgroundColor = "#0d1117"
secondaryBackgroundColor = "#161b22"
textColor = "#c9d1d9"
```

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-CORS
- **Frontend**: Streamlit, Custom CSS
- **Data**: JSON (easily migratable to MongoDB/SQL)
- **Styling**: GitHub Dark Theme inspired design

## 📝 Notes

- The system works offline with local JSON data if API is unavailable
- All dates are in DD-MM-YYYY format
- Roll numbers are case-insensitive
- Session persists until logout

## 🚀 Deployment

### Backend (Flask)
Options: Heroku, PythonAnywhere, AWS, DigitalOcean

### Frontend (Streamlit)
Options: Streamlit Cloud, Heroku, AWS

---

Built for college attendance management with ❤️
'''

with open('/mnt/kimi/output/README.md', 'w') as f:
    f.write(readme)

print("✅ Requirements & README Created")
print("\n" + "="*60)
print("📦 SETUP COMPLETE")
print("="*60)
print("\n📂 Files Generated:")
print("   • college_data.json  - Student database with 20 records")
print("   • app.py             - Flask REST API backend")
print("   • dashboard.py       - Streamlit UI frontend")
print("   • requirements.txt   - Python dependencies")
print("   • config.toml        - Streamlit theme configuration")
print("   • README.md          - Documentation & setup guide")
print("\n🚀 To run the application:")
print("   1. Terminal 1: python app.py")
print("   2. Terminal 2: streamlit run dashboard.py")
print("\n🔑 Quick Test Login:")
print("   Roll No: 2023CS1001")
print("   DOB:     06-04-2005")

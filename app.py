from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

data = {
    "students": [
        {
            "roll_no": "2023CS1001",
            "name": "Saanvi Joshi",
            "dob": "06-04-2005",
            "department": "Computer Science",
            "semester": 3,
            "batch": "2023-2027",
            "email": "2023cs1001@college.edu.in",
            "attendance": {
                "CS301": {"subject_name": "Data Structures & Algorithms", "total_classes": 52, "attended": 42, "percentage": 80.77},
                "CS302": {"subject_name": "Database Management Systems", "total_classes": 48, "attended": 35, "percentage": 72.92},
                "CS303": {"subject_name": "Computer Networks", "total_classes": 45, "attended": 38, "percentage": 84.44},
                "CS304": {"subject_name": "Operating Systems", "total_classes": 50, "attended": 33, "percentage": 66.0}
            }
        },
        {
            "roll_no": "2023CS1002",
            "name": "Arnav Kumar",
            "dob": "17-08-2002",
            "department": "Computer Science",
            "semester": 3,
            "batch": "2023-2027",
            "email": "2023cs1002@college.edu.in",
            "attendance": {
                "CS301": {"subject_name": "Data Structures & Algorithms", "total_classes": 52, "attended": 40, "percentage": 76.92},
                "CS302": {"subject_name": "Database Management Systems", "total_classes": 48, "attended": 41, "percentage": 85.42},
                "CS303": {"subject_name": "Computer Networks", "total_classes": 45, "attended": 32, "percentage": 71.11},
                "CS304": {"subject_name": "Operating Systems", "total_classes": 50, "attended": 38, "percentage": 76.0}
            }
        }
    ],
    "subjects": [
        {"code": "CS301", "name": "Data Structures & Algorithms", "credits": 4, "semester": 3},
        {"code": "CS302", "name": "Database Management Systems", "credits": 4, "semester": 3},
        {"code": "CS303", "name": "Computer Networks", "credits": 3, "semester": 3},
        {"code": "CS304", "name": "Operating Systems", "credits": 3, "semester": 3}
    ]
}

@app.route('/api/login', methods=['POST'])
def login():
    try:
        req_data = request.get_json()
        roll_no = req_data.get('roll_no', '').strip().upper()
        dob = req_data.get('dob', '').strip()

        student = next((s for s in data['students'] if s['roll_no'] == roll_no), None) 

        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404

        if student['dob'] != dob:
            return jsonify({
                'success': False,
                'message': 'Invalid Date of Birth'
            }), 401

        total_attended = sum(att['attended'] for att in student['attendance'].values())
        total_classes = sum(att['total_classes'] for att in student['attendance'].values())
        overall_percentage = round((total_attended / total_classes) * 100, 2) if total_classes > 0 else 0

        low_attendance_subjects = [
            {
                'code': code,
                'name': att['subject_name'],
                'percentage': att['percentage']
            }
            for code, att in student['attendance'].items()
            if att['percentage'] < 75
        ]

        return jsonify({
            'success': True,
            'student': {
                'roll_no': student['roll_no'],
                'name': student['name'],
                'department': student['department'],
                'semester': student['semester'],
                'batch': student['batch'],
                'email': student['email']
            },
            'attendance_summary': {
                'overall_percentage': overall_percentage,
                'total_subjects': len(student['attendance']),
                'subjects_at_risk': len(low_attendance_subjects),
                'status': 'Good Standing' if overall_percentage >= 75 else 'Attendance Deficient'
            },
            'subjects': student['attendance'],
            'alerts': low_attendance_subjects
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/student/<roll_no>/attendance', methods=['GET'])
def get_attendance(roll_no):
    student = next((s for s in data['students'] if s['roll_no'] == roll_no.upper()), None)

    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404

    return jsonify({
        'success': True,
        'attendance': student['attendance']
    })

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    return jsonify({
        'success': True,
        'subjects': data['subjects']
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_students': len(data['students'])
    })

if __name__ == '__main__':
    print("Server running at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
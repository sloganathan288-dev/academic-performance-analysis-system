from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'academic_system_2024'
app.config['JSON_AS_ASCII'] = False

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

USERS_FILE = 'users.json'
RECORDS_FILE = 'records.json'

def load_json(filename):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return {}
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return {}

def save_json(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json(force=True)
        print(f"Registration data: {data}")
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        
        if not username or not password or not name:
            return jsonify({'success': False, 'message': 'All fields required'})
        
        users = load_json(USERS_FILE)
        
        if username in users:
            return jsonify({'success': False, 'message': 'Username exists'})
        
        users[username] = {'password': password, 'name': name}
        save_json(USERS_FILE, users)
        print(f"User registered: {username}")
        return jsonify({'success': True, 'message': 'Registration successful'})
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        print(f"Login data: {data}")
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'})
        
        users = load_json(USERS_FILE)
        print(f"Users: {list(users.keys())}")
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['name'] = users[username]['name']
            print(f"Login successful: {username}")
            return jsonify({'success': True, 'name': users[username]['name']})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/save_exam', methods=['POST'])
def save_exam():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    data = request.json
    records = load_json(RECORDS_FILE)
    
    exam_id = f"{data['department']}_{data['year']}_{data['internal']}_{data['subject']}_{data['date']}"
    
    students = data['students']
    present = [s for s in students if s['marks'] != '']
    absent = [s for s in students if s['marks'] == '']
    
    marks_list = [int(s['marks']) for s in present]
    
    analysis = {
        'total': len(students),
        'present': len(present),
        'absent': len(absent),
        'highest': max(marks_list) if marks_list else 0,
        'lowest': min(marks_list) if marks_list else 0,
        'average': round(sum(marks_list) / len(marks_list), 2) if marks_list else 0
    }
    
    ranked = sorted(present, key=lambda x: int(x['marks']), reverse=True)
    
    for student in ranked:
        mark = int(student['marks'])
        if mark >= analysis['average'] + 10:
            student['category'] = 'high'
        elif mark < analysis['average'] - 10:
            student['category'] = 'low'
        else:
            student['category'] = 'average'
    
    records[exam_id] = {
        'department': data['department'],
        'year': data['year'],
        'internal': data['internal'],
        'subject': data['subject'],
        'date': data['date'],
        'month': datetime.strptime(data['date'], '%Y-%m-%d').strftime('%B %Y'),
        'students': students,
        'analysis': analysis,
        'ranked': ranked,
        'teacher': session['name'],
        'timestamp': datetime.now().isoformat()
    }
    
    save_json(RECORDS_FILE, records)
    
    return jsonify({
        'success': True,
        'analysis': analysis,
        'ranked': ranked
    })

@app.route('/get_records', methods=['GET'])
def get_records():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    records = load_json(RECORDS_FILE)
    return jsonify({'success': True, 'records': list(records.values())})

@app.route('/filter_records', methods=['POST'])
def filter_records():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    filters = request.json
    records = load_json(RECORDS_FILE)
    
    filtered = []
    for record in records.values():
        match = True
        if filters.get('month') and record['month'] != filters['month']:
            match = False
        if filters.get('subject') and record['subject'] != filters['subject']:
            match = False
        if filters.get('year') and record['year'] != filters['year']:
            match = False
        if filters.get('internal') and record['internal'] != filters['internal']:
            match = False
        
        if match:
            filtered.append(record)
    
    return jsonify({'success': True, 'records': filtered})

@app.route('/get_alerts', methods=['GET'])
def get_alerts():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    records = load_json(RECORDS_FILE)
    student_performance = {}
    
    for record in records.values():
        for student in record['students']:
            if student['marks'] != '':
                name = student['name']
                if name not in student_performance:
                    student_performance[name] = []
                student_performance[name].append({
                    'marks': int(student['marks']),
                    'subject': record['subject'],
                    'internal': record['internal']
                })
    
    alerts = []
    for name, exams in student_performance.items():
        if len(exams) >= 2:
            avg = sum(e['marks'] for e in exams) / len(exams)
            if avg < 40:
                alerts.append({
                    'name': name,
                    'average': round(avg, 2),
                    'exams': len(exams)
                })
    
    return jsonify({'success': True, 'alerts': alerts})

if __name__ == '__main__':
    # Initialize JSON files if they don't exist
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
        print(f"Created {USERS_FILE}")
    if not os.path.exists(RECORDS_FILE):
        save_json(RECORDS_FILE, {})
        print(f"Created {RECORDS_FILE}")
    
    print("Starting Academic Assessment System...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000, host='127.0.0.1')

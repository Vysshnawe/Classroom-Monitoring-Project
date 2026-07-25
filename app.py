import os
import sqlite3
import subprocess
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'admin123'


UPLOAD_BASE = os.path.join('static', 'recordings')
OUTPUT_BASE = os.path.join('static', 'outputs')
DATASET_BASE = 'dataset'


for folder in [UPLOAD_BASE, OUTPUT_BASE, DATASET_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
   
    db = get_db()
    
    
    db.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   username TEXT NOT NULL, 
                   password TEXT NOT NULL)''')
    
    
    db.execute('''CREATE TABLE IF NOT EXISTS classrooms 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT NOT NULL UNIQUE)''')

   
    db.execute('''CREATE TABLE IF NOT EXISTS sessions 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   class_name TEXT, 
                   video_path TEXT, 
                   session_date TEXT, 
                   total_students INTEGER, 
                   avg_attentiveness REAL,
                   faculty_notes TEXT)''')
    
    
    db.execute('''CREATE TABLE IF NOT EXISTS journal 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   class_name TEXT, 
                   content TEXT, 
                   note_date TEXT, 
                   note_time TEXT)''')

   
    user = db.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not user:
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin123'))
    
    db.commit()
    db.close()

init_db()

def get_dataset_structure():
    structure = {}
    if os.path.exists(DATASET_BASE):
        for class_folder in os.listdir(DATASET_BASE):
            path = os.path.join(DATASET_BASE, class_folder)
            if os.path.isdir(path):
                structure[class_folder] = os.listdir(path)
    return structure



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        if user:
            session.clear()
            session['user'] = username
            row = db.execute('SELECT id FROM sessions ORDER BY id DESC LIMIT 1').fetchone()
            session['login_session_id'] = row['id'] if row else 0
            db.close()
            return redirect(url_for('dashboard'))
        else:
            db.close()
            flash("Invalid credentials!")
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    classes = db.execute('SELECT * FROM classrooms').fetchall()
    
    login_id = session.get('login_session_id', 0)
    latest = db.execute(
        'SELECT * FROM sessions WHERE id > ? ORDER BY id DESC LIMIT 1', (login_id,)
    ).fetchone()

    attn_label = None
    if latest:
        score = latest['avg_attentiveness']
        if score >= 80:
            attn_label = "Excellent"
        elif score >= 50:
            attn_label = "Stable"
        else:
            attn_label = "Poor"

    db.close()
    return render_template('dashboard.html', latest=latest, classes=classes, attn_label=attn_label)
    
    
    
@app.route('/analyze', methods=['POST'])
def analyze():
    print("ANALYZE BUTTON CLICKED")
    if 'user' not in session: return redirect(url_for('login'))
    
    class_name = request.form.get('class_name')
    video = request.files.get('video')

    if not video or not class_name:
        flash("Please select a class and upload a video.")
        return redirect(url_for('dashboard'))

    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_folder = f"{class_name.replace(' ', '_')}_{timestamp}"
    
    
    save_path = os.path.join(UPLOAD_BASE, session_folder)
    os.makedirs(save_path, exist_ok=True)
    
    video_filename = "input_video.mp4"
    video_full_path = os.path.join(save_path, video_filename)
    video.save(video_full_path)

   
    output_path = os.path.join(OUTPUT_BASE, session_folder)
    os.makedirs(output_path, exist_ok=True)

    
    dataset_path = os.path.join(DATASET_BASE, class_name.replace(' ', '_'))

   
    try:
        subprocess.run([
            'python', 'main.py',
            video_full_path,   
            dataset_path,      
            output_path       
        ], check=True)
        session['analysis_started'] = True
        flash("Analysis started! Please wait for results to appear.", "info")
    except Exception as e:
        logger.error(f"Error starting analysis: {e}")
        flash("Failed to start analysis engine.")

    return redirect(url_for('dashboard'))

@app.route('/update_note', methods=['POST'])
def update_note():
    video_path = request.form.get('video_path')
    note = request.form.get('faculty_note')
    if video_path:
        db = get_db()
        db.execute('UPDATE sessions SET faculty_notes = ? WHERE video_path = ?', (note, video_path))
        db.commit()
        db.close()
        flash("Session note updated.", "success")
    return redirect(url_for('dashboard'))

@app.route('/dataset', methods=['GET', 'POST'])
def dataset():
    if 'user' not in session: return redirect(url_for('login'))
    db = get_db()
    
    if request.method == 'POST':
        class_name = request.form.get('class_name')
        images = request.files.getlist('student_images')
        
        if class_name and images:
            target_dir = os.path.join(DATASET_BASE, class_name.replace(" ", "_"))
            os.makedirs(target_dir, exist_ok=True)
            
            count = 0
            for img in images:
                if img.filename:
                    img.save(os.path.join(target_dir, img.filename))
                    count += 1
            flash(f"Successfully uploaded {count} images to {class_name}.", "success")

    classes = db.execute('SELECT * FROM classrooms').fetchall()
    structure = get_dataset_structure()
    db.close()
    return render_template('dataset.html', classes=classes, structure=structure)

@app.route('/attendance')
def attendance():
    if 'user' not in session: return redirect(url_for('login'))
    db = get_db()
    sessions = db.execute('SELECT * FROM sessions ORDER BY id DESC').fetchall()
    db.close()
    return render_template('attendance.html', sessions=sessions)

@app.route('/reports')
def reports():
    if 'user' not in session: return redirect(url_for('login'))
    db = get_db()
    latest = db.execute('SELECT * FROM sessions ORDER BY id DESC LIMIT 1').fetchone()
    db.close()
    return render_template('reports.html', latest=latest)

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if 'user' not in session: return redirect(url_for('login'))
    db = get_db()
    
    if request.method == 'POST':
        class_name = request.form.get('class_name')
        content = request.form.get('content')
        date_str = datetime.now().strftime("%d %b %Y")
        time_str = datetime.now().strftime("%I:%M %p")
        
        db.execute('INSERT INTO journal (class_name, content, note_date, note_time) VALUES (?, ?, ?, ?)',
                   (class_name, content, date_str, time_str))
        db.commit()
        flash("Journal entry saved.")

    entries = db.execute('SELECT * FROM journal ORDER BY id DESC').fetchall()
    classes = db.execute('SELECT * FROM classrooms').fetchall()
    db.close()
    return render_template('journal.html', journal_entries=entries, classes=classes)

@app.route('/download/attendance/<folder>')
def download_attendance(folder):
    path = os.path.join(OUTPUT_BASE, folder, 'attendance.csv')
    return send_file(path, as_attachment=True)

@app.route('/download/attentiveness/<folder>')
def download_attentiveness(folder):
    path = os.path.join(OUTPUT_BASE, folder, 'attentiveness.csv')
    return send_file(path, as_attachment=True)

@app.route('/clear_sessions')
def clear_sessions():
    if 'user' not in session: return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM sessions')
    db.commit()
    db.close()
    flash("All sessions cleared.", "info")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
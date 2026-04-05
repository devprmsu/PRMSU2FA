import os, cv2, face_recognition, json, time
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "prmsu_thesis_2026_final"

DB_FILE = "users.json"
FACES_DIR = "known_faces"

if not os.path.exists(FACES_DIR): os.makedirs(FACES_DIR)

def get_users():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, 'r') as f: return json.load(f)
    except: return {}

@app.route('/')
def index(): return render_template('login.html')

@app.route('/register_page')
def register_page(): return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    pw = request.form.get('password')
    fn = request.form.get('first_name')
    ln = request.form.get('last_name')
    
    cam = cv2.VideoCapture(0)
    # Burst capture: take 5 frames, save the last one for best exposure
    for i in range(5):
        ret, frame = cam.read()
        if ret and i == 4:
            path = os.path.join(FACES_DIR, f"{email}.jpg")
            cv2.imwrite(path, frame)
    cam.release()
    
    users = get_users()
    users[email] = {"password": pw, "first_name": fn, "last_name": ln}
    with open(DB_FILE, 'w') as f: json.dump(users, f)
    
    return jsonify({"status": "success"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    u, p = data.get('email'), data.get('password')
    users = get_users()
    if u in users and users[u]['password'] == p:
        session['temp_user'] = u
        return jsonify({"status": "success", "next": "/verify"})
    return jsonify({"status": "error", "message": "Invalid Credentials"}), 401

@app.route('/verify')
def verify_page():
    if 'temp_user' not in session: return redirect(url_for('index'))
    return render_template('verify.html')

@app.route('/run_face_scan', methods=['POST'])
def run_face_scan():
    u = session.get('temp_user')
    path = os.path.join(FACES_DIR, f"{u}.jpg")
    known = face_recognition.face_encodings(face_recognition.load_image_file(path))[0]
    
    cam = cv2.VideoCapture(0)
    found = False
    for _ in range(15):
        ret, frame = cam.read()
        if not ret: continue
        rgb = cv2.cvtColor(cv2.resize(frame, (0,0), fx=0.25, fy=0.25), cv2.COLOR_BGR2RGB)
        encs = face_recognition.face_encodings(rgb)
        if encs and face_recognition.compare_faces([known], encs[0], 0.5)[0]:
            found = True; break
    cam.release()
    
    if found:
        session['logged_in'] = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 401

@app.route('/home')
def home():
    if not session.get('logged_in'): return redirect(url_for('index'))
    u = get_users().get(session['temp_user'], {})
    return render_template('home.html', name=u.get('first_name'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__': app.run(debug=True)
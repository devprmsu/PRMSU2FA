import os, cv2, face_recognition, json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "prmsu_secure_2fa_2026"

DB_FILE = "users.json"
FACES_DIR = "known_faces"

if not os.path.exists(FACES_DIR): os.makedirs(FACES_DIR)

def get_users():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r') as f: return json.load(f)

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        face_path = os.path.join(FACES_DIR, f"{email}.jpg")
        cv2.imwrite(face_path, frame)
        users = get_users()
        users[email] = password
        with open(DB_FILE, 'w') as f: json.dump(users, f)
        cam.release()
        return jsonify({"status": "success", "message": "Account & Face Registered!"})
    
    cam.release()
    return jsonify({"status": "error", "message": "Camera access failed."}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')
    users = get_users()

    if email in users and users[email] == password:
        session['temp_user'] = email 
        return jsonify({"status": "success", "next": "/verify"})
    
    return jsonify({"status": "error", "message": "Invalid Email or Password!"}), 401

@app.route('/verify')
def verify_page():
    if 'temp_user' not in session: 
        return redirect(url_for('index'))
    return render_template('verify.html')

@app.route('/run_face_scan', methods=['POST'])
def run_face_scan():
    email = session.get('temp_user')
    face_path = os.path.join(FACES_DIR, f"{email}.jpg")
    
    if not os.path.exists(face_path):
        return jsonify({"status": "error", "message": "No face data found."}), 404

    img = face_recognition.load_image_file(face_path)
    known_encoding = face_recognition.face_encodings(img)[0]

    cam = cv2.VideoCapture(0)
    found = False
    for _ in range(25): # Try for ~5 seconds
        ret, frame = cam.read()
        if not ret: continue
        # Speed up processing by resizing frame
        small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        encs = face_recognition.face_encodings(rgb)
        if encs:
            match = face_recognition.compare_faces([known_encoding], encs[0], 0.5)
            if match[0]:
                found = True; break
            
    cam.release()
    if found:
        session['logged_in'] = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Face ID Match Failed!"}), 401

@app.route('/home')
def home():
    if not session.get('logged_in'): return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
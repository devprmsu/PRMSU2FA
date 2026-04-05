# 🛡️ PRMSU Secure 2FA System
### Biometric & Credential-Based Two-Factor Authentication
**Developed as a Research Thesis Project (2026)**

This project implements a robust **Two-Factor Authentication (2FA)** system using **Python Flask**, **OpenCV**, and the **Face Recognition** library. It provides a modern, "Glassmorphism" UI to bridge the gap between high-level security and user experience.

---

## 🚀 Features
* **Step 1: Secure Login** – Traditional Email/Password validation against a local JSON database.
* **Step 2: Face ID Verification** – Real-time biometric scanning using the webcam.
* **Registration System** – Automatically captures and encodes the user's face during account creation.
* **Session Guarding** – Prevents unauthorized users from bypassing the biometric step via URL manipulation.
* **Modern UI** – Built with Poppins typography, FontAwesome icons, and smooth CSS transitions.

---

## 🛠️ Tech Stack
* **Backend:** Python 3.12, Flask
* **Computer Vision:** Dlib, OpenCV, Face Recognition
* **Frontend:** HTML5, CSS3 (Glassmorphism), JavaScript (Fetch API)
* **Database:** Local JSON (Scalable to Firebase/MySQL)

---

## 📦 Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.12** installed. You will also need **CMake** installed on your system to compile the `dlib` library.

### 2. Clone the Repository
```bash
git clone [https://github.com/devprmsu/PRMSU2FA.git](https://github.com/devprmsu/PRMSU2FA.git)
cd PRMSU2FA
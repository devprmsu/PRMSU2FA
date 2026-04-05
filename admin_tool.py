import firebase_admin
from firebase_admin import credentials, auth
import os

# Init Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def manage():
    print("\n[1] Register New User\n[2] List Users\n[3] Exit")
    choice = input("Choice: ")
    
    if choice == '1':
        email = input("Email: ")
        pw = input("Password: ")
        auth.create_user(email=email, password=pw)
        print("User created. Now run the Photo Registration Tool.")
    elif choice == '2':
        for user in auth.list_users().iterate_all():
            photo = "✅" if os.path.exists(f"{user.email}.jpg") else "❌"
            print(f"{photo} {user.email}")
    elif choice == '3':
        exit()

if __name__ == "__main__":
    while True: manage()
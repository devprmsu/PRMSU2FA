import cv2

email = input("Enter email for this photo: ").strip()
cap = cv2.VideoCapture(0)

print("Look at the camera. Press 'S' to save your photo.")

while True:
    ret, frame = cap.read()
    cv2.imshow("Register Face", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f"{email}.jpg", frame)
        print(f"Saved {email}.jpg")
        break

cap.release()
cv2.destroyAllWindows()
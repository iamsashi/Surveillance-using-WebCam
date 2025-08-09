import cv2
import platform

# For sound
if platform.system() == "Windows":
    import winsound
else:
    import os

# Video Capture
cam = cv2.VideoCapture(0)

while cam.isOpened():
    # 1st Frame
    ret, frame1 = cam.read()
    # 2nd Frame
    ret, frame2 = cam.read()

    # Detecting Movement
    diff = cv2.absdiff(frame1, frame2)

    # Colour & Blur
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold & Dilate
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Monitor & Alarm
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Sound alert
        if platform.system() == "Windows":
            winsound.Beep(3000, 1000)  # Frequency: 3000 Hz, Duration: 1000 ms
            winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
        else:
            os.system('afplay alert.wav')  # macOS default audio player

    # Show feed
    cv2.imshow("Sashi's Personal CCTV", frame1)

    # Stop on key press '5'
    if cv2.waitKey(10) == ord('5'):
        break

cam.release()
cv2.destroyAllWindows()


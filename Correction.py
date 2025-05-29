import cv2  # open cv module
import imutils  # helper library of opencv like resizing image
import time  # pause and delay execution
import smtplib  # library to send emails
import ssl  # provides secure connection
from datetime import datetime  # current time
from email.message import EmailMessage  # for formatting email
import os  # to handle file path
import pyttsx3  # text to speech library to speak message

# Email configuration
EMAIL_SENDER = "thebasantaadhikari@gmail.com"  # sender email address
EMAIL_PASSWORD = "abc def ghi jkl"  # app password from email provider
EMAIL_RECEIVER = "ailurus2005@gmail.com"  # receiver email address

# function to speak a message when motion is detected
def speak_message():
    engine = pyttsx3.init()  # initialize the engine
    engine.say("Alert! Motion has been detected. Image has been saved and emailed.")  # message to speak
    engine.runAndWait()  # speak the message

# function to send email with attached image
def send_email_with_attachment(filename):
    msg = EmailMessage()  # create an email message
    msg['Subject'] = 'Motion Detected!'  # subject of the email
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content("Motion was detected. Please find the attached image.")  # body content

    with open(filename, 'rb') as f:
        file_data = f.read()  # read the image file
        file_name = os.path.basename(f.name)  # get only file name from full path
        msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)  # attach the image

    context = ssl.create_default_context()  # secure connection context
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:  # connect to Gmail SMTP server
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # login to email
        server.send_message(msg)  # send the message
        print(f"[INFO] Email sent to {EMAIL_RECEIVER} with image {file_name}")

camera = cv2.VideoCapture(0)  # open the camera
time.sleep(2)  # wait 2 sec before starting

first_frame = None  # variable to store first frame
print("[INFO] starting motion detection...")

while True:  # loop forever
    ret, frame = camera.read()  # read frame from camera
    if not ret:  # if frame not read correctly
        print("[ERROR] Failed to grab frame from camera.")
        break
    frame = imutils.resize(frame, width=500)  # resize the frame to width 500
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blur to remove noise

    if first_frame is None:
        first_frame = gray  # save the first frame to compare
        continue

    frame_delta = cv2.absdiff(first_frame, gray)  # difference between first and current frame
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]  # threshold the difference
    thresh = cv2.dilate(thresh, None, iterations=2)  # thicken white area (motion)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # find motion area
    motion_detected = False  # flag for motion detection

    for contour in contours:
        if cv2.contourArea(contour) < 800:  # ignore small motion area
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(contour)  # get rectangle around motion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw green rectangle on motion

    if motion_detected:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # current time as string
        filename = f"motion_{timestamp}.jpg"  # image file name
        cv2.imwrite(filename, frame)  # save the image
        print(f"[INFO] Motion detected! Image saved as {filename}")
        speak_message()  # call function to speak message
        send_email_with_attachment(filename)  # send the image through email
        time.sleep(1)  # wait 1 sec to avoid multiple emails for same motion

camera.release()  # release camera
cv2.destroyAllWindows()  # close all windows

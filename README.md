#code for motion detection
import cv2  # open cv module
import imutils  # helper library of opencv like resizing image
import time  # pause and delay execution
import smtplib  # library to send emails
import ssl  # provides secure connection
from datetime import datetime  # current time
from email.message import EmailMessage  # for formatting email
import os  # to handle file path

# Email configuration
EMAIL_SENDER = "thebasantaadhikari@gmail.com"  # sender email address
EMAIL_PASSWORD = "xbmo dqog tten ieux"  # app password from email provider
EMAIL_RECEIVER = "ailurus2005@gmail.com"  # receiver email address

def send_email_with_attachment(filename):
    msg = EmailMessage()  # create an email message
    msg['Subject'] = 'Motion Detected!'  # subject of the email
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content("Motion was detected. Please find the attached image.")  # body content

    with open(filename, 'rb') as f:
        file_data = f.read()  # read the image file
        file_name = os.path.basename(f.name)  # get the image file name
        msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)  # attach the image

    context = ssl.create_default_context()  # secure context for email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:  # connect to Gmail SMTP server
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # login to email
        server.send_message(msg)  # send the message
        print(f"[INFO] Email sent to {EMAIL_RECEIVER} with image {file_name}")

camera = cv2.VideoCapture(0)  # tell opencv to open camera
time.sleep(2)  # sleep for 2 sec

first_frame = None  # store first image frame
print("[INFO] starting motion detection...")

while True:  # infinite loop open
    ret, frame = camera.read()  # ret is a boolean so if true frame capture image through read
    if not ret:
        print("[ERROR] Failed to grab frame from camera.")
        break
    frame = imutils.resize(frame, width=500)  # resize the image to 500 pixels
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert the image from color to grayscale (easier for motion detection)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # apply a blur to smooth the image and remove small changes like lighting flickers

    if first_frame is None:
        first_frame = gray  # store the gray image as first_frame
        continue

    frame_delta = cv2.absdiff(first_frame, gray)  # calculates the difference between first frame and current frame
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]  # convert the difference image into black and white
    thresh = cv2.dilate(thresh, None, iterations=2)  # makes white area thicker so motion is more visible

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # find the movement
    motion_detected = False  # variable to detect any motion

    for contour in contours:
        if cv2.contourArea(contour) < 800:  # accept image if movement is greater than 800 pixels
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(contour)  # boundingRect gives rectangle coordinates around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw a green rectangle around the motion area in the frame

    if motion_detected:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # get the current time
        filename = f"motion_{timestamp}.jpg"  # format file name
        cv2.imwrite(filename, frame)  # save the image
        print(f"[INFO] Motion detected! Image saved as {filename}")
        send_email_with_attachment(filename)  # call the email function to send the image
        time.sleep(1)  # wait for 1 second to avoid multiple emails for the same motion

camera.release()
cv2.destroyAllWindows()

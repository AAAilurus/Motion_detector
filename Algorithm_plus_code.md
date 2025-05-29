 1. Start the camera so it can take video.
-- camera = cv2.VideoCapture(0)

2. Wait a little bit so the camera gets ready.
--time.sleep(2)

3. Write down my email address and app password to send emails.
-EMAIL_SENDER = "thebasantaadhikari@gmail.com"
-EMAIL_PASSWORD = "abc def ghi jkl"  # your app password here

4. Write down the email address where you want to send alerts.
--EMAIL_RECEIVER = "ailurus2005@gmail.com"

5. Set up the email sending system with a safe connection.
--def send_email_with_attachment(filename):
    msg = EmailMessage()
    msg['Subject'] = 'Motion Detected!'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content("Motion was detected. Please find the attached image.")

    with open(filename, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(f.name)
        msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

 6. Take the very first picture from the camera.
--ret, frame = camera.read()

7. Change this picture to black and white (gray scale).
--gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

8. Blur the picture a little to ignore small light changes or noise.
gray = cv2.GaussianBlur(gray, (21, 21), 0)

9. Save this blurred gray picture as the background to compare with later pictures.
first_frame = gray

10. Start a loop that keeps taking new pictures from the camera again and again.
while True:
    ret, frame = camera.read()

    11. Make the new picture smaller so it’s faster to check.
    frame = imutils.resize(frame, width=500)

    12. Change the new picture to black and white.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    13. Blur this new picture the same way to reduce small changes.
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    14. Compare the new blurred gray picture with the first saved background picture.
    frame_delta = cv2.absdiff(first_frame, gray)

    16. Turn the difference picture into black and white — white means motion, black means no motion.
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    17. Make the white motion parts thicker so it’s easier to find.
    thresh = cv2.dilate(thresh, None, iterations=2)

    18. Find the outlines (contours) of the white motion parts.
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    19. For each motion part found, check how big it is.
    for contour in contours:
        area = cv2.contourArea(contour)

        20. If it’s too small (like small flickers), ignore it.
        if area < 800:
            continue

        21. If it’s big enough, say “motion detected.”
        motion_detected = True

        22. Draw a green rectangle around the motion part on the picture to show where the motion is.
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if motion_detected:
         23. Get the current date and time to make a unique file name.
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"motion_{timestamp}.jpg"

        24. Save the current picture with the green rectangle as an image file.
        cv2.imwrite(filename, frame)

         27. Send the email to the person I want to alert.
        send_email_with_attachment(filename)

        28. Wait for 1 second so I don’t send too many emails too fast.
        time.sleep(1)

    29. Keep repeating the loop to check for more motion.

31. When I want to stop, close the cam
32. era.
camera.release()

 33. Clean up all open windows and resources.
cv2.destroyAllWindows()


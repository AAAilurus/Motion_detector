What to do inside the code?

1. Start by preparing the system to capture video using the device's camera.
2. Wait for a short moment to let the camera stabilize.
3. Define the sender's email address and password (from Gmail app password).
4. Define the reciver's email address to send alerts.
5. Set up the email sending method with a secure connection.
6. Capture the very first frame from the camera.
7. Convert this frame to grayscale (black and white).
8. Apply a blur to this frame to remove small lighting changes or noise.
9. Save this as the "reference background frame" for comparing future frames.
10. Enter an infinite loop that repeatedly captures new frames from the camera.
11. Resize the frame to a smaller width to make processing faster.
12. Convert the current frame to grayscale.
13. Apply the same blur to reduce noise and small irrelevant changes.
14. Take the absolute difference between the new frame and the reference frame.
15. The result shows areas where pixels have changed — potential motion areas.
16. Apply a threshold to turn the difference into a binary image (white = motion, black = no motion).
17. Dilate (thicken) the white areas to make the motion zones clearer and more connected.
18. Identify the contours (shapes) of the white motion areas.
19. For each detected contour, check its size (area).
20. If it's smaller than a specific size (e.g., a small light flicker), ignore it.
21. If it's large enough, mark that motion has occurred.
22. Draw a rectangle around the detected motion area on the current frame for visual tracking (optional for display or debugging).
23. Get the current date and time to create a unique filename.
24. Save the current frame as an image with that filename.
25. Create an email with a subject and message saying motion was detected.
26. Attach the saved image file.
27. Send the email to the recipient.
28. Add a short pause (e.g., 1 second) to avoid sending too many emails if motion is detected continuously.
29. Keep looping to check for more motion.
30. You can choose to update the reference frame occasionally or after sending an alert, depending on your design.
31. When the loop ends (manually or through a break condition), release the camera.
32. Close all used resources and clean up.

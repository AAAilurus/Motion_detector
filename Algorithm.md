What to do inside the code:

1. Start the camera so it can take video.
2. Wait a little bit so the camera gets ready.
3. Write down my email address and app password to send emails.
4. Write down the email address where I want to send alerts.
5. Set up the email sending system with a safe connection.
6. Take the very first picture from the camera.
7. Change this picture to black and white (gray scale).
8. Blur the picture a little to ignore small light changes or noise.
9. Save this blurred gray picture as the background to compare with later pictures.
10. Start a loop that keeps taking new pictures from the camera again and again.
11. Make the new picture smaller so it’s faster to check.
12. Change the new picture to black and white.
13. Blur this new picture the same way to reduce small changes.
14. Compare the new blurred gray picture with the first saved background picture.
15. See where the pixels are different — that means there might be motion.
16. Turn the difference picture into black and white — white means motion, black means no motion.
17. Make the white motion parts thicker so it’s easier to find.
18. Find the outlines (contours) of the white motion parts.
19. For each motion part found, check how big it is.
20. If it’s too small (like small flickers), ignore it.
21. If it’s big enough, say “motion detected.”
22. Draw a green rectangle around the motion part on the picture to show where the motion is.
23. Get the current date and time to make a unique file name.
24. Save the current picture with the green rectangle as an image file.
25. Create an email message with a subject saying motion is detected.
26. Attach the saved image to the email.
27. Send the email to the person I want to alert.
28. Wait for 1 second so I don’t send too many emails too fast.
29. Keep repeating the loop to check for more motion.
30. Optionally, update the background picture sometimes or after sending an alert to adjust to changes.
31. When I want to stop, close the camera.
32. Clean up all open windows and resources.

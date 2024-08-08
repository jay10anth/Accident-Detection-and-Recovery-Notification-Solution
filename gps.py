import cv2
import time
from tkinter import *
from tkinter import messagebox

import folium as folium
import geocoder as geocoder
import pygame
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "roadaccident980@gmail.com"
toaddr = "roadaccident980@gmail.com"
from geopy.geocoders import Nominatim

# facial landmark predictor
pygame.init()

pygame.mixer.music.load("alarm.wav")
# Capturing Video
cap = cv2.VideoCapture("assets/test_0.mp4")
#cap = cv2.VideoCapture("assets/12.mp4")
#cap = cv2.VideoCapture("assets/1.mp4")
if not cap.isOpened():
    print("Initialising the capture...")
    cap.open("assets/accident.mp4")
    print("Done.")

# Subtracting the background
subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=20)

# Text setting up
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (40, 50)

# fontScale
fontScale = 0.8

# Blue color in BGR
color = (0, 0, 255)

# Line thickness of 2 px
thickness = 2

res = 1

arcount = 0

count = -1

while True:
    # Reading the frame
    res, frame = cap.read()

    if res == True:
        # Applying the mask
        mask = subtractor.apply(frame)

    # finding the contours
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Flag for accident detection
        flag = 0

        for cnts in contours:
            (x, y, w, h) = cv2.boundingRect(cnts)

            if w * h > 1000:
                if flag == 1:
                    # If accident detected change color if contours to red
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 0, 255), 3)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 255, 0), 3)

        # If area of rectangle more than a threshold detect accident
            if w * h > 10000:
                area = w * h
            # Countint the number of frames for which the condition persists to refine the accident detection case
                arcount += 1
            # print(arcount)
            if arcount > 35:
                flag = 1

        if flag == 1:
            # If accident detected print Accident on the screen
            frame = cv2.putText(frame, "Accident Detected ", org, font,
                                fontScale, color, thickness, cv2.LINE_AA, False)
            try:
                cv2.imwrite('img.jpg', frame)
                pygame.mixer.music.play()
                g = geocoder.ip('me')
                print(g.latlng)

                location = g.latlng

                map = folium.Map(location=location, zoom_start=10)
                folium.CircleMarker(location=location, radius=50, color="red").add_to(map)
                folium.Marker(location).add_to(map)

                map
                map.save("map1.html")
                # instance of MIMEMultipart
                msg = MIMEMultipart()

                # storing the senders email address
                msg['From'] = fromaddr

                # storing the receivers email address
                msg['To'] = toaddr

                # storing the subject
                msg['Subject'] = "Subject of the Mail"

                # string to store the body of the mail
                body = "Body_of_the_mail"

                # attach the body with the msg instance
                msg.attach(MIMEText(body, 'plain'))

                # open the file to be sent
                filename = "map1.html"
                attachment = open("map1.html", "rb")

                # instance of MIMEBase and named as p
                p = MIMEBase('application', 'octet-stream')

                # To change the payload into encoded form
                p.set_payload((attachment).read())

                # encode into base64
                encoders.encode_base64(p)

                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                # attach the instance 'p' to instance 'msg'
                msg.attach(p)
                filename = "img.jpg"
                attachment = open("img.jpg", "rb")

                # instance of MIMEBase and named as p
                p = MIMEBase('application', 'octet-stream')

                # To change the payload into encoded form
                p.set_payload((attachment).read())

                # encode into base64
                encoders.encode_base64(p)

                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                # attach the instance 'p' to instance 'msg'
                msg.attach(p)

                # creates SMTP session
                s = smtplib.SMTP('smtp.gmail.com', 587)

                # start TLS for security
                s.starttls()

                # Authentication
                s.login(fromaddr, "qsso gvea ivhy mcvj")

                # Converts the Multipart msg into a string
                text = msg.as_string()

                # sending the mail
                s.sendmail(fromaddr, toaddr, text)

                # terminating the session
                s.quit()
                #messagebox.showerror("Accident", "Accident Detected")


            except:
                pass
           # frame = cv2.putText(frame, "28° 35' 31.7040'' N and 77° 2' 45.7836'' E. ; ",
                               # (40, 80), font, fontScale, color, thickness, cv2.LINE_AA, False)
           # frame = cv2.putText(frame, "time:1600 hrs; ", (40, 100),
                               # font, fontScale, color, thickness, cv2.LINE_AA, False)
           # frame = cv2.putText(frame, "camera id:DWARKA_ROAD_22", (40, 120),
                               # font, fontScale, color, thickness, cv2.LINE_AA, False)

        cv2.imshow("Accident detection", frame)


        count += 1

        if cv2.waitKey(33) & 0xff == 27:
            break

    else:
        break
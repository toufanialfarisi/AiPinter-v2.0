
from sklearn.externals import joblib
from aipinter.camera.forms import ObjectDetectionForm
from sklearn.svm import LinearSVC
from aipinter.camera.hog import HOG 
from aipinter import dataset
from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify, Response
from flask_login import current_user, login_required
import argparse
import cv2
import mahotas
import face_recognition

cam = Blueprint('camera', __name__)


@cam.route('/camera', methods=['POST', 'GET'])
def camera():
    form_od = ObjectDetectionForm()
    if current_user.is_authenticated == False:
        flash('Please, login first', 'danger')
        return redirect(url_for('users.login'))
    else:
        if request.method == 'POST':
            data_cam = request.form['camera']
            if data_cam == 'SSD_Mobile_Net':
                req = 'ssd'
                return render_template('camera.html', form=form_od, req=req)
            elif data_cam == 'Ordinary_CNN':
                req = 'ord'
                return render_template('camera.html', form=form_od, req=req)
            
            else:
                req = 'norm'
                return render_template('camera.html', form=form_od, req=req)
        else:
            return render_template('camera.html', form=form_od, req='norm')

def gen():
    i=1
    while i<10:
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+str(i)+b'\r\n')
        i+=1

def get_frame_od():
    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object

    i=1

    parser = argparse.ArgumentParser(description='Script to run MobileNet-SSD object detection network ')
    parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
    parser.add_argument("--prototxt", default="aipinter/dnn/MobileNetSSD_deploy.prototxt.txt",
                                    help='Path to text network file: '
                                        'MobileNetSSD_deploy.prototxt for Caffe model or '
                                        )
    parser.add_argument("--weights", default="aipinter/dnn/MobileNetSSD_deploy.caffemodel",
                                    help='Path to weights: '
                                        'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                        )
    parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
    args = parser.parse_args()

    # Labels of Network.
    classNames = { 0: 'background',
        1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
        5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
        10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
        14: 'motorbike', 15: 'person', 16: 'pottedplant',
        17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }

    net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)
    while True:
        retval, frame = camera.read()
        frame = cv2.resize(frame,(400, 320))
        frame_resized = frame
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        #Set to network the input blob 
        net.setInput(blob)
        #Prediction of network
        detections = net.forward()

        #Size of frame resize (300x300)
        cols = frame_resized.shape[1] 
        rows = frame_resized.shape[0]

        #For get the class and location of object detected, 
        # There is a fix index for class, location and confidence
        # value in @detections array .
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2] #Confidence of prediction 
            if confidence > args.thr: # Filter prediction 
                class_id = int(detections[0, 0, i, 1]) # Class label

                # Object location 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)
                
                # Factor for scale to original size of frame
                heightFactor = frame.shape[0]/300.0  
                widthFactor = frame.shape[1]/300.0 
                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom) 
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)
                # Draw location of object  
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                            (255, 255, 0))

                # Draw label and confidence of prediction in frame resized
                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                        (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                        (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 2)
        
        imgencode=cv2.imencode('.jpg',frame)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1

    del(camera)

def get_frame():
    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object

    i=1

    # codingan face recognition
    obama_image = face_recognition.load_image_file('aipinter/dataset/face-datasets/toufan/10.jpg')
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
    biden_image = face_recognition.load_image_file("aipinter/dataset/face-datasets/cezar/1.jpg")
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding
    ]
    known_face_names = [
        "Toufan",
        "Cezar"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True


    while True:
        retval, frame = camera.read()
        frame = cv2.resize(frame,(400, 320))
        # im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, model='cnn')
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, top - 35), (right, top), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    
        imgencode=cv2.imencode('.jpg',frame)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1

    del(camera)


# CAMERA NORMAL / BIASA
def get_frame_norm():
    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object
    i=1
    while True:
        retval, frame = camera.read()
        frame = cv2.resize(frame,(400, 320))
    
        imgencode=cv2.imencode('.jpg',frame)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1

    del(camera)

# @camera.route('/calc')
@cam.route('/calc')
def calc():
    # form = ObjectDetectionForm()
    form_od = ObjectDetectionForm()
    data_cam = 'SSD MOBILE NET'
    if data_cam == 'SSD MOBILE NET':
        return Response(get_frame_od(),mimetype='multipart/x-mixed-replace; boundary=frame')
    elif data_cam == 'Ordinary_CNN':
        return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(get_frame_norm(),mimetype='multipart/x-mixed-replace; boundary=frame')

    return request(url_for('camera.calc_ord'))

@cam.route('/calc_ssd')
def calc_ssd():
    return Response(get_frame_od(),mimetype='multipart/x-mixed-replace; boundary=frame')

@cam.route('/calc_ord')
def calc_ord():
    return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@cam.route('/calc_norm')
def calc_norm():
    return Response(get_frame_norm(),mimetype='multipart/x-mixed-replace; boundary=frame')





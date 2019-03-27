
from sklearn.externals import joblib
from aipinter.camera.forms import ObjectDetectionForm
from sklearn.svm import LinearSVC
from aipinter.camera.hog import HOG 
from aipinter import dataset
from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify, Response
from flask_login import current_user, login_required
from imutils.video import VideoStream
import imutils
import argparse
import cv2
import mahotas
import face_recognition
import numpy as np
import time

cam = Blueprint('camera', __name__)


@cam.route('/camera', methods=['POST', 'GET'])
@login_required
def camera():
    form_od = ObjectDetectionForm()
    if current_user.is_authenticated == False:
        flash('Please, login first', 'danger')
        return redirect(url_for('users.login'))
    else:
        if request.method == 'POST':
            data_cam = request.form['camera']
            if data_cam == 'SSD MobileNet':
                req = 'ssd'
                return render_template('camera.html', form=form_od, req=req)
            elif data_cam == 'DLIB Face Recognition':
                req = 'dlib'
                return render_template('camera.html', form=form_od, req=req)
            
            elif data_cam == 'ResNet10 Face Recognition':
                req = 'res10'
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

def get_frame_ssd():
    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object

    i=1

    parser = argparse.ArgumentParser(description='Script to run MobileNet-SSD object detection network ')
    parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
    parser.add_argument("--prototxt", default="aipinter/dnn/mobileNet_ssd/MobileNetSSD_deploy.prototxt.txt",
                                    help='Path to text network file: '
                                        'MobileNetSSD_deploy.prototxt for Caffe model or '
                                        )
    parser.add_argument("--weights", default="aipinter/dnn/mobileNet_ssd/MobileNetSSD_deploy.caffemodel",
                                    help='Path to weights: '
                                        'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                        )
    # parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
    args = parser.parse_args()


    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    # print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    # (note: normalization is done via the authors of the MobileNet SSD
    # implementation)
    # image = cv2.imread(args["image"])
    # (h, w) = image.shape[:2]
    # blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    # print("[INFO] computing object detections...")


    while True:
        # image = cv2.imread(args["image"])
        retval, image = camera.read()
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (100, 100)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.2:
                # extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # display the prediction
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                cv2.rectangle(image, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        
        imgencode=cv2.imencode('.jpg',image)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i+=1

    del(camera)


def get_frame_dlib():
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
            # cv2.rectangle(frame, (left, top - 35), (right, top), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    
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

def get_frame_res10():

    camera_port=0
    ramp_frames=100
    camera=cv2.VideoCapture(camera_port) #this makes a web cam object


    ap = argparse.ArgumentParser()
    ap.add_argument("--prototxt", default="aipinter/dnn/res10/deploy.prototxt.txt",
        help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("--model", default="aipinter/dnn/res10/res10_300x300_ssd_iter_140000.caffemodel",
        help="path to Caffe pre-trained model")
    ap.add_argument("--confidence", type=float, default=0.5,
        help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    # load our serialized model from disk
    print("[INFO] loading model...")
    try:
        net = cv2.dnn.readNetFromCaffe("aipinter/dnn/res10/deploy.prototxt.txt", "aipinter/dnn/res10/res10_300x300_ssd_iter_140000.caffemodel")
        print('success to load the model')
    except:
        print('model failed to load')

    # initialize the video stream and allow the cammera sensor to warmup
    # print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    # time.sleep(2.0)

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        _, frame = camera.read()
        frame = imutils.resize(frame, width=400)
    
        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
    
        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < args["confidence"]:
                continue

            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
    
            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv2.putText(frame, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        
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
        return Response(get_frame_ssd(),mimetype='multipart/x-mixed-replace; boundary=frame')
    elif data_cam == 'DLIB Face Recognition':
        return Response(get_frame_dlib(),mimetype='multipart/x-mixed-replace; boundary=frame')
    elif data_cam == 'ResNet10 Face Recognition':
        return Response(get_frame_res10(),mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(get_frame_norm(),mimetype='multipart/x-mixed-replace; boundary=frame')

    return request(url_for('camera.calc_ord'))

@cam.route('/calc_ssd')
@login_required
def calc_ssd():
    return Response(get_frame_ssd(),mimetype='multipart/x-mixed-replace; boundary=frame')

@cam.route('/calc_dlib')
@login_required
def calc_dlib():
    return Response(get_frame_dlib(),mimetype='multipart/x-mixed-replace; boundary=frame')

@cam.route('/calc_res10')
@login_required
def calc_res10():
    return Response(get_frame_res10(),mimetype='multipart/x-mixed-replace; boundary=frame')


@cam.route('/calc_norm')
@login_required
def calc_norm():
    return Response(get_frame_norm(),mimetype='multipart/x-mixed-replace; boundary=frame')





import cv2

# Load the trained model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# You may need to change the index depending on your computer and camera
video_capture = cv2.VideoCapture(0)

while True:
    # Get an image frame
    ret, frame = video_capture.read()

    # Convert it to grayscale and run detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(
            img=frame,
            pt1=(x, y),
            pt2=(x + w, y + h),
            color=(0, 255, 0),
            thickness=2,
        )

    # Display the resulting frame
    cv2.imshow("Chapter 14 - OpenCV", frame)

    # Break when key "q" is pressed
    if cv2.waitKey(1) == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()

# You can simply run this script by invoking it with Python:
# $ python Chapter14/opencv.py

# Let's go through the implementation. 
# The first thing we do is instantiate a CascadeClassifier class with an XML file bundled with the library. 
# This class is actually a machine learning algorithm using the Haar cascade principle. 
# You can read more about the theory behind this algorithm in the OpenCV documentation:https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html.
# The nice thing here is that OpenCV comes with pre-trained models, provided in the form of XML files, including ones for face detection. 
# Hence, we only have to load them to start working on images.

# Then, we instantiate a VideoCapture class. It'll allow us to stream images from a webcam. 
# The integer argument in the initializer is the index of the camera you want to use. 
# If you have several cameras, you may need to adjust this argument.

# After that, we start an infinite loop so that we can continuously run detections on the stream of images. 
# Inside it, we start by retrieving an image, frame, from the video_capture instance. 
# This image is then fed to the classifier thanks to the detectMultiScale method. 
# Notice that we first convert it to grayscale, which is a requirement for Haar cascade classifiers.
# The result of this operation is a list of tuples containing the characteristics of the rectangles around the detected faces: 
    # x and y are the coordinates of the starting point; w and h are the width and height of this rectangle. 
# All we have to do is draw each rectangle on the image using the rectangle function.

# Finally, we can display the image in a window. 
# Notice that before ending the loop, we give it a chance to break by listening for a keypress on the keyboard: if the q key is pressed, we break the loop.
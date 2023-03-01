import cv2

cap = cv2.VideoCapture(0)

# Get the frames per second
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
success, image = cap.read()
print(success)

if success:
    print(type(image))

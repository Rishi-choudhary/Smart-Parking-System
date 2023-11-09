# import cv2
# from matplotlib import pyplot as plt
# import numpy as np
# import imutils
# import easyocr

# img = cv2.imread('image4.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
# edged = cv2.Canny(bfilter, 30, 200) #Edge detection

# keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours = imutils.grab_contours(keypoints)
# contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# location = None
# for contour in contours:
#     approx = cv2.approxPolyDP(contour, 10, True)
#     if len(approx) == 4:
#         location = approx
#         break
    
# mask = np.zeros(gray.shape, np.uint8)
# new_image = cv2.drawContours(mask, [location], 0,255, -1)
# new_image = cv2.bitwise_and(img, img, mask=mask)

# plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

# (x,y) = np.where(mask==255)
# (x1, y1) = (np.min(x), np.min(y))
# (x2, y2) = (np.max(x), np.max(y))
# cropped_image = gray[x1:x2+1, y1:y2+1]

# reader = easyocr.Reader(['en'])
# result = reader.readtext(cropped_image)
# print(result)

# text = result[0][-2]
# font = cv2.FONT_HERSHEY_SIMPLEX
# res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
# res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)


import cv2
import numpy as np
import easyocr

# Load the EasyOCR reader
reader = easyocr.Reader(['en'])


url = "http://192.168.101.5:8080/video"
# Initialize the video capture
cap = cv2.VideoCapture(url)  # 0 for the default camera, or provide a path to a video file

while True:
    
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter and edge detection (similar to your code)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)

    # Find contours
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    if location is not None:
        # Draw the contour on the frame
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(frame, frame, mask=mask)

        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

        # Read text using EasyOCR
        result = reader.readtext(cropped_image)

        if result:
            text = result[0][-2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            res = cv2.putText(frame, text=text, org=(location[0][0][0], location[1][0][1] + 60), fontFace=font,
                             fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
            res = cv2.rectangle(frame, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)
            
            # Display the frame with the detected plate
            cv2.imshow("Car Plate Detection", frame)

            # Break the loop and print the result
            print(result)
            break

    # Display the original frame
    cv2.imshow("Car Plate Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit the loop
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()





# # /////////////////

# import cv2
# from matplotlib import pyplot as plt
# import numpy as np
# import imutils
# import easyocr

# url = "http://192.168.101.5:8080/video"
# cap = cv2.VideoCapture(url) # 0 for the default camera

# while(True):
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     bfilter = cv2.bilateralFilter(gray, 11, 17, 17) # Noise reduction
#     edged = cv2.Canny(bfilter, 30, 200) # Edge detection

#     keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = imutils.grab_contours(keypoints)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

#     location = None
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 10, True)
#         if len(approx) == 4:
#             location = approx
#             break
    
#     if location is not None:
#         mask = np.zeros(gray.shape, np.uint8)
#         new_image = cv2.drawContours(mask, [location], 0,255, -1)
#         new_image = cv2.bitwise_and(frame, frame, mask=mask)

#         (x,y) = np.where(mask==255)
#         (x1, y1) = (np.min(x), np.min(y))
#         (x2, y2) = (np.max(x), np.max(y))
#         cropped_image = gray[x1:x2+1, y1:y2+1]

#         reader = easyocr.Reader(['en'])
#         result = reader.readtext(cropped_image)
#         print(result)

#         text = result[0][-2]
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         res = cv2.putText(frame, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
#         res = cv2.rectangle(frame, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)

#         cv2.imshow('frame', frame)
#         break

#     cv2.imshow('edged', edged)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

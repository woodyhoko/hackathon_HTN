import cv2

POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

protoFile = "model/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "model/pose_iter_160000.caffemodel"
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# capture video
video_path = "test.mp4"
out_path = "output"
out_name = "test-out_1"
FPS = 20
size_out = (368,368)
width_out = 368
height = 368
width = 368
inWidth = 368
inHeight = 368
frameWidth = 368
frameHeight = 368
cap = cv2.VideoCapture(video_path)
# Check if video file is opened successfully
if (cap.isOpened() == False):
  print("Error opening video stream or file")
# Read until video is completed
out = cv2.VideoWriter(out_path + '/' + out_name + '.webm', cv2.VideoWriter_fourcc(*'VP90'), FPS, size_out)
print("hey")
while(cap.isOpened()):
# Capture frame-by-frame
    ret, frame = cap.read()
    # print(frame)
    if ret == True:
        frame = cv2.resize(frame, (width_out, int(width_out*height/width)), cv2.INTER_AREA)
        # process the frame here
        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()
        # print(output)
        H = output.shape[2]
        W = output.shape[3]
        # Empty list to store the detected keypoints
        points = []
        print(output.shape)
        for i in range(output.shape[1]):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]
            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
            # Scale the point to fit on the original image
            x = (frameWidth * point[0]) / W
            y = (frameHeight * point[1]) / H
            if prob:# &amp;amp;gt; threshold :
                cv2.circle(frame, (int(x), int(y)), 15, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, lineType=cv2.LINE_AA)
                # Add the point to the list if the probability is greater than the threshold
                points.append((int(x), int(y)))
            else :
                points.append(None)
        for pair in POSE_PAIRS:
            partA = pair[0]
            partB = pair[1]
            if points[partA] and points[partB]:
                cv2.line(frame, points[partA], points[partB], (0, 255, 0), 3)
        out.write(frame)

# Break the loop
    else:
        break
out.release()
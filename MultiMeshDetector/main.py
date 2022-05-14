import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("testvi.mov")
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()
mpPose = mp.solutions.pose
pose = mpPose.Pose()

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    results2 = faceMesh.process(imgRGB)
    results3 = pose.process(imgRGB)
    results4 = faceMesh.process(imgRGB)
    print(results)

    if results.detections:
        for id,detection in enumerate(results.detections):
            mpDraw.draw_detection(img,detection,
                                  mpDraw.DrawingSpec(color=(0, 250, 0)),
                                  mpDraw.DrawingSpec(color=(0, 250, 0))
                                  )
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (0, 250, 0), 2)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        3, (0, 255, 0), 2)

    if results3.pose_landmarks:
        mpDraw.draw_landmarks(img, results3.pose_landmarks,mpPose.POSE_CONNECTIONS,
                              mpDraw.DrawingSpec(color=(0,250,0)),
                              mpDraw.DrawingSpec(color=(0, 250, 0))
                              )

    if results4.multi_face_landmarks:
        for faceLms in results4.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,drawSpec,mpDraw.DrawingSpec(color=(0, 250, 0)))

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.imshow("Image", img)
    cv2.waitKey(1)

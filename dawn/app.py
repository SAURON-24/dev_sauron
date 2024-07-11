from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import io

app = FastAPI()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
raw_capture = PiRGBArray(camera, size=(640, 480))

def generate_video_stream():
    # Capture video continuously
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', image)
        if not ret:
            continue

        # Convert the frame to bytes and yield it
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        # Clear the stream to prepare for the next frame
        raw_capture.truncate(0)

# uid값 받기
@app.post("/uid")
async def receive_uid(request: Request):
    data = await request.json()
    uid = data.get("uid")
    print(f"Received UID: {uid}")
    return {"status": "success", "uid": uid}

# uid값 분류 : rec있으면 관리자, rec 없으면 일반사용자 (임의)
# async def get_uid_type(uid):
#     if uid.startswith("rec"):
#         return "rec"
#     else:
#         return "normal"

# cctv영상 표시
@app.get("/getcctv")
async def video_feed():
    return StreamingResponse(generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from flask import Flask, render_template, Response, redirect, url_for
import cv2
import os
from ultralytics import YOLO

app = Flask(__name__)

model_path = os.path.join('.', 'models', 'best.pt')
model = YOLO(model_path)

cap = None
threshold = 0.5
class_name_dict = {0: "Hello", 1: "ILoveYou", 2: "No", 3: "Please", 4: "Thanks", 5: "Yes"}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/graph')
def graph():
    # List of graph filenames
    graph_files = ["confusion_matrix.png", "F1_curve.png", "P_curve.png", "PR_curve.png", "R_curve.png", "results.png"]
    
    # Generate URLs for each graph file
    graph_urls = [url_for('static', filename=graph_file) for graph_file in graph_files]
    
    return render_template('graph.html', graph_urls=graph_urls)

@app.route('/start_detection')
def start_detection():
    global cap
    cap = cv2.VideoCapture(0)
    return "Detection started"

@app.route('/stop_detection')
def stop_detection():
    global cap
    if cap is not None:
        cap.release()
        cap = None
    return redirect(url_for('detection'))

def generate_frames():
    global cap
    while cap and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, class_name_dict[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    if cap:
        cap.release()
        cap = None

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, Response, redirect, url_for, request, flash
import cv2
import os
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'supersecretkey'  # Necessary for flash messages

model_path = os.path.join('.', 'models', 'best.pt')
model = YOLO(model_path)

cap = None
threshold = 0.5
class_name_dict = {0: "Hello", 1: "ILoveYou", 2: "No", 3: "Please", 4: "Thanks", 5: "Yes"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/graph')
def graph():
    graph_files = ["confusion_matrix.png", "F1_curve.png", "P_curve.png", "PR_curve.png", "R_curve.png", "results.png"]
    graph_urls = [url_for('static', filename=graph_file) for graph_file in graph_files]
    return render_template('graph.html', graph_urls=graph_urls)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            flash('File type not supported. Only PNG, JPG, and JPEG files are allowed.')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_type = filename.rsplit('.', 1)[1].lower()
    
    if file_type in {'png', 'jpg', 'jpeg'}:
        result_image = detect_image(filepath)
        result_filename = 'result_' + filename
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_path, result_image)
        return render_template('result.html', image_url=url_for('static', filename='uploads/' + result_filename))
    else:
        flash('File type not supported')
        return redirect(url_for('upload'))

def detect_image(image_path):
    image = cv2.imread(image_path)
    results = model(image)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(image, class_name_dict[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    return image

@app.route('/start_detection')
def start_detection():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)
    return "Detection started"

@app.route('/stop_detection')
def stop_detection():
    global cap
    if cap is not None:
        cap.release()
        cap = None
    return "Detection stopped"

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
    if cap is None:
        return Response(status=204)  # No content
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

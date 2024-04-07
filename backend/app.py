from flask import Flask, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
from celery import Celery
from flask_cors import CORS


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Adjust as needed

# Configure Celery (This requires a running broker, e.g., RabbitMQ or Redis)
app.config['CELERY_BROKER_URL'] = 'url_to_your_broker'
app.config['CELERY_RESULT_BACKEND'] = 'url_to_your_backend'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# Enabling CORS for all domains on all routes. For production, narrow this down.
# CORS(app, resources={r"/upload": {"origins": "http://127.0.0.1:3000"}}, supports_credentials=True)
CORS(app, supports_credentials=True)


@celery.task(bind=True)
def process_video(self, filename):
    # Replace the line below with your video processing logic
    # For now, we just simulate long-running processing
    import time
    time.sleep(10)  # Simulate a long-running process
    self.update_state(state='PROGRESS', meta={'process_percent': 100})
    # Return the URL for the processed video
    return url_for('uploaded_file', filename=filename, _external=True)


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        print(f"Saving file to: {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Start processing stuff
        

        return jsonify({'message': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
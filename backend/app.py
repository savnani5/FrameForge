from utils.plugin_loader import PluginLoader
from config import config as cfg
import torch
import os
import numpy as np
from test_tools.common import detect_all, grab_all_frames
from test_tools.utils import get_crop_box
from test_tools.ct.operations import find_longest, multiple_tracking
from test_tools.faster_crop_align_xray import FasterCropAlignXRay
from test_tools.supply_writer import SupplyWriter
import argparse
from tqdm import tqdm
import subprocess


from flask import Flask, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
from celery import Celery
from flask_cors import CORS

mean = torch.tensor([0.485 * 255, 0.456 * 255, 0.406 * 255,]).view(1, 3, 1, 1, 1)
std = torch.tensor([0.229 * 255, 0.224 * 255, 0.225 * 255,]).view(1, 3, 1, 1, 1)


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app = Flask(__name__, static_folder='frontend/build', static_url_path='')

# Example configuration - adjust as necessary for your environment
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Adjust as needed

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Celery (This requires a running broker, e.g., RabbitMQ or Redis)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# Enabling CORS for all domains on all routes. For production, narrow this down.
# CORS(app, resources={r"/upload": {"origins": "http://127.0.0.1:3000"}}, supports_credentials=True)
CORS(app, supports_credentials=True)


@celery.task(bind=True)
def process_video(self, filename):
    with app.app_context():  # Use your Flask app instance
        
        ##----------------------------##
        # out_dir = 'output'
        # cfg.init_with_yaml()
        # cfg.update_with_yaml("ftcn_tt.yaml")
        # cfg.freeze()

        # classifier = PluginLoader.get_classifier(cfg.classifier_type)()
        # # classifier.cuda()
        # classifier.eval()
        # classifier.load("checkpoints/ftcn_tt.pth")
        # print(classifier)
        # crop_align_func = FasterCropAlignXRay(cfg.imsize)

        # input_file = filename
        # os.makedirs(out_dir, exist_ok=True)
        # basename = os.path.splitext(os.path.basename(input_file))[0] + ".mp4"
        # out_file = os.path.join(out_dir, basename)

        # max_frame = 768
        # cache_file = f"{input_file}_{str(max_frame)}.pth"

        # if os.path.exists(cache_file):
        #     detect_res, all_lm68 = torch.load(cache_file)
        #     frames = grab_all_frames(input_file, max_size=max_frame, cvt=True)
        #     print("detection result loaded from cache")
        # else:
        #     print("detecting")
        #     detect_res, all_lm68, frames = detect_all(
        #         input_file, return_frames=True, max_size=max_frame
        #     )
        #     torch.save((detect_res, all_lm68), cache_file)
        #     print("detect finished")

        # print("number of frames",len(frames))

        
        # shape = frames[0].shape[:2]

        # all_detect_res = []

        # assert len(all_lm68) == len(detect_res)

        # for faces, faces_lm68 in zip(detect_res, all_lm68):
        #     new_faces = []
        #     for (box, lm5, score), face_lm68 in zip(faces, faces_lm68):
        #         new_face = (box, lm5, face_lm68, score)
        #         new_faces.append(new_face)
        #     all_detect_res.append(new_faces)

        # detect_res = all_detect_res

        # print("split into super clips")

        # tracks = multiple_tracking(detect_res)
        # tuples = [(0, len(detect_res))] * len(tracks)

        # print("full_tracks", len(tracks))

        # if len(tracks) == 0:
        #     tuples, tracks = find_longest(detect_res)

        # data_storage = {}
        # frame_boxes = {}
        # super_clips = []

        # for track_i, ((start, end), track) in enumerate(zip(tuples, tracks)):
        #     print(start, end)
        #     assert len(detect_res[start:end]) == len(track)

        #     super_clips.append(len(track))

        #     for face, frame_idx, j in zip(track, range(start, end), range(len(track))):
        #         box,lm5,lm68 = face[:3]
        #         big_box = get_crop_box(shape, box, scale=0.5)

        #         top_left = big_box[:2][None, :]

        #         new_lm5 = lm5 - top_left
        #         new_lm68 = lm68 - top_left

        #         new_box = (box.reshape(2, 2) - top_left).reshape(-1)

        #         info = (new_box, new_lm5, new_lm68, big_box)


        #         x1, y1, x2, y2 = big_box
        #         cropped = frames[frame_idx][y1:y2, x1:x2]

        #         base_key = f"{track_i}_{j}_"
        #         data_storage[base_key + "img"] = cropped
        #         data_storage[base_key + "ldm"] = info
        #         data_storage[base_key + "idx"] = frame_idx

        #         frame_boxes[frame_idx] = np.rint(box).astype(np.int64)

        # print("sampling clips from super clips", super_clips)

        # clips_for_video = []
        # clip_size = cfg.clip_size
        # pad_length = clip_size - 1

        # for super_clip_idx, super_clip_size in enumerate(super_clips):
        #     inner_index = list(range(super_clip_size))
        #     if super_clip_size < clip_size: # padding
        #         post_module = inner_index[1:-1][::-1] + inner_index

        #         l_post = len(post_module)
        #         post_module = post_module * (pad_length // l_post + 1)
        #         post_module = post_module[:pad_length]
        #         assert len(post_module) == pad_length

        #         pre_module = inner_index + inner_index[1:-1][::-1]
        #         l_pre = len(post_module)
        #         pre_module = pre_module * (pad_length // l_pre + 1)
        #         pre_module = pre_module[-pad_length:]
        #         # assert len(pre_module) == pad_length

        #         inner_index = pre_module + inner_index + post_module

        #     super_clip_size = len(inner_index)

        #     frame_range = [
        #         inner_index[i : i + clip_size] for i in range(super_clip_size) if i + clip_size <= super_clip_size
        #     ]
        #     for indices in frame_range:
        #         clip = [(super_clip_idx, t) for t in indices]
        #         clips_for_video.append(clip)
        
        # preds = []
        # frame_res = {}

        # for clip in tqdm(clips_for_video, desc="testing"):
        #     images = [data_storage[f"{i}_{j}_img"] for i, j in clip]
        #     landmarks = [data_storage[f"{i}_{j}_ldm"] for i, j in clip]
        #     frame_ids = [data_storage[f"{i}_{j}_idx"] for i, j in clip]
        #     landmarks, images = crop_align_func(landmarks, images)
        #     # images = torch.as_tensor(images, dtype=torch.float32).cuda().permute(3, 0, 1, 2)
        #     images = torch.as_tensor(images, dtype=torch.float32).permute(3, 0, 1, 2)
        #     images = images.unsqueeze(0).sub(mean).div(std)

        #     with torch.no_grad():
        #         output = classifier(images)

        #     pred = float(output["final_output"])
        #     for f_id in frame_ids:
        #         if f_id not in frame_res:
        #             frame_res[f_id] = []
        #         frame_res[f_id].append(pred)
        #     preds.append(pred)

        # print(np.mean(preds))
        
        # boxes = []
        # scores = []

        # for frame_idx in range(len(frames)):
        #     if frame_idx in frame_res:
        #         pred_prob = np.mean(frame_res[frame_idx])
        #         rect = frame_boxes[frame_idx]
        #     else:
        #         pred_prob = None
        #         rect = None
        #     scores.append(pred_prob)
        #     boxes.append(rect)

        # SupplyWriter(filename, out_file, 0.504857167676091).run(frames, scores, boxes)

        ##----------------------------##
        # Assuming 'uploaded_file' is a valid endpoint in your Flask app
        processed_video_url = url_for('uploaded_file', filename=filename, _external=True)
        return processed_video_url

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(filename)
    import time
    time.sleep(3)
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


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
        process_video.delay(filename)

        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
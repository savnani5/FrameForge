# FrameForge AI

## How to run? 

1) Clone the repo and download pretrained weights
```
git clone https://github.com/savnani5/deepfake-detection.git
```
Download `FTCN+TT` model trained on FF++ from [here](https://github.com/yinglinzheng/FTCN/releases/download/weights/ftcn_tt.pth) and place it under `./checkpoints` folder in backend

2) Install dependencies
```
pip install -r requirements.txt
```
3) Run Flask server in backend
```
flask run
```
4) Run Redis Server
```
brew services start redis
```
5) Run Celery in backend
```
celery -A app.celery worker --loglevel=info
```
6) Build the React App
```
npm run build
```
7) Run React App
```
npm start
```


## Algorithm Abstract
Although current face manipulation techniques achieve impressive performance regarding quality and controllability, they are struggling to generate temporal coherent face videos. In this work, we explore to take full advantage of the temporal coherence for video face forgery detection. To achieve this, we propose a novel end-to-end framework, which consists of two major stages. The first stage is a fully temporal convolution network (FTCN). The key insight of FTCN is to reduce the spatial convolution kernel size to 1, while maintaining the temporal convolution kernel size unchanged. We surprisingly find this special design can benefit the model for extracting the temporal features as well as improve the generalization capability. The second stage is a Temporal Transformer network, which aims to explore the long-term temporal coherence. The proposed framework is general and flexible, which can be directly trained from scratch without any pre-training models or external datasets. Extensive experiments show that our framework outperforms existing methods and remains effective when applied to detect new sorts of face forgery videos.


# Setup
First setup python environment with pytorch 1.4.0 installed, **it's highly recommended to use docker image [pytorch/pytorch:1.4-cuda10.1-cudnn7-devel](https://hub.docker.com/layers/pytorch/pytorch/1.4-cuda10.1-cudnn7-devel/images/sha256-c612782acc39256aac0637d58d297644066c62f6f84f0b88cfdc335bb25d0d22), as the pretrained model and the code might be incompatible with higher version pytorch.**

then install dependencies for the experiment:



# Test
## Inference Using Pretrained Model on Raw Video
```bash
python backend/test_on_raw_video.py examples/shining.mp4 output
```
the output will be a video under folder `output` named `shining.avi`

![](backend/examples/shining.gif)

# Website
![](backend/examples/image.png)

# Acknowledgments

This code borrows heavily from [SlowFast](https://github.com/facebookresearch/SlowFast).

The face detection network comes from [biubug6/Pytorch_Retinaface](https://github.com/biubug6/Pytorch_Retinaface).

The face alignment network comes from [cunjian/pytorch_face_landmark](https://github.com/cunjian/pytorch_face_landmark).

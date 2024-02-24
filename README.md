# LabelerCV
Labeling scripts and tools for Computer Vision datasets

### 1. CVAT 
- Git Repository
    ```
    git clone --recurse-submodules https://github.com/karmarv/labelercv.git
    ```
    - Ensure CVAT submodule is checked out 
    ```
    git clone --depth 1 --branch v2.11.0 https://github.com/opencv/cvat
    ```

- Operate CVAT - [Instructions](./cvat_scripts/README.md)
    ```
    cd cvat_scripts
    bash startup_cvat.bash
    bash shutdown_cvat.bash
    ```
- Access CVAT: http://karmax:8080/tasks

### 2. CVAT Functions
- Nuclio functions. Eg: [YoloV7 & Onnx](https://github.com/WongKinYiu/yolov7)

### 3. Data Converters
- Convert backup task to YOLO labels.txt format
- Convert backup task to COCO annotations.json format

### GCP Installation
- GCP Reference: https://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/install/google-docker-container.html
- Docker Reference: https://docs.docker.com/engine/install/ubuntu/



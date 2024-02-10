# Copyright (C) 2023 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

import cv2
import numpy as np
import onnxruntime as ort
import torch

class ModelHandler:
    def __init__(self, labels):
        self.model = None
        self.load_network(model="best.onnx")
        self.labels = labels

    def load_network(self, model):
        device = ort.get_device()
        cuda = True if device == 'GPU' else False
        try:
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
            so = ort.SessionOptions()
            so.log_severity_level = 3

            # Model - https://pytorch.org/hub/ultralytics_yolov5/
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', model)

            #self.model = ort.InferenceSession(model, providers=providers, sess_options=so)
            #self.output_details = [i.name for i in self.model.get_outputs()]
            #self.input_details = [i.name for i in self.model.get_inputs()]

            self.is_inititated = True
        except Exception as e:
            raise Exception(f"Cannot load model {model}: {e}")

    def letterbox(self, im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, r, (dw, dh)

    def _infer(self, inputs, new_shape):
        # https://docs.ultralytics.com/yolov5/tutorials/pytorch_hub_model_loading/#cropped-results
        try:
            img = cv2.cvtColor(inputs, cv2.COLOR_BGR2RGB)
            image = img.copy()
            image_sized = cv2.resize(image, new_shape, interpolation = cv2.INTER_AREA)
            # Inference
            preds = self.model([image_sized])
            print(preds.print())
            detections = preds.xyxy[0]
            # for det in detections
            boxes  = detections[:, 0:4].numpy()
            labels = detections[:, 5].numpy()
            scores = detections[:, 4].numpy()
            boxes = boxes.round().astype(np.int32)
            # Output list
            output = list()
            output.append(boxes)
            output.append(labels)
            output.append(scores)
            return output
        except Exception as e:
            print(e)

    def infer(self, image, threshold):
        image = np.array(image)
        image = image[:, :, ::-1].copy()
        h, w, _ = image.shape
        print("Input image shape: ", image.shape)
        new_shape = (512, 512)
        detections = self._infer(image, new_shape)
        scaling_h, scaling_w = h/new_shape[0], w/new_shape[1]
        print("Scaling factor: ", scaling_h, scaling_w)

        results = []
        if detections:
            boxes = detections[0]
            labels = detections[1]
            scores = detections[2]

            for label, score, box in zip(labels, scores, boxes):
                if score >= threshold:
                    xtl = max(int(box[0]*scaling_w), 0)
                    ytl = max(int(box[1]*scaling_h), 0)
                    xbr = min(int(box[2]*scaling_w), w)
                    ybr = min(int(box[3]*scaling_h), h)

                    results.append({
                        "confidence": str(score),
                        "label": self.labels.get(label, "unknown"),
                        "points": [xtl, ytl, xbr, ybr],
                        "type": "rectangle",
                    })

        return results

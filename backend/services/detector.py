import base64
import io
import os

import cv2
import numpy as np

from PIL import Image
from ultralytics import YOLO


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "best.pt"
)


if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"YOLO model not found at: {MODEL_PATH}"
    )


model = YOLO(MODEL_PATH)


CLASS_COLORS = {
    "crack": (0, 0, 255),
    "scratch": (255, 0, 0),
    "dent": (0, 165, 255),
    "glass shatter": (255, 0, 255),
    "lamp broken": (0, 255, 255),
    "tire flat": (0, 255, 0)
}


def get_color(defect):

    return CLASS_COLORS.get(
        defect.lower(),
        (255, 255, 255)
    )


def detect_image(
    image_bytes,
    confidence_threshold=0.40
):

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image_array = np.array(image)

    results = model.predict(
        source=image_array,
        conf=confidence_threshold,
        verbose=False
    )

    detections = []

    annotated_image = image_array.copy()

    for result in results:

        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )

            defect = model.names[
                class_id
            ]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            color = get_color(
                defect
            )

            cv2.rectangle(
                annotated_image,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

            label = (
                f"{defect} "
                f"{confidence * 100:.1f}%"
            )

            (
                text_width,
                text_height
            ), baseline = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )

            label_y = max(
                y1,
                text_height + baseline + 5
            )

            cv2.rectangle(
                annotated_image,
                (
                    x1,
                    label_y
                    - text_height
                    - baseline
                    - 8
                ),
                (
                    x1 + text_width + 8,
                    label_y
                ),
                color,
                -1
            )

            cv2.putText(
                annotated_image,
                label,
                (
                    x1 + 4,
                    label_y - 6
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            detections.append({
                "defect": defect,
                "confidence": round(
                    confidence,
                    4
                ),
                "confidence_percent": round(
                    confidence * 100,
                    2
                ),
                "bbox": [
                    x1,
                    y1,
                    x2,
                    y2
                ]
            })

    annotated_bgr = cv2.cvtColor(
        annotated_image,
        cv2.COLOR_RGB2BGR
    )

    success, encoded_image = cv2.imencode(
        ".jpg",
        annotated_bgr
    )

    if not success:
        raise RuntimeError(
            "Could not encode annotated image."
        )

    image_base64 = base64.b64encode(
        encoded_image.tobytes()
    ).decode("utf-8")

    defect_summary = {}

    for detection in detections:

        defect = detection["defect"]
        confidence = detection["confidence"]

        if defect not in defect_summary:
            defect_summary[defect] = {
                "defect": defect,
                "detections": 0,
                "highest_confidence": confidence
            }

        defect_summary[defect]["detections"] += 1

        if confidence > defect_summary[defect]["highest_confidence"]:
            defect_summary[defect]["highest_confidence"] = confidence

    return {
        "success": True,
        "count": len(detections),
        "defect_count": len(defect_summary),
        "detections": detections,
        "summary": list(defect_summary.values()),
        "image": (
            "data:image/jpeg;base64,"
            + image_base64
        )
    }
import os
import tempfile

import cv2

from backend.services.detector import model


def process_video(
    video_bytes,
    filename,
    frame_interval=1,
    confidence_threshold=0.40
):

    extension = os.path.splitext(filename)[1]

    if not extension:
        extension = ".mp4"

    temporary_path = None

    try:

        # ==================================================
        # 1. Save uploaded video temporarily
        # ==================================================

        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False
        ) as temporary_file:

            temporary_file.write(video_bytes)

            temporary_path = temporary_file.name

        # ==================================================
        # 2. Open video
        # ==================================================

        capture = cv2.VideoCapture(
            temporary_path
        )

        if not capture.isOpened():
            raise RuntimeError(
                "Unable to open video."
            )

        frame_number = 0
        processed_frames = 0

        # Only frames containing defects
        detected_frames = []

        # ==================================================
        # 3. Process video
        # ==================================================

        while True:

            success, frame = capture.read()

            if not success:
                break

            frame_number += 1

            # Process every frame
            if frame_number % frame_interval != 0:
                continue

            processed_frames += 1

            # ==================================================
            # YOLO prediction
            # ==================================================

            results = model.predict(
                source=frame,
                conf=confidence_threshold,
                verbose=False
            )

            frame_detections = []

            # ==================================================
            # Extract detections
            # ==================================================

            for result in results:

                if result.boxes is None:
                    continue

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
                        box.xyxy[0]
                    )

                    frame_detections.append({

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

            # ==================================================
            # No defect -> discard frame
            # ==================================================

            if not frame_detections:
                continue

            # ==================================================
            # Draw ALL detections
            # ==================================================

            annotated_frame = frame.copy()

            for detection in frame_detections:

                x1, y1, x2, y2 = (
                    detection["bbox"]
                )

                defect = detection["defect"]

                confidence = detection["confidence"]

                label = (
                    f"{defect.upper()} "
                    f"{confidence * 100:.1f}%"
                )

                # Bounding box
                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )

                # Label
                cv2.putText(
                    annotated_frame,
                    label,
                    (
                        x1,
                        max(y1 - 10, 25)
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            # ==================================================
            # Save detected frame
            # ==================================================

            evidence_directory = os.path.join(
                "reports",
                "video_evidence"
            )

            os.makedirs(
                evidence_directory,
                exist_ok=True
            )

            image_filename = (
                f"frame_{frame_number}.jpg"
            )

            image_path = os.path.join(
                evidence_directory,
                image_filename
            )

            cv2.imwrite(
                image_path,
                annotated_frame
            )

            # ==================================================
            # Browser-accessible URL
            # ==================================================

            image_url = (
                f"/reports/video_evidence/"
                f"{image_filename}"
            )

            # ==================================================
            # Add detected frame
            # ==================================================

            detected_frames.append({

                "frame": frame_number,

                "image": image_url,

                "detections": frame_detections

            })

        capture.release()

        # ==================================================
        # 4. Create defect summary
        # ==================================================

        defect_summary = {}

        for frame_data in detected_frames:

            for detection in frame_data["detections"]:

                defect = detection["defect"]

                confidence = detection["confidence"]

                if defect not in defect_summary:

                    defect_summary[defect] = {

                        "defect": defect,

                        "detections": 0,

                        "highest_confidence":
                            confidence

                    }

                defect_summary[
                    defect
                ]["detections"] += 1

                if confidence > (
                    defect_summary[
                        defect
                    ]["highest_confidence"]
                ):

                    defect_summary[
                        defect
                    ]["highest_confidence"] = confidence

        # ==================================================
        # 5. Return result
        # ==================================================

        return {

            "success": True,

            "total_frames":
                frame_number,

            "processed_frames":
                processed_frames,

            "detected_frames":
                len(detected_frames),

            "defects_found":
                len(detected_frames) > 0,

            "frames":
                detected_frames,

            "summary":
                list(
                    defect_summary.values()
                ),

            "defect_count":
                len(defect_summary)

        }

    finally:

        # ==================================================
        # Remove temporary uploaded video
        # ==================================================

        if (
            temporary_path
            and os.path.exists(
                temporary_path
            )
        ):

            os.remove(
                temporary_path
            )
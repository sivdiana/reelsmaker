import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
import config

def get_coords(path_to_input_video: str, all_ranges: list) -> pd.DataFrame:
    """
    Извлекает координаты скелета из видео с помощью MediaPipe task_landmarker_lite.

    Args:
        path_to_input_video (str): Путь к видео.
        all_ranges (list): Список диапазонов кадров [(start, end), ...].

    Returns:
        pd.DataFrame: Таблица координат: frame, landmark_index, x, y, z, visibility.
    """
    cap = cv2.VideoCapture(path_to_input_video)
    landmarks_data = []
    valid_frames = set()
    for start, end in all_ranges:
        valid_frames.update(range(start, end + 1))

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=config.MODEL_PATH),
        running_mode=VisionRunningMode.VIDEO,
        num_poses=config.NUM_POSES,
        min_pose_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
        min_pose_presence_confidence=config.MIN_PRESENCE_CONFIDENCE,
        min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
        output_segmentation_masks=config.CALCULATE_MASKS,
    )

    with PoseLandmarker.create_from_options(options) as landmarker:
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx in valid_frames:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
                timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
                result = landmarker.detect_for_video(mp_frame, timestamp_ms=timestamp)
                if result.pose_landmarks:
                    for idx, landmark in enumerate(result.pose_landmarks[0]):
                        landmarks_data.append({
                            'frame': frame_idx,
                            'landmark_index': idx,
                            'x': landmark.x,
                            'y': landmark.y,
                            'z': landmark.z,
                            'visibility': landmark.visibility
                        })
                else:
                    for idx in range(33):
                        landmarks_data.append({
                            'frame': frame_idx,
                            'landmark_index': idx,
                            'x': np.nan,
                            'y': np.nan,
                            'z': np.nan,
                            'visibility': np.nan
                        })
            frame_idx += 1

    cap.release()
    return pd.DataFrame(landmarks_data)

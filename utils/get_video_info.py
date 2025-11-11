import cv2

def get_video_information(path_to_input_video: str):
    """
    Получает ширину, высоту и FPS видео.

    Args:
        path_to_input_video (str): Путь к видеофайлу.

    Returns:
        tuple: (ширина, высота, fps)
    """
    cap = cv2.VideoCapture(path_to_input_video)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return frame_width, frame_height, fps

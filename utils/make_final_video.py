import cv2

def make_final_video(video_path: str,
                     boxes: list[dict],
                     output_path: str,
                     crop_width: int,
                     crop_height: int,
                     fps: float,
                     frame_height: int,
                     frame_width: int) -> None:
    """
    Создаёт финальное видео с кропами вокруг фигуриста на каждом кадре.

    Args:
        video_path (str): Путь к исходному видео.
        boxes (list[dict]): Список кропов: [{'frame': int, 'x1': int, 'x2': int, 'y1': int, 'y2': int}, ...].
        output_path (str): Путь к выходному видео.
        crop_width (int): Ширина финального кадра.
        crop_height (int): Высота финального кадра.
        fps (float): Частота кадров.
        frame_height (int): Оригинальная высота кадра.
        frame_width (int): Оригинальная ширина кадра.
    """
    cap = cv2.VideoCapture(video_path)

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (crop_width, crop_height)
    )

    print(f"Начинается генерация видео: {output_path} ({crop_width}x{crop_height})")

    for box in boxes:
        frame_num = box['frame']
        x1, x2 = box['x1'], box['x2']
        y1, y2 = box['y1'], box['y2']

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            print(f"Кадр №{frame_num} не читается")
            continue

        x1_clamp = max(0, x1)
        x2_clamp = min(frame_width, x2)
        cropped = frame[y1:y2, x1_clamp:x2_clamp]

        pad_left = x1_clamp - x1
        pad_right = x2 - x2_clamp

        if pad_left > 0 or pad_right > 0:
            cropped = cv2.copyMakeBorder(
                cropped,
                top=0,
                bottom=0,
                left=pad_left,
                right=pad_right,
                borderType=cv2.BORDER_CONSTANT,
                value=(0, 0, 0)
            )

        final = cv2.resize(cropped, (crop_width, crop_height))
        out.write(final)

    cap.release()
    out.release()
    print(f"Видео сохранено в {output_path}")

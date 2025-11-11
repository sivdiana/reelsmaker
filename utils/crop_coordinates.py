import pandas as pd
from utils.one_euro_filter import OneEuroFilter
from utils.moving_average import moving_average

def detect_fragment_type(range_pair: list, dict_elements: dict) -> str:
    """
    Определяет тип фрагмента ("jump", "spin", "unknown") по диапазону кадров.

    Args:
        range_pair (list): Диапазон [start, end].
        dict_elements (dict): Словарь с типами фрагментов.

    Returns:
        str: Тип фрагмента.
    """
    if range_pair in dict_elements.get("jump_ranges_normal", []):
        return "jump"
    elif range_pair in dict_elements.get("spin_ranges_normal", []):
        return "spin"
    return "unknown"

def crop_coordinates(coords_df: pd.DataFrame,
                     all_ranges: list,
                     dict_elements: dict,
                     fps: float,
                     frame_width: int,
                     frame_height: int,
                     window: int = 5) -> tuple[list[dict], int, int]:
    """
    Строит прямоугольники (crop box) для каждого кадра на основе координат.

    Args:
        coords_df (pd.DataFrame): Координаты скелета.
        all_ranges (list): Список диапазонов кадров.
        dict_elements (dict): Типы фрагментов.
        fps (float): Частота кадров.
        frame_width (int): Ширина кадра.
        frame_height (int): Высота кадра.
        window (int): Размер окна сглаживания.

    Returns:
        list[dict]: Кропы по кадрам.
        int: Ширина кропа.
        int: Высота кропа.
    """
    fragment_boxes = []
    crop_height = frame_height
    crop_width = int(crop_height * 9 / 16)
    crop_width += int(crop_width * 0.1)  # небольшой запас
    half_w = crop_width // 2

    for (start, end) in all_ranges:
        fragment_type = detect_fragment_type([start, end], dict_elements)
        if fragment_type == "jump":
            min_cutoff = 0.2
            beta = 0.001
        elif fragment_type == "spin":
            min_cutoff = 0.08
            beta = 0.00005
        else:
            min_cutoff = 0.1
            beta = 0.0001

        raw_cx = []
        for f in range(start, end + 1):
            df_frame = coords_df[coords_df['frame'] == f]
            x_min = df_frame['x'].min()
            x_max = df_frame['x'].max()
            cx = ((x_min + x_max) / 2) * frame_width
            raw_cx.append(cx)

        pad_len = 15
        padded = [raw_cx[0]] * pad_len + raw_cx + [raw_cx[-1]] * pad_len
        smooth_fwd = moving_average(padded, window)
        smooth_bwd = moving_average(padded[::-1], window)[::-1]
        smoothed = [(a + b) / 2 for a, b in zip(smooth_fwd, smooth_bwd)][pad_len:-pad_len]

        euro = OneEuroFilter(freq=fps, min_cutoff=min_cutoff, beta=beta)
        final_cx = [euro.filter(x, t=i / fps) for i, x in enumerate(smoothed)]

        for i, f in enumerate(range(start, end + 1)):
            cx = int(final_cx[i])
            x1 = cx - half_w
            x2 = cx + half_w
            y1 = 0
            y2 = crop_height

            fragment_boxes.append({
                'frame': f,
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2
            })

    return fragment_boxes, crop_width, crop_height

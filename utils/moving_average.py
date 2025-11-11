import numpy as np

def moving_average(seq: list, window: int) -> list:
    """
    Скользящее среднее для сглаживания последовательности.

    Args:
        seq (list): Последовательность значений.
        window (int): Размер окна сглаживания.

    Returns:
        list: Сглаженная последовательность.
    """
    return np.convolve(seq, np.ones(window)/window, mode='same').tolist()

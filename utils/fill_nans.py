import pandas as pd

def fill_nans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Заполняет пропущенные значения координат линейной интерполяцией.

    Args:
        df (pd.DataFrame): Датафрейм с координатами.

    Returns:
        pd.DataFrame: Обновлённый датафрейм.
    """
    df[['x', 'y', 'z']] = df[['x', 'y', 'z']].interpolate(method='linear', limit_direction='both')
    if df[['x', 'y', 'z']].isna().any().any():
        print("Ошибка: остались незаполненные значения.")
    return df

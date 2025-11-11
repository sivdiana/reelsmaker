# Video Processor Project

Обработка видео по фигурному катанию с извлечением координат поз, сегментацией прыжков и вращений, а также сохранением обработанного результата. Финальное видео автоматически обрезается и центрируется вокруг фигуриста, чтобы обеспечить стабильный фокус на спортсмене. Используется модель pose_landmarker_lite.task из MediaPipe.

---

## Возможности

- Извлечение координат с помощью [MediaPipe Pose Landmarker Lite](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)
- Заполнение пропущенных точек линейной интерполяцией
- Сглаживание траектории с использованием:
  - Скользящего среднего
  - One Euro Filter
- Автоматический расчёт области crop вокруг фигуриста (по типу фрагмента: прыжок/вращение)
- Генерация видео в формате 9:16

---
## Запуск через терминал

**conda env create -f environment.yml**

**conda activate fskate**

В main.py задаются пути и диапазоны кадров:

path_to_input_video = "input/input_video.mp4"

path_to_output_video = "output/output_video.mp4"

Загрузить видео на сайт https://apireels.sportchamp.ru/interface2/

Значения словаря dict_elements заполняются данными jump_ranges_normal,spin_ranges_normal с сайта
dict_elements = 
{

    "jump_ranges_normal": [[2801, 3357], [4481, 4695], [5651, 5853], [7079, 7641]],
    "spin_ranges_normal": [[1360, 1478], [2369, 2481], [6101, 6207], [6251, 6363], [6821, 6945]]

}

Далее в терминале запустить алгоритм c помощью **python main.py**

---
## Структура проекта

project/

├── main.py

├── config.py

├── requirements.txt

├── pose_landmarker_lite.task

├── utils/

│ ├── crop_coordinates.py

│ ├── fill_nans.py

│ ├── get_coords.py

│ ├── get_video_info.py

│ ├── make_final_video.py

│ ├── moving_average.py

│ ├── one_euro_filter.py



Настройки модели в config.py:

MODEL_PATH = "pose_landmarker_lite.task"

NUM_POSES = 1

MIN_DETECTION_CONFIDENCE = 0.5

MIN_PRESENCE_CONFIDENCE = 0.5

MIN_TRACKING_CONFIDENCE = 0.5

CALCULATE_MASKS = False
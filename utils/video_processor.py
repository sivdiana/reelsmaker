from utils.get_video_info import get_video_information
from utils.get_coords import get_coords
from utils.fill_nans import fill_nans
from utils.crop_coordinates import crop_coordinates
from utils.make_final_video import make_final_video

class VideoProcessor:
    def __init__(self, path_to_input_video: str,
                 dict_elements: dict,
                 path_to_output_video: str):
        self.path_to_input_video = path_to_input_video
        self.dict_elements = dict_elements
        self.path_to_output_video = path_to_output_video
        self.all_ranges = sum(dict_elements.values(), [])

        self.coords_df = None
        self.frame_width = None
        self.frame_height = None
        self.fps = None

    def get_video_information(self):
        self.frame_width, self.frame_height, self.fps = get_video_information(self.path_to_input_video)

    def get_landmarks(self):
        self.coords_df = get_coords(self.path_to_input_video, self.all_ranges)
        if self.coords_df.empty:
            raise ValueError('Ошибка: координаты не извлечены.')

    def fill_missing_values(self):
        self.coords_df = fill_nans(self.coords_df)

    def get_frame_crops(self):
        boxes, crop_width, crop_height = crop_coordinates(
            self.coords_df,
            self.all_ranges,
            self.dict_elements,
            self.fps,
            self.frame_width,
            self.frame_height)
        make_final_video(self.path_to_input_video,
                         boxes,
                         self.path_to_output_video,
                         crop_width,
                         crop_height,
                         self.fps,
                         self.frame_height,
                         self.frame_width)

    def run(self):
        self.get_video_information()
        self.get_landmarks()
        self.fill_missing_values()
        self.get_frame_crops()

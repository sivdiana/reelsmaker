from utils.video_processor import VideoProcessor

if __name__ == "__main__":
    path_to_input_video = "input/input_video.mp4"
    path_to_output_video = "output/output_video.mp4"

    dict_elements = {
        "jump_ranges_normal": [[2801, 3357], [4481, 4695], [5651, 5853], [7079, 7641]],
        "spin_ranges_normal": [[1360, 1478], [2369, 2481], [6101, 6207], [6251, 6363], [6821, 6945]]
    }

    processor = VideoProcessor(path_to_input_video, dict_elements, path_to_output_video)
    processor.run()

from utils.video_processor import VideoProcessor

if __name__ == "__main__":
    path_to_input_video = "input/test.mp4"
    path_to_output_video = "output1/test.mp4"

    dict_elements = {
        "jump_ranges_normal": [[590,680],[1430,1500],[2430,2540]],
        "spin_ranges_normal": [[1575,1880], [2580,3000],[3960, 4240]]
    }

    processor = VideoProcessor(path_to_input_video, dict_elements, path_to_output_video)
    processor.run()
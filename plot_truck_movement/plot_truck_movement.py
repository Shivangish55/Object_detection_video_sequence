import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def read_detections_from_folder(folder_path):
    detections = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    frame_num = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])
                    detections.append((frame_num, x, y, width, height))
    return detections

def map_to_2d_image(video_coord, video_frame_dims, road_coords):
    (x, y) = video_coord
    (frame_width, frame_height) = video_frame_dims
    (road_x1, road_y1, road_x2, road_y2) = road_coords

    scale_x = (road_x2 - road_x1) / frame_width
    scale_y = (road_y2 - road_y1) / frame_height

    mapped_x = road_x1 + x * scale_x
    mapped_y = road_y1 + y * scale_y

    return (mapped_x, mapped_y)

def plot_truck_movement(detections, video_frame_dims, road_coords, image_path):
    img = plt.imread(image_path)
    fig, ax = plt.subplots()
    ax.imshow(img)

    for detection in detections:
        frame_num, x, y, width, height = detection
        center_x = x + width / 2
        center_y = y + height / 2
        mapped_coord = map_to_2d_image((center_x, center_y), video_frame_dims, road_coords)
        ax.plot(mapped_coord[0], mapped_coord[1], 'ro', markersize=5)  # Plotting as red dots with size 5

    road_x1, road_y1, road_x2, road_y2 = road_coords
    rect = Rectangle((road_x1, road_y1), road_x2 - road_x1, road_y2 - road_y1, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

    plt.show()

if __name__ == "__main__":
    video_frame_dims = (1280, 720) 
    road_coords = (466, 357, 911, 355)  
    image_path = '2D image.png'  
    detections_folder_path = 'runs/detect/exp18/labels'  

    detections = read_detections_from_folder(detections_folder_path)
    plot_truck_movement(detections, video_frame_dims, road_coords, image_path)


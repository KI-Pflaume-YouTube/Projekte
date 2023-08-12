# Panormana Bild in Video umwandeln | 60 FPS | 20 Sekunden

import imageio
import numpy as np

# Laden Sie das hochgeladene Bild
image_path = "d:/PythonProjekte/Bilder_hochskalieren/this.png"
image = imageio.v2.imread(image_path)

# Holen Sie sich die Dimensionen des Bildes
height, width, channels = image.shape

# Schneiden Sie die Bildbreite und -höhe so zu, dass sie durch 16 teilbar sind
new_width = width - (width % 16)
new_height = height - (height % 16)
image_cropped = image[:new_height, :new_width, :]

# Bestimmen Sie die Größe des 16:9 Video-Frames
video_height = new_height
video_width = int(video_height * 16 / 9)

# Definieren Sie die Schwenkpositionen
start_position = 0
center_position = (new_width - video_width) // 2
end_position = new_width - video_width

# Berechnen Sie den erforderlichen Frame-Schritt für ein 20-Sekunden-Video mit 60 fps
required_frame_step = (end_position - start_position) / (20 * 60)
adjusted_frame_step = round(required_frame_step)

# Definieren Sie den Pfad zum Speichern des Videos
video_path = "d:/PythonProjekte/panorama_video2.mp4"

# Erstellen Sie einen Video-Writer mit der flüssigeren Bildrate und setzen Sie macro_block_size auf 1
writer = imageio.get_writer(video_path, fps=60, quality=9, macro_block_size=1)

# Erzeugen Sie Frames und speichern Sie das Video mit der angepassten Bildrate und dem Frame-Schritt
for position in range(start_position, end_position + 1, adjusted_frame_step):
    frame = image_cropped[:, position:position + video_width, :]
    writer.append_data(frame)

writer.close()

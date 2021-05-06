import json

# from functools import partial
# from multiprocessing.pool import Pool
from PIL import Image

import os
import cv2
import pafy


# AAA
URL =  r"https://youtu.be/FtutLA63Cp8" # Bad Apple
#URL =  r'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Never gonna

# Output Parameters
OUTPUT_WIDTH = 36
OUTPUT_HEIGHT = 28

# Paths
OUTPUT_PATH = r"BadAppleFrameData.json"

# result
result_frames = []


#
def process_video_parallel(url, skip_frames, process_number):
    """
    :param url: String
    :param skip_frames:
    :param process_number:
    :return:
    """
    cap = cv2.VideoCapture(url)
    # num_processes = os.cpu_count()
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  #
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print("***********************")
    print("Frames=", total_frames)
    print("Width=", width, ", Height=", height)
    print("FPS=", fps)
    print("***********************")
    # cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)

    frame_count = 0
    has_get_size = False
    use_resize = False

    # Loop through each frame
    while True:
        ret, frame = cap.read()

        # exit when finish playing
        if frame is None:
            break
        else:
            frame_count += 1
            if frame_count % 1000 == 0:
                print("Processed", frame_count, "frames...")
            # print("Frame", frame_count)

        # Get frame height and width
        # if width == 0:
        #     height, width, channels = frame.shape  # Accessing RGB pixel values

        # evaluate stuff
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # 因為 OpenCV是用B,G,R存，PIL是R,G,B , and PIL is faster on loading idk
        if not has_get_size:
            (w, h) = img.size
            use_resize = (w != OUTPUT_WIDTH or h != OUTPUT_HEIGHT)
            has_get_size = True
            print('WIDTH=%d, HEIGHT=%d, use_resize=%d'%(w, h, use_resize))
        if use_resize:
            img = img.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT))
            # print("USE RESIZE")
        pixels = img.load()

        matrix = []
        # evaluate all pixels
        for y in range(OUTPUT_HEIGHT):  # height
            row = []
            for x in range(OUTPUT_WIDTH):  # width
                # print(img[y, x])
                if pixels[x, y][0] < 128:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        result_frames.append(matrix)

        # show img
        cv2.imshow('Bad Apple!!', frame)
        if cv2.waitKey(3) & 0xFF == ord('q'): # #if 'q' key-pressed break out
            break
    cap.release()
    # return result_frames




# DL
def main():
    # ydl_opts = {}
    # ydl = youtube_dl.YoutubeDL(ydl_opts)
    # info_dict = ydl.extract_info(URL, download=False)
    #
    # formats = info_dict.get('formats', None)
    #
    #
    # for f in formats:
    #     if f.get('format_note', None) == '144p':
    #     url = f.get('url', None)
    vPafy = pafy.new(URL)
    play = vPafy.getbest()  # reftype="webm"
    url = play.url
    # url = r"/home/jcxyis/Downloads/videoplayback.mp4"  # for test
    print("Get Url=", url)

    print("Now Processing")
    process_video_parallel(url, 0, 300)
    with open(OUTPUT_PATH, 'w+') as f:
        json.dump(result_frames, f)
    print("Done! Data saved to %s" % OUTPUT_PATH)


if __name__ == '__main__':
    main()

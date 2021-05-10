import json
import threading

from PIL import Image

import os
import cv2
import pafy


# Url
URL =  r"https://youtu.be/FtutLA63Cp8"
#URL =  r'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Output Parameters
OUTPUT_MAX_WIDTH = 36
OUTPUT_MAX_HEIGHT = 28
OUTPUT_COLOR_COUNT = 2  # Color steps => 2:[0, 1], 3:[0, 1, 2]... less is darker
# OUTPUT_MAX_FPS = 30

# Paths
FRAME_DATA_PATH = r"output/FrameData.json"
AUDIO_PATH = r"output/music"


#
def process_video(url):
    """
    :param url: 影片原網址 (either local or remote)
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
    print("(Source) Width=", width, ", Height=", height)
    print("FPS=", fps)
    print("***********************")
    # cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)

    frame_count = 0
    use_resize = width > OUTPUT_MAX_WIDTH or height > OUTPUT_MAX_HEIGHT
    result_frames = []  # result

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
        if use_resize:
            img = img.resize((OUTPUT_MAX_WIDTH, OUTPUT_MAX_HEIGHT))
            # print("USE RESIZE")
        pixels = img.load()

        matrix = []
        # go through all pixels
        for y in range(OUTPUT_MAX_HEIGHT):  # height
            row = []
            for x in range(OUTPUT_MAX_WIDTH):  # width
                # print(img[y, x])
                # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
                gray = 0.2989 * pixels[x, y][0] + 0.5870 * pixels[x, y][1] + 0.1140 * pixels[x, y][2]
                for i in range(OUTPUT_COLOR_COUNT):
                    gray -= 256.0/OUTPUT_COLOR_COUNT
                    if gray <= 0:
                        row.append(OUTPUT_COLOR_COUNT-i-1)
                        break
                # if pixels[x, y][0] < 128:
                #     row.append(1)
                # else:
                #     row.append(0)
            matrix.append(row)
        result_frames.append(matrix)

        # show img
        # cv2.imshow('Bad Apple!!', frame)
        # if cv2.waitKey(3) & 0xFF == ord('q'): # #if 'q' key-pressed break out
        #     break
    cap.release()

    # Write File
    print("process done! now saving...")
    output_data = {
        "fps": fps,
        "frames": len(result_frames),
        "colors": OUTPUT_COLOR_COUNT,
        "width": len(result_frames[0][0]),
        "height": len(result_frames[0]),
        "data": result_frames,
    }
    with open(FRAME_DATA_PATH, 'w+') as f:
        json.dump(output_data, f)
    print("Done! Data saved to %s" % FRAME_DATA_PATH)
    # return result_frames


def download_audio(pafyObj):
    if os.path.exists(AUDIO_PATH):
        os.remove(AUDIO_PATH)
    aud = pafyObj.getbestaudio()
    aud.download(filepath=AUDIO_PATH)
    print("Audio saved to", AUDIO_PATH, "(Format=", aud.extension, ")")


# DL
def main(url=URL):
    # init folder
    os.makedirs(os.path.dirname(FRAME_DATA_PATH), exist_ok=True)

    vPafy = pafy.new(url)
    play = vPafy.getbest()  # reftype="webm"
    video_url = play.url
    # url = r"/home/jcxyis/Downloads/videoplayback.mp4"  # for test
    print("Get Url=", video_url)

    print("Now Processing")
    threading.Thread(target=download_audio, args=(vPafy,)).start()  # download_audio(vPafy)
    process_video(video_url)


if __name__ == '__main__':
    main(URL)

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
OUTPUT_WIDTH = 36
OUTPUT_HEIGHT = 28

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
    print("Width=", width, ", Height=", height)
    print("FPS=", fps)
    print("***********************")
    # cap.set(cv2.CAP_PROP_POS_FRAMES, frames_per_process * process_number)

    frame_count = 0
    has_get_size = False
    use_resize = False
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
        # cv2.imshow('Bad Apple!!', frame)
        # if cv2.waitKey(3) & 0xFF == ord('q'): # #if 'q' key-pressed break out
        #     break
    cap.release()

    print("process done! now saving...")
    with open(FRAME_DATA_PATH, 'w+') as f:
        json.dump(result_frames, f)
    print("Done! Data saved to %s" % FRAME_DATA_PATH)
    # return result_frames


def download_audio(pafyObj):
    aud = pafyObj.getbestaudio()
    aud.download(filepath=AUDIO_PATH)
    print("Audio saved to", AUDIO_PATH, "(Format=", aud.extension, ")")


# DL
def main():
    # init folder
    os.makedirs(os.path.dirname(FRAME_DATA_PATH), exist_ok=True)

    vPafy = pafy.new(URL)
    play = vPafy.getbest()  # reftype="webm"
    url = play.url
    # url = r"/home/jcxyis/Downloads/videoplayback.mp4"  # for test
    print("Get Url=", url)

    print("Now Processing")
    threading.Thread(target=download_audio, args=(vPafy,)).start()  # download_audio(vPafy)
    process_video(url)


if __name__ == '__main__':
    main()

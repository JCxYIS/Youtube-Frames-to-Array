# Youtube-Frames-to-Array

Bad Apple Preprocessing  
Turn youtube video into a 3D array `([frame][y][x])`

## How to use
- (optional) create a python venv
- install required packages `pip install -r requirements.txt`
- run `runtestserver.py`
- go http://localhost:8763 //TODO  

## 程式與功能說明
### `runserver.py` (API)
會在 8763 port 開啟一個服務。有以下的 route：
- `refresh/`: 需要用 POST 存取，並提供一個 youtube 影片的網址(`url`)。會呼叫 `preprocess`來處理這支影片，並在完成時丟回一個回應
- `output/`: 會回傳把處理好的 json 檔
- `audio/`: 會回傳下載好的音檔 (沒有副標題，但對於瀏覽器沒差)

### `preprocess.py` (core)
處理影片的主要程式，有以下幾個設定參數
- `URL`： Youtube 影片網址
- `OUTPUT_MAX_WIDTH`：輸出寬度最多為幾格
- `OUTPUT_MAX_HEIGHT`：輸出高度最多為幾格
- `OUTPUT_COLOR_COUNT`：要分成幾種色彩？ 如：2 代表就只有 0 跟 1 兩種顏色
- `FRAME_DATA_PATH`、`AUDIO_PATH` 一些路徑設定

#### Exported JSON format
```json
{
    "fps": fps of the data,
    "frames":  how many frames in data (== data.length),
    "colors": how many colors in data,
    "width": frame width (== data[x][x].length),
    "height": frame height (== data[x].length),
    "data": the 3D array of the result,
}
```

---

> see also https://github.com/JCxYIS/ncueeclass-yt-player
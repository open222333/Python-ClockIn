# clock_in_python

```
google表單 自動填入
```

# 步驟

1. 根據 `config/config.ini.default` 建立 `config/config.ini`，並填寫相關參數

2. 根據 `config/setting.json.default` 建立 `config/setting.json`，並填寫相關參數

3. 根據Chrome版本，下載[ChromeDriver](https://chromedriver.chromium.org/downloads)

	- [查看 Google Chrome 版本](https://support.google.com/chrome/answer/95414?hl=zh-Hant&co=GENIE.Platform%3DDesktop#zippy=%2C%E6%AA%A2%E6%9F%A5%E6%9B%B4%E6%96%B0%E5%8F%8A%E6%9F%A5%E7%9C%8B%E7%9B%AE%E5%89%8D%E7%9A%84%E7%80%8F%E8%A6%BD%E5%99%A8%E7%89%88%E6%9C%AC)

	```
	檢查更新及查看目前的瀏覽器版本
		在電腦上開啟 Chrome。
		按一下右上方的「更多」圖示 更多。
		依序按一下 [說明] 下一步 [關於 Google Chrome]。
		Google Chrome 標題下方顯示的一連串數字就是目前的版本號碼。
		當您開啟這個頁面時，Chrome 就會自動檢查更新。
	```

4. 執行 main.py

	```bash
	git clone https://github.com/open222333/Python-Clock_In.git clock_in
	cd clock_in
	pip install -r requirements.txt
	python main.py
	```

## config.ini

```ini
[INFO]
; google表單網址(必填)
FORM_URL=

; driver路徑
; DRIVER_PATH=

; 使用 selenium 套件，1為開啟 0為關閉 預設為關閉, 使用 requests
; USE_SELENIUM=

; 使用者資訊json位置 預設 config/setting.json
; USER_SETTING_PATH=

; log紀錄位置 預設 log
; LOG_DIR_PATH=

; 會將大量訊息存入log 是否開啟DEBUG，1為開啟 0為關閉 預設為關閉
; DEBUG=

; log紀錄名稱 預設 2023-01-01.log
; LOG_FILE_NAME=

; error log紀錄名稱 預設 error-2023-01-01.log
; ERROR_LOG_FILE_NAME=

; schedule log紀錄名稱 預設 schedule-2023-01-01.log
; SCHEDULE_LOG_FILE_NAME=

; 排班時間設定json檔路徑 預設 config/shift.json
; SHIFT_JSON_FILE_PATH=

; 創建天數超過指定天數 刪除log 預設 7
; REMOVE_LOG_DAYS

[RANDOM]
; 隨機時間 單位分鐘
; MAX_MINUTE=
; MIN_MINUTE=

[XPATH]
; selenium 使用xpath
; NAME_XPATH=
; SHIFT_M_ON_XPATH=
; SHIFT_M_OFF_XPATH=
; SHIFT_N_ON_XPATH=
; SHIFT_N_OFF_XPATH=
; SHIFT_G_ON_XPATH=
; SHIFT_G_OFF_XPATH=
; SUBMIT_XPATH=

[SELECTOR]
; requests bs4使用 selector
; SELECTOR_POST_URL=
; SELECTOR_NAME_COLUMN =
; SELECTOR_CLOCK_IN=
; SELECTOR_CLOCK_OFF=

; 欄位名稱
; MORNING_MSG=
; NIGHT_MSG=
; GRAVEYARD_MSG=
```

## setting.json

### 格式

```
"名字": {
	"shift": "班別" 早班 中班 晚班
	"day_off": [1,2,3,4,5,6,7] (休假日) 星期一:1 ~ 星期日:7
}
```

### json檔 範例

```json
{
  "David": {
    "shift": "早班",
    "day_off": [1, 2]
  },
  "Tom": {
    "shift": "中班",
    "day_off": [6, 7]
  },
  "Joe": {
    "shift": "晚班",
    "day_off": [4, 5]
  }
}
```
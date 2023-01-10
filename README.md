# clock_in_python

```
google表單 自動填入
```

# 步驟

1. 根據 `config/config.ini.default` 建立 `config/config.ini`，並填寫相關參數

2. 根據 `config/setting.json.default` 建立 `config/setting.json`，並填寫相關參數

3. 執行 main.py

```bash
python path_to_workdir/main.py
```

## config.ini

```ini
[INFO]
; google表單網址
FORM_URL=

; driver路徑
DRIVER_PATH=

; 使用者資訊json位置 預設 config/setting.json
USER_SETTING_PATH=

; log紀錄位置 預設 log/2023-01-01.log
LOG_FILE_PATH=

; error log紀錄位置 預設 log/error-2023-01-01.log
ERROR_LOG_FILE_PATH=
```

## setting.json

```json
{
  // 設置資訊
  "Tom": {
	// 班別
    "shitf": "中班",
	// 休假 星期一:1  星期日:7
    "day_off": [6, 7]
  },
  "David": {
    "shitf": "早班",
    "day_off": [1, 2]
  }
}
```
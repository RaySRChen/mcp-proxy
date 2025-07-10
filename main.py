import json
import os
from typing import Dict

# 確保你已經安裝了 python-dotenv
# 在終端機中執行: pip install python-dotenv
from dotenv import load_dotenv


def load_config_from_template(json_path: str) -> Dict:
    """
    從 JSON 樣板檔案載入設定，並用環境變數替換其中的佔位符。

    Args:
        json_path (str): servers.json 樣板檔案的路徑。

    Returns:
        Dict: 包含真實祕密值的最終設定字典。
    """
    print(f"正在從 '{json_path}' 載入設定樣板...")

    # 步驟 1: 載入 .env 檔案中的環境變數到系統中
    # 這會讓 os.environ.get('YOUR_VAR') 能夠讀取到 .env 裡的值
    load_dotenv()
    print(".env 檔案中的環境變數已載入。")

    try:
        # 步驟 2: 讀取 JSON 樣板檔案成為一個純文字字串
        with open(json_path, 'r', encoding='utf-8') as f:
            template_string = f.read()

        # 步驟 3: 使用環境變數替換字串中的 ${VAR} 或 $VAR 佔位符
        # 這是最關鍵的一步，os.path.expandvars 會自動完成替換
        print("正在用環境變數替換設定中的佔位符...")
        expanded_string = os.path.expandvars(template_string)

        # 步驟 4: 將這個處理過的字串解析為最終的 Python 字典物件
        final_config = json.loads(expanded_string)
        print("設定載入並組合成功！")

        return final_config

    except FileNotFoundError:
        print(f"錯誤: 找不到設定檔 '{json_path}'。請確認檔案是否存在。")
        return {}
    except json.JSONDecodeError:
        print(f"錯誤: 解析 '{json_path}' 失敗。請確認其為有效的 JSON 格式。")
        return {}
    except Exception as e:
        print(f"發生未知錯誤: {e}")
        return {}


# --- 主程式執行區塊 ---
if __name__ == "__main__":
    # 設定檔的路徑
    CONFIG_FILE_PATH = 'servers.json'
    
    # 執行我們的函式來取得最終設定
    my_app_config = load_config_from_template(CONFIG_FILE_PATH)

    # 如果設定成功載入，就印出來看看結果
    if my_app_config:
        print("\n--- 最終設定內容 ---")
        # 使用 json.dumps 美化輸出，方便閱讀
        print(json.dumps(my_app_config, indent=2, ensure_ascii=False))

        print("\n--- 如何使用設定 ---")
        # 示範如何取得特定設定值
        try:
            line_bot_token = my_app_config['mcpServers']['line-bot']['env']['CHANNEL_ACCESS_TOKEN']
            print(f"成功讀取 LINE Bot Token 的前 10 個字元: {line_bot_token[:10]}...")
        except KeyError:
            print("在設定中找不到 LINE Bot Token。")
import requests
from bs4 import BeautifulSoup
import os

# --- 配置区域 ---
# 目标网址
URL = "http://www.gyruibo4.cn/WxSearch/GetRoomInfo?Apartid=48&Roomname=8112"
# 从环境变量读取 SERVER_KEY (GitHub Secrets)
SERVER_KEY = os.environ.get("SERVER_KEY")
# 预警阈值
THRESHOLD = 10.0
# ---------------

def send_to_server_chan():
    """通过 Server 酱 POST 方式发送自定义提醒"""
    if not SERVER_KEY:
        return
    
    # 使用官方推荐的 POST 接口
    push_url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"
    
    # 明确将 title 和 desp 放入数据中
    data = {
        "title": "电费预警",
        "desp": "电费过低咯～快交电费啦!"
    }

    
    try:
        requests.post(push_url, data=data)
        print("推送发送成功")
    except Exception as e:
        print(f"推送失败: {e}")

def check_power():
    try:
        # 获取网页数据
        response = requests.get(URL, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取剩余电量 (根据之前分析，第三个 infolab 标签为剩余电量)
        info_labels = soup.find_all('label', class_='infolab')
        if len(info_labels) < 3:
            print("未能成功获取电量数据标签")
            return

        remaining_power_str = info_labels[2].text.strip().replace(' 度', '')
        remaining_power = float(remaining_power_str)
        
        print(f"当前剩余电量: {remaining_power} 度")
        
        # 逻辑判断
        if remaining_power < THRESHOLD:
            title = "电费预警"
            msg = f"宿舍 8112 当前剩余电量仅剩 {remaining_power} 度，请及时充值！"
            send_to_server_chan(title, msg)
        else:
            print("电量充足，无需提醒")
            
    except Exception as e:
        print(f"查询出错: {e}")
        send_to_server_chan("电费查询错误", f"查询脚本运行出错: {str(e)}")

if __name__ == "__main__":
    check_power()

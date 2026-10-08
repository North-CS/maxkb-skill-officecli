import json
import os
import sys
import requests
import tempfile

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(tempfile.gettempdir(), "officecli")
os.makedirs(TMP_DIR, exist_ok=True)


def _load_env():
    """从 .env 文件加载环境变量"""
    env_path = os.path.join(SKILL_DIR, ".env")
    env = {}
    if os.path.isfile(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env[key.strip()] = value.strip()
    return env


def main(user_file: list):
    """
        下载文件到 /tmp/officecli 目录，base_url 从 .env 读取
    """
    env = _load_env()
    base_url = env.get("BASE_URL")
    if not base_url:
        raise ValueError("启动参数 BASE_URL 未设置")
    clean_base_url = base_url.rstrip("/")
    result = []

    for file_info in user_file:
        file_name = file_info["name"]
        relative_url = file_info["url"]

        # 处理相对路径（去掉开头的 './'）
        if relative_url.startswith("./"):
            relative_url = relative_url[2:]

        # 下载文件（新版本服务端要求携带认证请求头）
        api_key = env.get("API_KEY")
        if api_key:
            headers = {"Authorization": f"Bearer {api_key}"}
        else:
            headers = {}
        download_url = f"{clean_base_url}/{relative_url.lstrip('/')}"
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 保存文件，保留原文件名
        save_path = os.path.join(TMP_DIR, file_name)
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
            result.append(save_path)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python scripts/download_user_file.py '<json>'")
        print('示例: python scripts/download_user_file.py \'[{"name":"example.docx","url":"./oss/file/xxxx"}]\'')
        sys.exit(1)
    file_list = json.loads(sys.argv[1])
    result = main(file_list)
    print(result)
    print("文件已下载到/tmp/officecli目录下，如需验证文件和读取内容使用python代码，而不是ls和read_file工具")

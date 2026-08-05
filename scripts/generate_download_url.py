import requests
import os
import tempfile
import mimetypes

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = os.path.join(tempfile.gettempdir(), "officecli")

# 完整的 Microsoft Office 文件后缀集合（小写）
OFFICE_EXTENSIONS = {
    '.doc', '.docx', '.docm', '.dot', '.dotx', '.dotm',
    '.xls', '.xlsx', '.xlsm', '.xlt', '.xltx', '.xltm', '.xlsb', '.xlam',
    '.ppt', '.pptx', '.pptm', '.pot', '.potx', '.potm',
    '.pps', '.ppsx', '.ppsm', '.ppam',
}


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


def _upload_file(file_name, base_url, token):
    """上传单个文件并返回下载链接"""
    filepath = os.path.join(TMP_DIR, file_name)
    clean_base_url = base_url.rstrip('/')

    with open(filepath, 'rb') as f:
        content = f.read()
    mime = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
    resp = requests.post(
        url=f"{clean_base_url}/api/oss/file",
        headers={"Authorization": f"Bearer {token}"},
        data={"source_id": "SYSTEM", "source_type": "SYSTEM"},
        files={'file': (file_name, content, mime)}
    )
    if resp.status_code == 200:
        data = resp.json().get("data")
        url = f"{clean_base_url}/{data.lstrip('./')}"
        return f"- [{file_name}]({url})"

    return None


def main(files=None):
    """
    遍历 /tmp/officecli 下所有 Office 文件，上传并返回下载链接。
    base_url 和 api_token 从 .env 读取。
    """
    env = _load_env()
    base_url = env.get("BASE_URL")
    token = env.get("API_KEY")
    if not base_url:
        raise ValueError("启动参数 BASE_URL 未设置")
    if not token:
        raise ValueError("启动参数 API_KEY 未设置")

    if not os.path.isdir(TMP_DIR):
        return "目录 /tmp/officecli 不存在"

    if not files:
        # 自动获取目录下所有文件，并只保留 Office 后缀的文件
        all_files = [f for f in os.listdir(TMP_DIR)
                     if os.path.isfile(os.path.join(TMP_DIR, f))]
        files = [f for f in all_files
                 if os.path.splitext(f)[1].lower() in OFFICE_EXTENSIONS]
        if not files:
            return "/tmp/officecli 下没有 Office 文件"

    links = []
    errors = []
    for file_name in files:
        result = _upload_file(file_name, base_url, token)
        if result:
            links.append(result)
        else:
            errors.append(file_name)

    output = "## 文件下载链接\n" + "\n".join(links)
    if errors:
        output += "\n\n## 上传失败\n" + "\n".join(f"- {f}" for f in errors)
    return output


if __name__ == "__main__":
    print(main())

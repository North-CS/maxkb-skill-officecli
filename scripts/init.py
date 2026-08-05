import os
import shutil
import tempfile

TMP_DIR = os.path.join(tempfile.gettempdir(), "officecli")


def main():
    """清理 /tmp/officecli 下所有文件，然后重建空目录"""
    if os.path.isdir(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    os.makedirs(TMP_DIR, exist_ok=True)


if __name__ == "__main__":
    main()
    print("初始化成功,/tmp/officecli目录已创建，如需验证使用python代码，而不是ls工具")

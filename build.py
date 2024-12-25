import subprocess
# "D://minianaconda//envs//pyside6//python.exe"
args = [
    f'{"python"} -m nuitka',
    '--standalone',
    f'--windows-console-mode=disable',
    '--enable-plugins=pyside6',
    '--nofollow-imports',
    f'--output-dir=out',
    '--show-progress',
    '--remove-output',
    f'main.py'
]
print(args)
process = subprocess.Popen(" ".join(args),shell=True,
                           stdin=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           stdout=subprocess.PIPE,
                           errors='ignore')
for line in process.stdout:
    print(line.strip())

# 检查脚本的返回码
if process.returncode != 0:
    print(f"脚本执行失败，返回码：{process.returncode}")
    # 可以选择打印stderr以获取更多错误信息
    print(process.stderr)
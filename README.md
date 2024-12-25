# pyside6-tools
基于pyside6制作的工具集合

## 文件目录结构
```shell
pyside6-tools
├── app
│   ├── common
│   ├── components
│   ├── gui
│   ├── recource
│   ├── view
├── README.md
├── main.py
├── nuitka_standalone_windows.sh
└── requirements.txt
```
## 安装部署
```shell
git clone https://github.com/xiaohuihui-com/pyside6-tools.git
cd pyside6-tools
pip install -r requirements.txt
python main.py
```
- 关闭ssl验证，可以加速github远程仓库连接，避免连接超时
    ```shell
    git config --global http.sslVerify false
    ```
## 基于百度语音的识别语音，转文字

### 准备工具

pip install pyaudio (这个可能最难安装，pip install XXX.whl)

##### 安装pyaudio出问题，请在https://www.lfd.uci.edu/~gohlke/pythonlibs/
##### 上面查看，我python版本是3.9，所以下载3.9即可。 
pip install wave 
pip install baidu-aip

### 2个文件最好放在同一文件。

### 配置文件

##### 在setting.py 里面 写好 必要配置

### 运行软件
##### 若无GUI界面则运行
python asr.py
##### 想要界面则运行
python asr_ui.py


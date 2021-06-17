# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workers\python项目\自创Python开发项目\课堂云语音\asr\asr.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import sys
import time
import pyaudio
import wave
import os
from aip import speech
import threading
from PyQt5 import QtCore, QtGui, QtWidgets


def Build_new_field(new_field_path):
    #     # 创建文件夹
    isExists = os.path.exists(new_field_path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(new_field_path)
        s = new_field_path + ' 创建成功'
        return s
    else:
        # 如果目录存在则不创建，并提示目录已存在
        s = new_field_path + ' 目录已存在'
        return s


def spell_path():
    path = 'e:\\语音库'
    Build_new_field(path)
    return path


class Ui_Form(QtWidgets.QWidget):
    signal_write_msg = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.setupUi()
        self.show()
        self.signal_write_msg.connect(self.write_msg)
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def setupUi(self):
        self.setWindowTitle("实时语音转文字")
        self.resize(640, 480)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(280, 20, 80, 30))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(20, 60, 601, 401))
        self.textEdit.setObjectName("textEdit")
        self.pushButton.setText("录音")

    def gettime(self):
        # ↓录音时间
        name = ''
        t = time.localtime()
        for i in range(0, 6):
            name += str(t[i])
            if i in [3, 4]:
                name += ':'
            elif i == 5:
                pass
            else:
                name += '-'
        name = name.replace(':', '')
        return name
        # print(name)
        # ↑录音时间

    # 录音函数
    def speech(self):
        CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1  # 声道
        self.RATE = 8000
        RECORD_SECONDS = 10  # 录音10秒
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=CHUNK)

        start = ("* 开始录音，您有%d秒时间输入语音内容！" % RECORD_SECONDS)
        self.signal_write_msg.emit(start)
        self.frames = []
        for i in range(0, int(self.RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            self.frames.append(data)
        end = ("* 录音结束")
        self.signal_write_msg.emit(end)
        stream.stop_stream()
        stream.close()
        p.terminate()  # 释放portaudio资源

        WAVE_OUTPUT_FILENAME = self.gettime() + '.wav'
        self.output_path = spell_path() + '\\' + WAVE_OUTPUT_FILENAME
        print(self.output_path)
        # with open(output_path, 'wb')as f:
        #     f.write('')
        #     f.close()
        print('创建新文件:%s' % self.output_path)
        # self.get_file_path(output_path)
        # print(output_path)
        wf = wave.open(self.output_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        with open(self.output_path, 'rb') as f:
            s = f.read()
            self.Baidu_speech_Api(s)

    def Baidu_speech_Api(self, fp):
        app_id = '18559488'
        app_key = 'ehYyckmKcAPCuvNOGOcFEGbw'
        secret_key = 'L3GTTtRz6ItgSzzyrwZbRBIGSXeLr9V0'
        client = speech.AipSpeech(app_id, app_key, secret_key)

        result = client.asr(fp, 'wav', 8000, {"dev_pid": 1537})
        # print(result)
        result_list = list(result.values())
        if 'success.' in result_list:
            msg = ('根据语音转文字，你说的是：\n%s' % result['result'][0]) + '\n'
            self.signal_write_msg.emit(msg)
            # i = self.data()[Number]
            # print(i)
        else:
            Number = result['err_no']
            if Number in result_list:
                i = self.data()[str(Number)]
                print(i)
            else:
                print('找不到匹配，请到官网看看错误码')

    def data(self):
        json = {
            "3300": "用户输入错误	输入参数不正确	请仔细核对文档及参照demo，核对输入参数",
            "3301": "用户输入错误	音频质量过差	请上传清晰的音频",
            "3302": "用户输入错误	鉴权失败	token字段校验失败。请使用正确的API_KEY 和 SECRET_KEY生成。或QPS、调用量超出限额。或音频采样率不正确（可尝试更换为16k采样率）。",
            "3303": "服务端问题	语音服务器后端问题	请将api返回结果反馈至论坛或者QQ群",
            "3304": "用户请求超限	用户的请求QPS超限	请降低识别api请求频率 （qps以appId计算，移动端如果共用则累计）",
            "3305": "用户请求超限	用户的日pv（日请求量）超限	请“申请提高配额”，如果暂未通过，请降低日请求量",
            "3307": "服务端问题	语音服务器后端识别出错问题	目前请确保16000的采样率音频时长低于30s。如果仍有问题，请将api返回结果反馈至论坛或者QQ群",
            "3308": "用户输入错误	音频过长	音频时长不超过60s，请将音频时长截取为60s以下",
            "3309": "用户输入错误	音频数据问题	服务端无法将音频转为pcm格式，可能是长度问题，音频格式问题等。 请将输入的音频时长截取为60s以下，并核对下音频的编码，是否是16K， 16bits，单声道。",
            "3310": "用户输入错误	输入的音频文件过大	语音文件共有3种输入方式： json 里的speech 参数（base64后）； 直接post 二进制数据，及callback参数里url。 分别对应三种情况：json超过10M；直接post的语音文件超过10M；callback里回调url的音频文件超过10M",
            "3311": "用户输入错误	采样率rate参数不在选项里	目前rate参数仅提供16000，填写4000即会有此错误",
            "3313": "用户输入错误	音频格式format参数不在选项里	目前格式仅仅支持pcm，wav或amr，如填写mp3即会有此错误"
        }
        return json

    def pushButton_clicked(self):
        # self.speech()
        self.threading = threading.Thread(target=self.speech)
        self.threading.start()

    def write_msg(self, msg):
        self.textEdit.append(msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    uf = Ui_Form()
    uf.show()
    sys.exit(app.exec_())

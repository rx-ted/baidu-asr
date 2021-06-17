import time
import pyaudio
import wave
import os
from aip import speech
import setting  # 自己设置


class REC():
    # 拼写
    def spell_path(self):
        path = os.getcwd()
        # print(path)
        path = path + '\\' + '语音库'
        self.Build_new_field(path)
        return path

    # 创建文件夹
    def Build_new_field(self, new_file_path):
        #     # 创建文件夹
        isExists = os.path.exists(new_file_path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(new_file_path)
            s = new_file_path + ' 创建成功'
            return s
        else:
            # 如果目录存在则不创建，并提示目录已存在
            s = new_file_path + ' 目录已存在'
            return s

    # 创建新的时间点
    def gettime(self):
        # ↓录音
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
        self.FORMAT = pyaudio.paInt16  # 16k
        self.CHANNELS = 1  # 声道 单通道
        self.RATE = 8000  # 采样率
        RECORD_SECONDS = 10  # 录音10秒
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        except Exception as e:
            print(e)
            print('设置-隐私-麦克风 下关闭/开启麦克风的应用访问权限')
            exit(0)

        '''
        self,
             PA_manager: Any,
             rate: Any,
             channels: Any,
             format: Any,
             input: bool = False,
             output: bool = False,
             input_device_index: Any = None,
             output_device_index: Any = None,
             frames_per_buffer: int = 1024,
             start: bool = True,
             input_host_api_specific_stream_info: Any = None,
             output_host_api_specific_stream_info: Any = None,
             stream_callback: Any = None
        
        '''

        print("* 开始录音，您有%d秒时间输入语音内容！" % RECORD_SECONDS)
        self.frames = []
        for i in range(0, int(self.RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            self.frames.append(data)
        print("* 录音结束")
        stream.stop_stream()
        stream.close()
        p.terminate()  # 释放portaudio资源

        WAVE_OUTPUT_FILENAME = self.gettime() + '.wav'
        self.output_path = self.spell_path() + '\\' + WAVE_OUTPUT_FILENAME
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

    # 读取文件
    def get_file_data(self, filepath):
        with open(filepath, 'rb')as f:
            return f.read()

    # 百度语音API
    def Baidu_speech_Api(self):
        client = speech.AipSpeech(setting.APP_ID, setting.client_id, setting.client_secret)
        result = client.asr((self.get_file_data(self.output_path)), 'wav', 8000, {"dev_pid": 1537})
        # print(result)
        result_list = list(result.values())
        if 'success.' in result_list:
            print('根据语音转文字，你说的是：\n%s' % result['result'][0])
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


if __name__ == '__main__':
    rec = REC()
    rec.speech()
    rec.Baidu_speech_Api()

'''
错误
{'err_msg': 'param dev_pid not support', 'err_no': 3300, 'sn': '739825927481582551956'}
成功
{'corpus_no': '6797009412074406095', 'err_msg': 'success.', 'err_no': 0, 'result': ['嗯嗯嗯嗯嗯。'], 'sn': '871915134601582552076'}
0
'''
'''
3300	用户输入错误	输入参数不正确	请仔细核对文档及参照demo，核对输入参数
3301	用户输入错误	音频质量过差	请上传清晰的音频
3302	用户输入错误	鉴权失败	token字段校验失败。请使用正确的API_KEY 和 SECRET_KEY生成。或QPS、调用量超出限额。或音频采样率不正确（可尝试更换为16k采样率）。
3303	服务端问题	语音服务器后端问题	请将api返回结果反馈至论坛或者QQ群
3304	用户请求超限	用户的请求QPS超限	请降低识别api请求频率 （qps以appId计算，移动端如果共用则累计）
3305	用户请求超限	用户的日pv（日请求量）超限	请“申请提高配额”，如果暂未通过，请降低日请求量
3307	服务端问题	语音服务器后端识别出错问题	目前请确保16000的采样率音频时长低于30s。如果仍有问题，请将api返回结果反馈至论坛或者QQ群
3308	用户输入错误	音频过长	音频时长不超过60s，请将音频时长截取为60s以下
3309	用户输入错误	音频数据问题	服务端无法将音频转为pcm格式，可能是长度问题，音频格式问题等。 请将输入的音频时长截取为60s以下，并核对下音频的编码，是否是16K， 16bits，单声道。
3310	用户输入错误	输入的音频文件过大	语音文件共有3种输入方式： json 里的speech 参数（base64后）； 直接post 二进制数据，及callback参数里url。 分别对应三种情况：json超过10M；直接post的语音文件超过10M；callback里回调url的音频文件超过10M
3311	用户输入错误	采样率rate参数不在选项里	目前rate参数仅提供16000，填写4000即会有此错误
3312	用户输入错误	音频格式format参数不在选项里	目前格式仅仅支持pcm，wav或amr，如填写mp3即会有此错误
'''

# PythonWhisperBatchTranscriptionTool

## 简述

这个脚本的功能是批量转写目标文件夹中的音频文件，使其变为.txt格式的文本文件。

目前支持 .mp3 和 .wav 以及 .flac 三种格式。.aac格式的转写存在问题，目前没排查出来是什么原因。

这个脚本使用了Whisper和ffmpeg。

关于具体的模型——转写前检测语言使用base，若为中文则使用medium，若为英文则使用small，若为其他语言则不转写。

由于有些时候Whisper转写完中文会输出繁体字，因此使用了opencc将输出语言转化为简体中文。

这个脚本几乎没有什么含金量。我上传它只是方便我的朋友们直接使用，而不用再写一遍。

## 使用方法

### 第一步——部署Whisper

[openai/whisper: Robust Speech Recognition via Large-Scale Weak Supervision (github.com)](https://github.com/openai/whisper)
根据其GITHUB主页的提示可以轻松地部署。

首先，python的pip是必须要安装的。

接下来，运行命令，拉取github内容到本地。
```
pip install git+https://github.com/openai/whisper.git 
```

然后，以`scoop`为例。
[Scoop](https://scoop.sh/)
打开Scoop官网，下载并安装。
运行命令安装ffmpeg。
```
# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

打开RUST主页，下载并安装RUST。
[Getting started - Rust Programming Language (rust-lang.org)](https://www.rust-lang.org/learn/get-started)
默认安装也是使用命令行。

再回到之前的窗口运行命令。
```
pip install setuptools-rust
```



### 第二步——部署第三方库

部署 `opencc-python-reimplemented`。这个库用于繁体中文和简体中文的转换。

```
pip install opencc-python-reimplemented
```



### 第三步——修改并运行本脚本

找到这两行代码，修改为需要的路径。

`audio_folder`是需要批量转写的文件夹路径。

`transcribed_files_log`是一个用于记录哪些音频文件被转写过了的日志文件。

```
audio_folder = "D:/Temp_Files/Whisper测试"
transcribed_files_log = "transcribed_files.log"
```




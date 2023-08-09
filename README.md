# XGPT
A macOS Client for free.xabcai.com made by Tkinter and Pyinstaller

一个用 Tkinter 绘制 UI 和 Pyinstaller 打包的 macOS ChatGPT 应用（采用 [free.xabcai.com](https://free.xabcai.com) 的API）


## 唠叨：

秉承`又不是不能用`、`只要有一个能跑就行`的原则，采用`ChatGPT 我考考你`、`面向Google、Stack Overflow编程`的方法，生成了这个应用。

本应用 99.9% 的代码由ChatGPT生成，我只是代码的搬运工和排列组合大师，所以不要和我说什么代码复用，代码封装还有其他什么我不懂的名词，我知道这个脚本的代码是屎山一座，So What。

目前实现的功能就是你问问题，ChatGPT回答，采用 model `gpt-3.5-turbo-16k`（暂不支持自定义）, 可以记住最新的10条问答记录（暂不支持自定义条数），显示每次发送的 message 的 token 数。

什么输出 markdown 格式结果渲染、Prompt、多会话窗口等等~~花里胡哨~~的功能暂不支持，等我有时间了让 ChatGPT 帮我写一下（抠鼻。


## 预览（底下左右两个按钮暂时没用，忘了说了，发送message的快捷键是 `command + enter`）：

<img src="/preview/light.png" alt="亮色模式" width="400" align="bottom" /><img src="/preview/dark.png" alt="暗色模式" width="400" align="bottom" />


https://github.com/AlickH/XGPT/assets/6060026/a9a3004b-daef-4621-a2fa-1677b9cd9cfc




## 对了，我打包的版本仅支持 `Apple Silicon` 处理器，如果你是 `Intel` 处理器的 Mac，打包命令如下：

1、安装 `Pyinstaller` 和各种依赖（打开脚本自己看，就前面几行）

    pip3 install pyinstaller
    pip3 install 各种依赖包
      
2、下载上面的 `XGPT.py`、`xabcai_gpt.py`、`GPT.icns` 放在同一文件夹下，`GPT.icns` 也可以换成你自己喜欢的图标

3、cd 到上面的文件夹里，然后运行以下命令：

    cd "PATH/TO/SHANG/MIAN/DE/WEN/JIAN/JIA
    pyinstaller --noconsole --icon=GPT.icns --name=X-GPT --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext XGPT.py

4、然后不出意外就可以在上面的文件夹的 `dist` 文件夹下找到打包好的 app 了，出意外了我也不知道咋处理，就 `要么放弃`、`要么自己折腾`、`为什么不问问神奇的 ChatGPT 呢`


## TODO（竟然能有这部分，ChatGPT 我来考考你）：
- Chat 存档
- 问答记忆条数选择
- model选择
- 标题改为当前 Chat 名称
- token超过时提示
- 更换源
- 提示词列表
- MD结果解析和语法高亮显示
- 历史记录选择与保存
- 新标签页Chat
- 删除记录中的单条
- 失败提示
- ...

## English README
Just, hey ChatGPT, help me to translate this in English.

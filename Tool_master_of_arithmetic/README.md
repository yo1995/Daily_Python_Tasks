## Description

『加减大师』、『加减王者』通用辅助解题~~外挂~~程序。能够延长所需答题时间或直接给出题目答案，从而使您闯关过程中一路平安。

## Versions

### 20180508

- added first version. works fine with mine.

## Usage

1. 安装 Python 3

2. 安装 mitmproxy
在终端中运行以下命令，或在您使用的IDE中安装此依赖库
'''
$ pip3 install mitmproxy
'''

3. 下载jjds-py3.py脚本，并切换至脚本所在目录

4. 在终端中运行以下命令
'''
$ mitmproxy -p 8129 -s ./jjds-py3.py
'''
# 端口号可自行设定，防止冲突且与后文保持一致。

5. 设置代理
在iPhone 下的「设置 - 无线局域网 - 你连接的 Wi-Fi 右侧的小i - 配置代理 - 手动」中设置服务器和端口。
如果在本地局域网内计算机运行：服务器为运行该脚本的计算机的内网 IP 地址（Windows 点击通知区域的网络图标 - 属性/Mac按住 Option 键选择 Wi-Fi 图标查询）
如果在具有独立地址或IP的服务器运行：地址为服务器地址
端口为 8129  # 或自行设定值

6. 在手机中打开 mitm.it  # mitmproxy库自带HTTP解析到本域名，

7. 下载证书、设置证书可信

这一步必须在步骤5已经配置完成的情况下进行，否则会看到*If you can see this, traffic is not passing through mitmproxy.*的提示语。

根据操作系统选择平台下载证书（iOS 选择 Apple 标识并确认安装描述文件即可），并在「设置 - 通用 - 关于本机 - 证书信任设置」中打开「mitmproxy」

8. 证书有效期为24小时，使用后别忘记关闭代理以免影响正常网络使用

## Keywords

加减大师 | 加减王者 | 微信小游戏 | 辅助 | 自动化

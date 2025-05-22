The principle is that the server plugin **MyPlugin** for the game will read player damage information and send it to **localhost:12345**.

Then, the program **server\_with\_local\_client.py** will read the player damage information, process it, and send it to **DGlab**.

The **pydglab\_ws** folder contains libraries and some pre-written functions provided officially.
**server\_with\_local\_client.py** is the main script.

**Note when running:**


url = client.get_qrcode("ws://<replace this with your computer’s IPv4 address>")
print("Please scan the QR code with the DG-Lab App to connect")
print_qrcode(url)  # Display the QR code



if message:
    # Check whether the message contains the player name "fclfcl"
    if "<replace this with your in-game character name>" in message:
        print("⚡ Player fclfcl is injured, sending waveform signal!")







原理是MyPlugin这个游戏的服务器插件 会读取玩家受伤信息并发送到localhost:12345这个端口上
然后server_with_local_client.py这个程序会读取玩家受伤信息 通过处理后会发送到DGlab上

pydglab_ws文件夹是官方提供的库和一些写好的函数
server_with_local_client.py是主函数 
运行时需注意
url = client.get_qrcode("ws://这里改成你的电脑IPv4地址")
        print("请用 DG-Lab App 扫描二维码以连接")
        print_qrcode(url)  # 显示二维码


if message:
            # 判断消息中是否包含玩家名 "fclfcl"
            if "这里改成你的游戏角色名" in message:
                print(f"⚡ 玩家 fclfcl 受伤，发送波形信号！")

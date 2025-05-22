import asyncio
import qrcode
import json
import io
from pydglab_ws import *

PULSE_DATA = {
    '呼吸': [
        ((10, 10, 10, 10), (0, 0, 0, 0)), ((10, 10, 10, 10), (0, 5, 10, 20)),
        ((10, 10, 10, 10), (20, 25, 30, 40)), ((10, 10, 10, 10), (40, 45, 50, 60)),
        ((10, 10, 10, 10), (60, 65, 70, 80)), ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((0, 0, 0, 0), (0, 0, 0, 0)), ((0, 0, 0, 0), (0, 0, 0, 0)), ((0, 0, 0, 0), (0, 0, 0, 0))
    ],
    
}

def print_qrcode(url: str):
    qr = qrcode.make(url)
    qr.show()

async def send_strength_command(client, strength_change):
    # 获取 clientId 和 targetId
    client_id = client.client_id
    target_id = client.target_id

    # 构建 JSON 格式的消息
    message = {
        "type": "msg",
        "clientId": client_id,
        "targetId": target_id,
        "message": f"strength-{strength_change}+{strength_change}+{strength_change}"
    }

    # 发送指令
    await client.send_msg(json.dumps(message))
    print(f"发送指令：{json.dumps(message)}")

async def send_strength_command(client, channel, strength_change):
    # 发送通道强度变化的命令到 App
    message = f"strength-{channel}+{strength_change}+{strength_change}"
    await client.send_msg(message)
    print(f"发送指令：{message}")

async def main():
    async with DGLabWSServer("0.0.0.0", 5678, 60) as server:
        client = server.new_local_client()

        url = client.get_qrcode("ws://192.168.2.102:5678")  # 本机IPv4地址
        print("请用 DG-Lab App 扫描二维码以连接")
        print(url)
        print_qrcode(url)

        # 等待绑定
        await client.bind()
        print(f"已与 App {client.target_id} 成功绑定")

        # 从 App 接收数据更新，并进行远控操作
        pulse_data_iterator = iter(PULSE_DATA.values())
        async for data in client.data_generator(FeedbackButton, RetCode):
            # 接收 App 反馈按钮
            if isinstance(data, FeedbackButton):
                print(f"App 触发了反馈按钮：{data.name}")

                if data == FeedbackButton.A1:
                    # 顺序发送波形
                    print("对方按下了 A 通道圆圈按钮，设置 A 通道强度")
                    # 设置 A 通道的强度
                    await client.set_strength(
                            Channel.A, 
                            StrengthOperationType.SET_TO,  # 强度设置
                            60  # 设置强度为 60
                            )
                    

            # 接收 心跳 / App 断开通知
            elif data == RetCode.CLIENT_DISCONNECTED:
                print("App 已断开连接，你可以尝试重新扫码进行连接绑定")
                await client.rebind()
                print("重新绑定成功")

        

if __name__ == "__main__":
    asyncio.run(main())
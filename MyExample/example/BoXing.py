"""
这段代码为波形发送的示例代码，用户按下 A 通道第一个按钮时，就会发送一段波形，每次按下都会发送不同的波形。

波形数据来源为 DG-Lab App，导出脚本参考本仓库目录下 ``scripts/pulse_data_db.py``。

另外，此处不仅提供 DG-Lab WebSocket 服务端服务，还生成了一个本地终端可供 App 连接。
"""
import asyncio
import io

import qrcode

from pydglab_ws import FeedbackButton, Channel, RetCode, DGLabWSServer, StrengthOperationType

def print_qrcode(url: str):
    qr = qrcode.make(url)
    qr.show()






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

        
        
        

        async for data in client.data_generator(FeedbackButton, RetCode):
            # 接收 App 反馈按钮
            if isinstance(data, FeedbackButton):
                print(f"App 触发了反馈按钮：{data.name}")

                if data == FeedbackButton.A1:
                    # 顺序发送波形
                    print("对方按下了 A 通道圆圈按钮，开始发送波形")
                    # 增加 A 通道强度
                    print("正在设置 A 通道强度")
                    await client.set_strength(Channel.A, StrengthOperationType.SET_TO, 60)

                    await client.add_pulses(Channel.A, *([
        ((25, 25, 24, 24), (100, 100, 100, 100)), ((24, 23, 23, 23), (100, 100, 100, 100)),
        ((22, 22, 22, 21), (100, 100, 100, 100)), ((21, 21, 20, 20), (100, 100, 100, 100)),
        ((20, 19, 19, 19), (100, 100, 100, 100)), ((18, 18, 18, 17), (100, 100, 100, 100)),
        ((17, 16, 16, 16), (100, 100, 100, 100)), ((15, 15, 15, 14), (100, 100, 100, 100)),
        ((14, 14, 13, 13), (100, 100, 100, 100)), ((13, 12, 12, 12), (100, 100, 100, 100)),
        ((11, 11, 11, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100)), ((10, 10, 10, 10), (100, 100, 100, 100)),
        ((10, 10, 10, 10), (100, 100, 100, 100))
    ]* 1))   # 复制 5 份，以维持一段时间

            # 接收 心跳 / App 断开通知
            elif data == RetCode.CLIENT_DISCONNECTED:
                print("App 已断开连接，你可以尝试重新扫码进行连接绑定")
                await client.rebind()
                print("重新绑定成功")


if __name__ == "__main__":
    asyncio.run(main())
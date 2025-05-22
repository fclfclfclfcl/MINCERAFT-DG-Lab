import asyncio
from websockets import ConnectionClosedOK
from pydglab_ws import DGLabWSConnect
import qrcode

def print_qrcode(url: str):
    """输出二维码到终端界面"""
    qr = qrcode.make(url)
    qr.show()

async def main():
    try:
        async with DGLabWSConnect("ws://192.168.1.161:5678") as client:
            # 获取二维码
            url = client.get_qrcode()
            print("请用 DG-Lab App 扫描二维码以连接")
            print_qrcode(url)

            # 等待绑定
            await client.bind()
            print(f"已与 App {client.target_id} 成功绑定")

            # 从 App 接收数据更新，并进行远控操作
            async for data in client.data_generator():
                print(f"收取到数据：{data}")
    except ConnectionClosedOK:
        print("Socket 服务端断开连接")

if __name__ == "__main__":
    asyncio.run(main())
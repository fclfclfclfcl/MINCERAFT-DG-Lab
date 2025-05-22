import asyncio
import socket
import qrcode
from pydglab_ws import *

def print_qrcode(url: str):
    qr = qrcode.make(url)
    qr.show()

async def start_listener(queue):
    """ 监听玩家受伤事件，并将事件加入队列 """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)  # 设置非阻塞模式
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)  # 设置监听队列长度

    print("监听线程已启动，等待玩家受伤事件...")  # **添加调试信息**
    loop = asyncio.get_running_loop()

    while True:
        try:
            client_socket, _ = await loop.sock_accept(server_socket)  # 异步的 accept
            print("连接已建立")  # **看看是否接收到连接**
            data = await loop.sock_recv(client_socket, 1024)  # 异步的 recv
            if data:
                message = data.decode('utf-8').strip()
                print(f"收到数据: {message}")  # **看看是否有数据传入**
                await queue.put(message)
            client_socket.close()
        except Exception as e:
            print(f"监听异常: {e}")
            await asyncio.sleep(0.1)  # 继续等待

async def handle_player_injury(queue, client):
    """ 处理玩家受伤事件，仅在玩家名为 fclfcl 时输出 """
    while True:
        # 从队列中获取玩家受伤事件
        message = await queue.get()
        if message:
            # 判断消息中是否包含玩家名 "fclfcl"
            if "fclfcl" in message:
                print(f"⚡ 玩家 fclfcl 受伤，发送波形信号！")
                await client.add_pulses(Channel.A, *(((25, 25, 24, 24), (100, 100, 100, 100)), ((24, 23, 23, 23), (100, 100, 100, 100))) * 1)

async def main():
    queue = asyncio.Queue()  # 创建异步队列

    async with DGLabWSServer("0.0.0.0", 5678, 60) as server:
        client = server.new_local_client()

        url = client.get_qrcode("ws://192.168.2.100:5678")
        print("请用 DG-Lab App 扫描二维码以连接")
        print_qrcode(url)  # 显示二维码

        # **等待 App 绑定成功**
        await client.bind()
        print(f"已成功绑定 App {client.target_id}")

        # **绑定成功后，才开始监听玩家受伤事件**
        asyncio.create_task(start_listener(queue))  # 启动监听任务
        asyncio.create_task(handle_player_injury(queue, client))  # 启动处理玩家受伤事件的任务

        while True:
            # 监听 App 事件
            data = await client.data_generator(FeedbackButton, RetCode).__anext__()

            # 处理 App 按钮反馈
            if isinstance(data, FeedbackButton):
                print(f"App 触发了反馈按钮：{data.name}")

                if data == FeedbackButton.A2:
                    print("对方按下了 A 通道三角按钮，开始增加强度")
                    await client.set_strength(Channel.A, StrengthOperationType.INCREASE, 10)
                elif data == FeedbackButton.A1:
                    print("对方按下了 A 通道圆圈按钮，发送波形")
                    await client.add_pulses(Channel.A, *(((25, 25, 24, 24), (100, 100, 100, 100)), ((24, 23, 23, 23), (100, 100, 100, 100))) * 5)
                elif data == FeedbackButton.A3:
                    print("对方按下了 A 通道方块按钮，开始降低强度")
                    await client.set_strength(Channel.A, StrengthOperationType.DECREASE, 10)

            # 处理 App 断开事件
            elif data == RetCode.CLIENT_DISCONNECTED:
                print("App 断开连接，尝试重新绑定...")
                print_qrcode(url)  # 显示二维码
                await client.rebind()
                print("重新绑定成功")

if __name__ == "__main__":
    asyncio.run(main())

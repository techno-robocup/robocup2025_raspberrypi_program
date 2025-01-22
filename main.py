import time
from i2cio.i2cio     import i2cio  # 正しいインポート形式で

if __name__ == "__main__":
    i2c_device = i2cio(0x08)  # I2Cアドレスを設定

    while True:
        message = input("Input message: ")

        try:
            # メッセージを送信
            i2c_device.writeData(message)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)

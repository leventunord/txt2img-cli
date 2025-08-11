import serial  # 导入串口模块
import time    # 导入时间模块

# 配置串口参数
ser = serial.Serial(
    port='/dev/tty.usbserial-2140',
    baudrate=9600,                   # 波特率
    bytesize=serial.EIGHTBITS,       # 数据位
    parity=serial.PARITY_NONE,       # 无奇偶校验
    stopbits=serial.STOPBITS_ONE,    # 停止位
    timeout=1                         # 超时时间（秒）
)

print("串口已打开:", ser.name)

# 发送一条数据
ser.write(b'1')  # 注意用字节类型发送

# 等待接收数据
while True:
    if ser.in_waiting:  # 如果有可读数据
        data = ser.readline()  # 读取一行（以换行符结尾）
        print("收到数据：", data.decode('utf-8').strip())

    time.sleep(0.1)  # 稍微延时，避免CPU占用太高

# 关闭串口（通常在程序退出时）
# ser.close()

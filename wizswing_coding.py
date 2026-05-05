import serial  # Sử dụng thư viện cổng serial
import time    # Sử dụng thư viện thời gian
import os      # Sử dụng thư viện hệ thống OS

# Thử nhập cổng và kết nối lặp lại
while True:  # Lặp vô hạn cho đến khi gặp lệnh break
    set0 = input(
        "Nhập cổng serial mà bộ điều khiển R4-A đang kết nối (ví dụ COM3): "
    )

    try:
        # Mở cổng serial với baudrate 9600
        ser = serial.Serial(
            port=set0,
            baudrate=9600,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=8
        )

        # Kiểm tra cổng đã mở thành công chưa
        if ser.is_open:
            print(f"\nCổng serial {set0} đã được mở thành công.\n")
        else:
            print(f"\nCổng {set0} không được mở. Vui lòng thử lại.\n")
            continue

        break  # Thoát vòng lặp khi thành công

    except Exception as e:
        print("\nKhông thể mở cổng serial. Vui lòng kiểm tra lại cổng.\n")
        time.sleep(2)

while True:
    os.system('cls')  # Xóa toàn bộ màn hình (Windows). Dùng 'clear' nếu là Linux/macOS

    print(' ')
    print('==========================================')
    print(' WIZWING Python Drone Coding Sample Code ')
    print('==========================================')
    print(' ')

    # Hiển thị cổng serial
    print('com port = ' + ser.name)

    # Tạo lệnh gửi xuống drone
    command10 = str.encode('battery?\r')  # Lệnh hỏi pin
    command20 = str.encode('height?\r')   # Lệnh hỏi độ cao

    # "\r" = Carriage Return (giống nhấn Enter)

    # Gửi lệnh kiểm tra pin
    ser.write(command10)
    if ser.readable():
        response = ser.readline()  # Đọc dữ liệu từ serial
        print(response[:len(response) - 1].decode())  # Hiển thị pin

    time.sleep(0.1)

    # Gửi lệnh kiểm tra độ cao
    ser.write(command20)
    if ser.readable():
        response = ser.readline()
        print(response[:len(response) - 1].decode())  # Hiển thị độ cao

    time.sleep(0.1)

    print('============================================================')
    print('Tham số được cài đặt mặc định: giá trị cần điều khiển (x:20~500) là 200, thời gian là 1000ms')
    print('============================================================')
    print(' ')
    command01 = input('Nhập lệnh [phím] rồi nhấn phím Enter ( [X] : Thoát chương trình ) : ')

    # Xử lý lệnh điều khiển
    if command01 == 'Q' or command01 == 'q':
        # Gửi lệnh start tới drone
        command01 = str.encode('start\r')
        ser.write(command01)
        time.sleep(0.1)

        command01b = str.encode('takeoff\r')
        ser.write(command01b)
        time.sleep(0.1)

        # Đọc phản hồi từ drone
        if ser.readable():
            response = ser.readline()
            print(response[:len(response) - 1].decode())  # "instruction good!"

        time.sleep(1)
    elif command01 == '77': # Bay vòng
        # Lệnh tiến về phía trước (Elevator)
        command02 = str.encode('forward 200 5000\r')  # tốc độ 200 trong 5 giây

        # Lệnh xoay ngược chiều kim đồng hồ (Rudder)
        command_turn = str.encode('ccw 200 5000\r')   # tốc độ 200 trong 5 giây

        # Gửi lệnh xoay trước
        ser.write(command_turn)
        time.sleep(0.025)

        # Sau đó gửi lệnh tiến
        ser.write(command02)
        time.sleep(0.1)  # đợi xác nhận gửi

        # Đọc phản hồi từ drone
        if ser.readable():
            response = ser.readline()
            print(response[:len(response) - 1].decode())

        # Đợi đủ thời gian thực hiện lệnh
        time.sleep(5)
    
    elif command01 == 'x' or command01 == 'X':
        # Thoát khỏi vòng lặp while
        commandLand = str.encode('land\r')
        ser.write(commandLand)
        break
    else:
        time.sleep(1)


    # ===== Kết thúc chương trình (tự động hạ cánh) =====
    print(' ')
    print('Kết thúc chương trình. (Tự động thực hiện lệnh land)')
    print(' ')

    command01 = str.encode('land\r')
    ser.write(command01)
    time.sleep(0.1)

    if ser.readable():
        response = ser.readline()
        print(response[:len(response) - 1].decode())

        time.sleep(3)
    # Bay vòng (xoay + tiến)
    

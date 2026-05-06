import serial  # Use the serial port library
import time    # Use the time library
import os      # Use the OS system library


def main():
    # Try to enter the port and connect repeatedly
    while True:  # Infinite loop until break
        set0 = input(
            "Enter the serial port that the R4-A controller is connected to (e.g. COM3): "
        )

        try:
            # Open the serial port with baudrate 9600
            ser = serial.Serial(
                port=set0,
                baudrate=9600,
                parity='N',
                stopbits=1,
                bytesize=8,
                timeout=8
            )

            # Check whether the port opened successfully
            if ser.is_open:
                print(f"\nSerial port {set0} opened successfully.\n")
            else:
                print(f"\nPort {set0} did not open. Please try again.\n")
                continue

            break  # Exit loop when successful

        except Exception as e:
            print("\nUnable to open serial port. Please check the port.\n")
            time.sleep(2)

    while True:
        os.system('cls')  # Clear the screen (Windows). Use 'clear' on Linux/macOS

        print(' ')
        print('==========================================')
        print(' WIZWING Python Drone Coding Sample Code ')
        print('==========================================')
        print(' ')

        # Display the serial port
        print('com port = ' + ser.name)

        # Create commands to send to the drone
        command10 = str.encode('battery?\r')  # Battery query command
        command20 = str.encode('height?\r')   # Height query command

        # "\r" = Carriage Return (same as pressing Enter)

        # Send battery check command
        ser.write(command10)
        if ser.readable():
            response = ser.readline()  # Read data from serial
            print(response[:len(response) - 1].decode())  # Display battery

        time.sleep(0.1)

        # Send height check command
        ser.write(command20)
        if ser.readable():
            response = ser.readline()
            print(response[:len(response) - 1].decode())  # Display height

        time.sleep(0.1)

        print('============================================================')
        print('Default parameters: control value (x:20~500) is 200, duration is 1000ms')
        print('============================================================')
        print(' ')
        command01 = input('Enter a command key and press Enter ( [X] : Exit program ) : ')

        # Handle control commands
        if command01 == 'Q' or command01 == 'q':
            # Send start command to the drone
            command01 = str.encode('start\r')
            ser.write(command01)
            time.sleep(0.1)

            command01b = str.encode('takeoff\r')
            ser.write(command01b)
            time.sleep(0.1)

            # Read response from the drone
            if ser.readable():
                response = ser.readline()
                print(response[:len(response) - 1].decode())  # "instruction good!"

            time.sleep(1)
        elif command01 == '77':  # Circle flight
            # Forward command (Elevator)
            command02 = str.encode('forward 200 5000\r')  # speed 200 for 5 seconds

            # Counterclockwise turn command (Rudder)
            command_turn = str.encode('ccw 200 5000\r')   # speed 200 for 5 seconds

            # Send turn command first
            ser.write(command_turn)
            time.sleep(0.025)

            # Then send forward command
            ser.write(command02)
            time.sleep(0.1)  # wait for send confirmation

            # Read response from the drone
            if ser.readable():
                response = ser.readline()
                print(response[:len(response) - 1].decode())

            # Wait enough time for the command to execute
            time.sleep(5)
        elif command01 == 'x' or command01 == 'X':   
            # ===== End of program (automatic landing) =====
            print(' ')
            print('Program ending. (Automatically sending land command)')
            print(' ')

            command01 = str.encode('land\r')
            ser.write(command01)
            time.sleep(0.1)
            break
        else:
            time.sleep(1)
            continue


if __name__ == '__main__':
    main()
    

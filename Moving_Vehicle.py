import serial
import time

# Define serial port and baud rate
serial_port = '/dev/ttyUSB0'  # Example serial port for Linux, change as needed
baud_rate = 9600

# Initialize serial communication
arduino = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        # Read sensor values
        arduino.write(b'r\n')  # Command to read sensor values
        response = arduino.readline().decode('utf-8').strip()
        left_sensor, right_sensor = map(int, response.split(','))
        
        # Simple line following logic
        if left_sensor < 500 and right_sensor < 500:
            # Both sensors see tape
            arduino.write(b'm150,150\n')  # Forward at moderate speed
        elif left_sensor < 500:
            # Only left sensor sees tape
            arduino.write(b'm100,150\n')  # Turn right slightly
        elif right_sensor < 500:
            # Only right sensor sees tape
            arduino.write(b'm150,100\n')  # Turn left slightly
        else:
            # No tape detected
            arduino.write(b'm0,0\n')  # Stop
        
        # Add a small delay
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    arduino.close()

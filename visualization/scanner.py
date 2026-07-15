import serial
import math
import matplotlib.pyplot as plt

PORT = "/dev/ttyACM0"
BAUD_RATE = 9600
MAX_DISTANCE = 200

arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)

print("Connected to Arduino.")
print("Starting environmental scanner...")

# Store one distance reading for each angle
scan_data = {}

plt.ion()

fig, ax = plt.subplots()

while True:
    try:
        line = arduino.readline().decode().strip()

        if not line:
            continue

        angle_text, distance_text = line.split(",")

        angle = int(angle_text)
        distance = float(distance_text)

        # Ignore invalid or excessively distant readings
        if distance <= 0 or distance > MAX_DISTANCE:
            continue

        # Replace the previous reading at this angle
        scan_data[angle] = distance

        x_points = []
        y_points = []

        # Convert all stored polar coordinates to Cartesian coordinates
        for stored_angle, stored_distance in sorted(scan_data.items()):

            radians = math.radians(stored_angle)

            x = stored_distance * math.cos(radians)
            y = stored_distance * math.sin(radians)

            x_points.append(x)
            y_points.append(y)

        # Clear previous frame
        ax.clear()

        # Draw current environmental scan
        ax.scatter(x_points, y_points)

        ax.set_xlim(-MAX_DISTANCE, MAX_DISTANCE)
        ax.set_ylim(0, MAX_DISTANCE)

        ax.set_xlabel("X Distance (cm)")
        ax.set_ylabel("Y Distance (cm)")
        ax.set_title("2D Ultrasonic Environmental Scanner")

        ax.grid(True)

        plt.pause(0.01)

    except ValueError:
        continue

    except KeyboardInterrupt:
        print("\nScanner stopped.")
        break

arduino.close()

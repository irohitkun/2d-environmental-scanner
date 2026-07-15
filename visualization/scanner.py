import serial
import math
import matplotlib.pyplot as plt

# Connect to Arduino
arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

print("Connected to Arduino.")
print("Waiting for scanner data...")

plt.ion()

fig, ax = plt.subplots()

while True:
    try:
        # Read one line from Arduino
        line = arduino.readline().decode().strip()

        if not line:
            continue

        # Arduino sends: angle,distance
        angle_text, distance_text = line.split(",")

        angle = float(angle_text)
        distance = float(distance_text)

        # Convert degrees to radians
        radians = math.radians(angle)

        # Convert polar coordinates to Cartesian coordinates
        x = distance * math.cos(radians)
        y = distance * math.sin(radians)

        print(
            f"Angle: {angle:.0f}° | "
            f"Distance: {distance:.1f} cm | "
            f"X: {x:.1f} | Y: {y:.1f}"
        )

        # Draw detected point
        ax.scatter(x, y)

        ax.set_xlim(-200, 200)
        ax.set_ylim(0, 200)

        ax.set_xlabel("X Distance (cm)")
        ax.set_ylabel("Y Distance (cm)")
        ax.set_title("2D Ultrasonic Environmental Scanner")

        plt.pause(0.01)

    except ValueError:
        # Ignore malformed serial data
        continue

    except KeyboardInterrupt:
        print("\nScanner stopped.")
        break

arduino.close()

import serial
import math
import matplotlib.pyplot as plt

PORT = "/dev/ttyACM0"
BAUD_RATE = 9600
MAX_DISTANCE = 200

# Object detection settings
DISTANCE_THRESHOLD = 15
MIN_OBJECT_POINTS = 3

arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)

print("Connected to Arduino.")
print("Starting environmental scanner...")

# Latest distance measured at each angle
scan_data = {}

plt.ion()

fig, ax = plt.subplots()


def detect_objects(scan_data):
    """
    Group consecutive scan points into possible objects.

    Two neighboring measurements are considered part of the same
    object if their distances differ by less than DISTANCE_THRESHOLD.
    """

    points = sorted(scan_data.items())

    objects = []
    current_object = []

    for angle, distance in points:

        if not current_object:
            current_object.append((angle, distance))
            continue

        previous_angle, previous_distance = current_object[-1]

        angle_gap = angle - previous_angle
        distance_gap = abs(distance - previous_distance)

        # Our Arduino normally scans in 2-degree steps.
        # Allow a slightly larger gap in case a reading was rejected.
        if angle_gap <= 4 and distance_gap <= DISTANCE_THRESHOLD:

            current_object.append((angle, distance))

        else:

            # Only keep clusters large enough to be meaningful
            if len(current_object) >= MIN_OBJECT_POINTS:
                objects.append(current_object)

            current_object = [(angle, distance)]

    # Don't forget the final cluster
    if len(current_object) >= MIN_OBJECT_POINTS:
        objects.append(current_object)

    return objects


while True:

    try:

        line = arduino.readline().decode().strip()

        if not line:
            continue

        angle_text, distance_text = line.split(",")

        angle = int(angle_text)
        distance = float(distance_text)

        # Ignore invalid readings
        if distance <= 0 or distance > MAX_DISTANCE:
            continue

        # Store newest reading for this angle
        scan_data[angle] = distance

        # Detect groups of points that may represent objects
        detected_objects = detect_objects(scan_data)

        # Clear previous frame
        ax.clear()

        # Draw every detected object
        for object_points in detected_objects:

            x_points = []
            y_points = []

            for stored_angle, stored_distance in object_points:

                radians = math.radians(stored_angle)

                x = stored_distance * math.cos(radians)
                y = stored_distance * math.sin(radians)

                x_points.append(x)
                y_points.append(y)

            ax.scatter(x_points, y_points)

        ax.set_xlim(-MAX_DISTANCE, MAX_DISTANCE)
        ax.set_ylim(0, MAX_DISTANCE)

        ax.set_xlabel("X Distance (cm)")
        ax.set_ylabel("Y Distance (cm)")
        ax.set_title(
            f"2D Ultrasonic Environmental Scanner | "
            f"Objects detected: {len(detected_objects)}"
        )

        ax.grid(True)

        plt.pause(0.01)

    except ValueError:
        # Ignore malformed serial data
        continue

    except KeyboardInterrupt:

        print("\nScanner stopped.")

        break


arduino.close()

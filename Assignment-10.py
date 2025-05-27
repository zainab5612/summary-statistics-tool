"""
Assignment 10: Print Summary Statistics
Submitted by Zainab Abdulhasan
Submitted: November 29, 2024

Assignment History:
- Assignment 9: Reading and using the contents of a file
- Assignment 8: Dataset Class
- Assignment 7: Filter List
- Assignment 6: Bubble Sort using Recursion
- Assignment 5: Reverse a List using Recursion
- Assignment 4: Creating a Sensor List and Filter List
- Assignment 3: Implementing a Menu
- Assignment 2: Converting Celsius to another temperature unit
- Assignment 1: Printing lines of text to the screen
"""

import math

# Global variable to store the current unit selection
current_unit = 0  # Default to Celsius

# Global constant dictionary for units
UNITS = {
    0: ("Celsius", "C"),
    1: ("Fahrenheit", "F"),
    2: ("Kelvin", "K")
}


class TempDataset:
    """
    A class to manage temperature data for the STEM Center.
    """

    _num_objects = 0  # Tracks the number of TempDataset objects created

    def __init__(self):
        self._data_set = None
        self._name = "Unnamed"
        TempDataset._num_objects += 1

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 3 <= len(value) <= 20:
            self._name = value
        else:
            raise ValueError("Name must be a string between 3 and 20 characters.")

    def process_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self._data_set = []
                for line in file:
                    parts = line.strip().split(",")
                    if parts[3] != "TEMP":
                        continue
                    day = int(parts[0])
                    time = math.floor(float(parts[1]) * 24)
                    sensor = int(parts[2])
                    temp = float(parts[4])
                    self._data_set.append((day, time, sensor, temp))
            return True
        except (FileNotFoundError, ValueError):
            return False

    def get_loaded_temps(self):
        return len(self._data_set) if self._data_set else None

    def get_avg_temperature_day_time(self, filter_list, day, time):
        if not self._data_set or not filter_list:
            return None
        temps = [convert_unit(temp[3], 0, current_unit) for temp in self._data_set
                 if temp[0] == day and temp[1] == time and temp[2] in filter_list]
        return sum(temps) / len(temps) if temps else None

    def get_summary_statistics(self, filter_list):
        if not self._data_set or not filter_list:
            return None
        # Apply conversion when building the temperature list
        temps = [convert_unit(temp[3], 0, current_unit) for temp in self._data_set if temp[2] in filter_list]
        return (min(temps), max(temps), sum(temps) / len(temps)) if temps else None


def convert_unit(temp, from_unit, to_unit):
    if from_unit == to_unit:
        return temp
    if from_unit == 0:
        if to_unit == 1:
            return (temp * 9 / 5) + 32
        elif to_unit == 2:
            return temp + 273.15
    elif from_unit == 1:
        if to_unit == 0:
            return (temp - 32) * 5 / 9
        elif to_unit == 2:
            return (temp - 32) * 5 / 9 + 273.15
    elif from_unit == 2:
        if to_unit == 0:
            return temp - 273.15
        elif to_unit == 1:
            return (temp - 273.15) * 9 / 5 + 32
    return temp


def print_filter(sensor_list, filter_list):
    """
    Prints the list of sensors with their active/inactive status.
    """
    for room_number, room_name, sensor_id in sensor_list:
        status = "[ACTIVE]" if sensor_id in filter_list else ""
        if room_number == "OUT":
            print(f"Out: {room_name} {status}")
        else:
            print(f"{room_number}: {room_name} {status}")


def change_filter(sensors, sensor_list, filter_list):
    """
    Allows the user to toggle sensors on and off in the filter.
    """
    while True:
        print_filter(sensor_list, filter_list)

        room_number = input("\nType the sensor number to toggle (e.g., 4201) or x to end: ").strip()

        if room_number.lower() == 'x':
            break

        normalized_room = "OUT" if room_number.lower() == "out" else room_number

        if normalized_room in sensors:
            sensor_id = sensors[normalized_room][1]
            if sensor_id in filter_list:
                filter_list.remove(sensor_id)  # Deactivate the sensor
            else:
                filter_list.append(sensor_id)  # Activate the sensor
        else:
            print("Invalid Sensor")


def choose_unit():
    """
    Allows the user to select the temperature unit.
    """
    global current_unit
    print(f"Current unit is {UNITS[current_unit][0]}")
    print("Choose new unit:")
    for key, (name, _) in UNITS.items():
        print(f"{key} - {name}")

    while True:
        try:
            choice = int(input("Which unit? "))
            if choice in UNITS:
                current_unit = choice
                break
            else:
                print("Please choose a valid unit from the list.")
        except ValueError:
            print("*** Please enter a number only ***")


def print_summary_statistics(dataset, filter_list):
    """
    Prints summary statistics for the dataset.
    """
    stats = dataset.get_summary_statistics(filter_list)
    if stats is None:
        print("Please load data file and make sure at least one sensor is active")
    else:
        min_temp, max_temp, avg_temp = stats
        print(f"Summary statistics for {dataset.name}")
        print(f"Minimum Temperature: {min_temp:.2f} {UNITS[current_unit][1]}")
        print(f"Maximum Temperature: {max_temp:.2f} {UNITS[current_unit][1]}")
        print(f"Average Temperature: {avg_temp:.2f} {UNITS[current_unit][1]}")


def print_menu():
    print("""
Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit
""")


def main():
    global current_unit

    sensors = {
        "4201": ("Foundations Lab", 1),
        "4204": ("CS Lab", 2),
        "4205": ("Tiled Room", 4),
        "4213": ("STEM Center", 0),
        "4218": ("Workshop Room", 3),
        "OUT": ("Outside", 5)
    }

    sensor_list = [(room_number, sensors[room_number][0], sensors[room_number][1]) for room_number in sensors]
    filter_list = [sensor[2] for sensor in sensor_list]  # All sensors active by default

    current_set = TempDataset()

    print("STEM Center Temperature Project")
    print("Zainab Abdulhasan")

    while True:
        print_menu()

        # Handle displaying `None` when no valid data is loaded
        if current_set.get_loaded_temps() is not None:
            avg_temp = current_set.get_avg_temperature_day_time(filter_list, 5, 7)
            print(avg_temp if avg_temp is not None else "None")  # Explicitly print `None` when no valid average exists
        else:
            print("None")  # Explicitly print `None` if no dataset is loaded

        try:
            choice = int(input("What is your choice? "))
            if choice == 1:
                filename = input("Please enter the filename of the new dataset: ")
                if current_set.process_file(filename):
                    print(f"Loaded {current_set.get_loaded_temps()} samples")
                    while True:
                        try:
                            dataset_name = input("Please provide a 3 to 20 character name for the dataset: ")
                            current_set.name = dataset_name
                            print(f"Dataset name set to: {current_set.name}")
                            break
                        except ValueError as e:
                            print(f"Error: {e}")
                else:
                    print("Unable to load the file. Please check the filename and try again.")
            elif choice == 2:
                choose_unit()
            elif choice == 3:
                change_filter(sensors, sensor_list, filter_list)
            elif choice == 4:
                print_summary_statistics(current_set, filter_list)
            elif choice == 7:
                print("Thank you for using the STEM Center Temperature Project")
                break
            else:
                print("Feature not implemented yet.")
        except ValueError:
            print("*** Please enter a number only ***")
        print()


if __name__ == "__main__":
    main()



"""

"C:\\Users\\zandu\\python projects\\Assignment-10.py\\.venv\\Scripts\\python.exe" "C:\\Users\\zandu\\python projects\\Assignment-10.py\\Assignment-10.py" 
STEM Center Temperature Project
Zainab Abdulhasan

Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 4
Please load data file and make sure at least one sensor is active


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 1
Please enter the filename of the new dataset: Temperatures2022-03-07.csv
Loaded 11724 samples
Please provide a 3 to 20 character name for the dataset: Test Week
Dataset name set to: Test Week


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

20.45544117647059
What is your choice? 4
Summary statistics for Test Week
Minimum Temperature: 16.55 C
Maximum Temperature: 28.42 C
Average Temperature: 21.47 C


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

20.45544117647059
What is your choice? 2
Current unit is Celsius
Choose new unit:
0 - Celsius
1 - Fahrenheit
2 - Kelvin
Which unit? 1


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

68.81979411764706
What is your choice? 4
Summary statistics for Test Week
Minimum Temperature: 61.79 F
Maximum Temperature: 83.16 F
Average Temperature: 70.64 F


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

68.81979411764706
What is your choice? 3
4201: Foundations Lab [ACTIVE]
4204: CS Lab [ACTIVE]
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor number to toggle (e.g., 4201) or x to end: 4201
4201: Foundations Lab 
4204: CS Lab [ACTIVE]
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor number to toggle (e.g., 4201) or x to end: 4204
4201: Foundations Lab 
4204: CS Lab 
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor number to toggle (e.g., 4201) or x to end: x


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

67.83914893617022
What is your choice? 4
Summary statistics for Test Week
Minimum Temperature: 61.79 F
Maximum Temperature: 83.16 F
Average Temperature: 70.13 F


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

67.83914893617022
What is your choice? 3
4201: Foundations Lab 
4204: CS Lab 
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor number to toggle (e.g., 4201) or x to end: 4205
4201: Foundations Lab 
4204: CS Lab 
4205: Tiled Room 
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor number to toggle (e.g., 4201) or x to end: 4213
4201: Foundations Lab 
4204: CS Lab 
4205: Tiled Room 
4213: STEM Center 
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor number to toggle (e.g., 4201) or x to end: 4218
4201: Foundations Lab 
4204: CS Lab 
4205: Tiled Room 
4213: STEM Center 
4218: Workshop Room 
Out: Outside [ACTIVE]

Type the sensor number to toggle (e.g., 4201) or x to end: out
4201: Foundations Lab 
4204: CS Lab 
4205: Tiled Room 
4213: STEM Center 
4218: Workshop Room 
Out: Outside 

Type the sensor number to toggle (e.g., 4201) or x to end: x


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 4
Please load data file and make sure at least one sensor is active


Main Menu
---------
1 - Process a new data file
2 - Choose unit
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 7
Thank you for using the STEM Center Temperature Project

"""





import psutil  # Import the psutil library to handle system-level operations.
import time  # Import the time module to manage time-related functionalities.

def read_existing_ports():
    """
    Reads existing ports from the 'ports.txt' file.

    Returns:
    set: A set containing existing ports.
    """
    try:
        with open("ports.txt", "r") as file:  # Open the 'ports.txt' file in read mode.
            existing_ports = {int(port.strip()) for port in file.readlines()}  # Read each line and create a set of ports.
        return existing_ports  # Return the set of existing ports.
    except FileNotFoundError:  # Handle if the file is not found.
        return set()  # Return an empty set.

def write_new_port(port):
    """
    Writes a new port to the 'ports.txt' file.

    Args:
    port (int): The new port to be added.
    """
    with open("ports.txt", "a") as file:  # Open the 'ports.txt' file in append mode.
        file.write(f"{port}\n")  # Write the new port to the file.

def get_latest_open_port():
    """
    Monitors network connections and identifies the latest open port(s) not present in the 'ports.txt' file.
    Stops after finding one new port and writes it to 'ports.txt'.
    """
    existing_ports = read_existing_ports()  # Retrieve existing ports from the file.
    latest_ports = set()  # Initialize an empty set to store the latest ports found.

    while len(latest_ports) < 1:  # Loop until one new port is found.
        current_ports = psutil.net_connections(kind='inet4')  # Get current network connections.

        # Filter current ports to those that are not in the existing or latest ports.
        new_ports = {conn.laddr.port for conn in current_ports if conn.status == 'LISTEN'} - existing_ports - latest_ports

        if new_ports:  # Check if new ports are found.
            for port in new_ports:  # Loop through the new ports.
                if len(latest_ports) < 1:  # Check if one new port is found.
                    latest_ports.add(port)  # Add the new port to the latest ports set.
                    write_new_port(port)  # Write the new port to the file.
                    print(f"{port}")  # Print the new port to the console.

        time.sleep(5)  # Wait for 5 seconds before checking for new ports again.

    #print(f"Stopped after finding 1 new port: {latest_ports}")

if __name__ == "__main__":
    get_latest_open_port()  # Call the main function when the script is executed.

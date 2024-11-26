from pymodbus.client import ModbusTcpClient
from my_IP_Addresses import SLAVE_IP, SLAVE_PORT
from datetime import datetime

# Configuration

UNIT_ID = 1  # Integriti Unit ID
SLAVE_ID = 1

# Initialize Modbus TCP Client
client = ModbusTcpClient(SLAVE_IP, port=SLAVE_PORT)

DOOR_LOCK_ADDR = 10001  # Modbus Input - Door Lock
DOOR_OPEN_ADDR = 10002  # Modbus Input - Door Open
DOOR_FORCED_ADDR = 10003  # Modbus Input - Door Forced
DOOR_DOTL_ADDR = 10004  # Modbus Input - Door DOTL
UNLOCK_DOOR_ADDR = 5  # Modbus Coil - Unlock Door
GRANT_ACCESS_ADDR = 6  # Modbus Coil - Grant Access to Door

DOOR2_LOCK_ADDR = 10101 # Modbus Input - Door Lock
DOOR2_OPEN_ADDR = 10102  # Modbus Input - Door Open
DOOR2_FORCED_ADDR = 10103  # Modbus Input - Door Forced
DOOR2_DOTL_ADDR = 10104  # Modbus Input - Door DOTL
UNLOCK_DOOR2_ADDR = 104    # Modbus Coil - Unlock Door
GRANT_ACCESS_DOOR2_ADDR = 105  # Modbus Coil - Grant Access to Door


def read_discrete_input(client, address):
    # Modbus Input registers are zero-based, subtract 1 from address?
    zero_based_address = address - 1
    response = client.read_discrete_inputs(zero_based_address, count=1)
    if response.isError():
        print(f"Error reading discrete input at address {address}: {response}")
        return None
        
    #print(f"Array of Bit: {response.bits}")
    return response.bits[0]  # First bit in the response

def read_all_statuses(client):
    print("Reading door statuses...")
    door_lock_status = read_discrete_input(client, DOOR_LOCK_ADDR)
    door_open_status = read_discrete_input(client, DOOR_OPEN_ADDR)
    door_forced_status = read_discrete_input(client, DOOR_FORCED_ADDR)

    print(f"Door Lock Status: {'Unlocked' if door_lock_status else 'Locked'}")
    print(f"Door Open Status: {'Open' if door_open_status else 'Closed'}")
    print(f"Door Forced Status: {'Forced Open' if door_forced_status else 'Normal'}")

def unlock_door(client):
    print("Trying to Unlock Door...")

    response = client.write_coil(UNLOCK_DOOR_ADDR, True)

    if response.isError():
        print(f"Error unlocking door: {response}")
    else:
        print("Door unlocked successfully.")

def lock_door(client):
    print("Trying to Lock Door...")

    response = client.write_coil(UNLOCK_DOOR_ADDR, False)

    if response.isError():
        print(f"Error locking door: {response}")
    else:
        print("Door locked successfully.")

def grant_access_to_door(client):
    response = client.write_coil(GRANT_ACCESS_ADDR, True)
    if response.isError():
        print(f"Error granting access to door: {response}")
    else:
        print("Access granted to the door.")


# Main script execution
if __name__ == "__main__":
    print(f"Testing Modbus Connection - {datetime.now().strftime('%H:%M:%S.%f')}"[:-4] + "\n")
    if client.connect():
        print("Connected to Modbus server.\n")

        # Read statuses
        read_all_statuses(client)

        # Example actions (optional)
        #unlock_door(client)
        lock_door(client)
        # grant_access_to_door(client)

        client.close()
        print(f"\nEnding Modbus Connection - {datetime.now().strftime('%H:%M:%S.%f')}"[:-4]
        )
    else:
        print("Failed to connect to Modbus server.")
# controller.py

from model import IPUtils, Network, Subnet


class NetworkController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # self.network = None
        self.first_subnets = None
        self.last_subnets = None

    def run(self):
        self.get_network_info()


    # @staticmethod
    def validate_ip(self):  # , ip_address):
        is_valid = False
        ip_address = None  # Initialize ip_address here
        while not is_valid:
            try:
                ip_address = self.view.prompt_for_ip_input().strip()
                octets = ip_address.split('.')
                if len(octets) != 4:
                    raise ValueError(
                        f"Invalid number of octets: {len(octets)}. Expected 4 octets in IP address {ip_address}.")

                for octet in octets:
                    if not octet.isdigit() or not (0 <= int(octet) <= 255):
                        raise ValueError(
                            f"Invalid octet value or type: {octet}. Each octet should be between 0 and 255.")
                is_valid = True
            except ValueError as e:
                print(e)
        return str(ip_address)  # Return the valid IP address

    def validate_cidr(self, valid_ip: str) -> int:
        is_valid = False
        cidr = None
        # while not is_valid:
        while not is_valid:

            try:
                cidr_input = self.view.prompt_for_cidr_input()  # This should call a method to get CIDR

                # Strip the leading slash and validate CIDR
                cidr_input = cidr_input.strip().lstrip('/')  # Remove leading spaces and the slash
                if cidr_input == "":
                    cidr = IPUtils.cidr_based_on_class(valid_ip)
                    is_valid = True
                    print(f"CIDR was inferred: /{cidr}")

                elif not cidr_input.isdigit() or not (0 <= int(cidr_input) <= 32):
                    raise ValueError("Invalid CIDR input. Please enter a number between 0 and 32.")
                else:
                    # Convert CIDR to int for further processing
                    cidr = int(cidr_input)
                    is_valid = True
            except (ValueError, IndexError) as e:
                print(f"Invalid CIDR: {e}. Please try again.")
        return int(cidr)

    def validate_partition(self):
        is_valid = False
        partition_type_input = ""
        partition_size_input = 0

        while not is_valid:
            partition_type_input = self.view.prompt_for_partition_type_input().strip().lower()

            if partition_type_input in ['s', 'subnets', 'h', 'hosts']:
                partition_size_input = self.view.prompt_for_partition_input('subnets' if partition_type_input in ['s', 'subnets'] else "hosts").strip()
                if not partition_size_input.isdigit():
                    raise ValueError("Invalid partition size. Please enter a numeric value.")
                # else:
                #     is_valid = True
                #     partition_size_input = int(partition_size_input)
                #

            else:
                print("Skip partitioning..")

                # raise ValueError("Invalid partition type. Please enter 'S' for subnets or 'H' for hosts.")

            is_valid = True

        return partition_type_input, int(partition_size_input)

    # def subnets_list(self, subnet: Subnet) -> list:
    #     """Get the list of subnets in dotted-decimal format."""
    #     subnets = []
    #     host_size = 2 ** (32 - self.cidr)
    #     start_ip = IPUtils.bin_to_ip(self.network_address_bin)
    #     subnets = [Subnet(self.cidr, start_ip + i * host_size, 1, host_size).subnet_valid_host_range for i in
    #                range(self.total_subnets)]  # should be all the network addresses of all subnets
    #     return subnets

    def get_network_info(self):

        state = "INPUT"
        while state != "STOP":
            try:
                # Get IP address and CIDR from user input
                ip_address = self.validate_ip()
                print(f"Valid ip: {ip_address}")
                # ip_address_input = self.view.prompt_for_ip_input()

                # cidr_input = self.view.prompt_for_cidr_input()
                # cidr = IPUtils.validate_cidr(ip_address, cidr_input)
                cidr = self.validate_cidr(ip_address)
                print(f"Valid cidr: {cidr}")

                # # Get and validate the partition type
                # partition_type_input = self.view.prompt_for_partition_type_input().strip().lower()
                #
                # if partition_type_input not in ['s', 'hosts', 'h', 'subnets']:
                #     raise ValueError("Invalid partition type. Would you like to calculate by [S]ubnets or [H]osts?.")
                #
                # # Get the partition input based on the selected type (hosts or subnets)
                # partition_input = int(self.view.prompt_for_partition_input('hosts' if partition_type_input == 'h'
                #                                                            else 'subnets'))

                partition_type_input, partition_size_input = self.validate_partition()

                subnets_size, hosts_size = 0, 0
                if partition_type_input in ['hosts', 'h']:
                    hosts_size = int(partition_size_input)
                    # network = self.model(cidr, ip_address, subnets_size=0, hosts_size=hosts_size)

                elif partition_type_input in ['subnets', 's']:
                    subnets_size = int(partition_size_input)
                # else:
                #     print("Skip partitioning..")

                # Pass the validated inputs to the model
                network = self.model(cidr, ip_address, subnets_size=subnets_size, hosts_size=hosts_size)
                # Display network information
                self.view.display_network_info(network)

                # self.subnets = network.subnets_list
                self.first_subnets = network.subnets_list_first_two
                self.view.display_first_subnets_info(first_subnets=self.first_subnets)
                self.last_subnets = network.subnets_list_last_two
                self.view.display_last_subnets_info(last_subnets=self.last_subnets)
                # network = self.model(ip_address, cidr, partition_type_input, partition_size_input)
                # self.view.display_subnets_info(network, self.subnets)

                # self.view.display_subnets_info(self.first_subnets, self.last_subnets)

                state = "STOP"  # End the loop after successful processing -> network created

            except ValueError as e:
                print(f"Error: {e}. Please try again.")
                # Keep the user in the loop until valid input is provided


# from ip_utils import IPUtils
#
# class Controller:
#     def __init__(self):
#         self.network = None
#         self.subnets = []
#
#     def create_network(self, cidr: int, base_ip: str):
#         """Create a new network."""
#         self.network = Network(cidr, base_ip)
#
#     def create_subnet(self, subnet_index: int, subnet_bits: int = 2):
#         """Create a new subnet based on the existing network."""
#         if self.network is None:
#             raise ValueError("Network not created yet.")
#         subnet = Subnet(self.network.cidr + subnet_bits, self.network.network_address, subnet_index, subnet_bits)
#         self.subnets.append(subnet)
#
#     def validate_host(self, ip: str) -> bool:
#         """Validate if a host IP is within the valid range of the network."""
#         if self.network is None:
#             raise ValueError("Network not created yet.")
#         host = Host(ip)
#         return host.is_valid_host(self.network)
#
#     def get_network_info(self):
#         """Retrieve network information."""
#         if self.network is None:
#             raise ValueError("Network not created yet.")
#         return {
#             'network_address': self.network.network_address,
#             'broadcast_address': self.network.broadcast_address,
#             'valid_host_range': self.network.valid_host_range,
#         }
#
#     def get_subnet_info(self):
#         """Retrieve information about subnets."""
#         return [{'subnet_address': subnet.subnet_address,
#                  'broadcast_address': subnet.subnet_broadcast_address,
#                  'valid_host_range': subnet.subnet_valid_host_range}
#                 for subnet in self.subnets]
#


# class SubnetController:
#     def __init__(self, base_ip: str, cidr: int):
#         """Initialize the controller with a base IP and CIDR."""
#         if not IPUtils.validate_ip(base_ip):
#             raise ValueError("Invalid IP address")
#         if not (0 <= cidr <= 32):
#             raise ValueError("Invalid CIDR value")
#
#         self.base_ip = base_ip
#         self.cidr = cidr
#         self.network = Network(cidr, base_ip)
#
#     def calculate_subnets(self, num_hosts: int = None, num_subnets: int = None):
#         """Calculate the new CIDR based on hosts or subnets."""
#         if num_hosts:
#             required_bits = (num_hosts + 2 - 1).bit_length()
#             new_cidr = 32 - required_bits
#         elif num_subnets:
#             subnet_bits = (num_subnets - 1).bit_length()
#             new_cidr = self.cidr + subnet_bits
#         else:
#             raise ValueError("Either hosts or subnets must be provided.")
#
#         print(f"New calculated CIDR: {new_cidr}")
#         return new_cidr
#
#     def get_network_details(self):
#         """Return network details like subnet mask, CIDR, and total hosts."""
#         return {
#             'subnet_mask': self.network.subnet_mask,
#             'cidr': f"/{self.cidr}",
#             'total_hosts': self.network.total_hosts,
#             'network_address': self.network.network_address,
#             'broadcast_address': self.network.broadcast_address
#         }

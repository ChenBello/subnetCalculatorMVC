# controller.py

from model import IPUtils


class NetworkController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.subnets = None

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
        # without output, calculation based on Class only
        cidr = IPUtils.cidr_based_on_class(valid_ip)
        print(f"CIDR was automatically set based on IP class: /{cidr}")
        return cidr

    # def validate_cidr(self, valid_ip: str) -> int:
    #     is_valid = False
    #     cidr = None
    #     while not is_valid:
    #
    #         try:
    #             cidr_input = self.view.prompt_for_cidr_input()  # This should call a method to get CIDR
    #
    #             # Strip the leading slash and validate CIDR
    #             cidr_input = cidr_input.strip().lstrip('/')  # Remove leading spaces and the slash
    #             if cidr_input == "":
    #                 cidr = IPUtils.cidr_based_on_class(valid_ip)
    #                 is_valid = True
    #                 print(f"CIDR was inferred: /{cidr}")
    #
    #             elif not cidr_input.isdigit() or not (0 <= int(cidr_input) <= 32):
    #                 raise ValueError("Invalid CIDR input. Please enter a number between 0 and 32.")
    #             else:
    #                 # Convert CIDR to int for further processing
    #                 cidr = int(cidr_input)
    #                 is_valid = True
    #         except (ValueError, IndexError) as e:
    #             print(f"Invalid CIDR: {e}. Please try again.")
    #     return int(cidr)

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
                self.subnets = network.subnets_list

                # Display network information
                self.view.display_network_info(network)
                self.view.display_subnets_info(network, self.subnets)

                state = "STOP"  # End the loop after successful processing -> network created

            except ValueError as e:
                print(f"Error: {e}. Please try again.")
                # Keep the user in the loop until valid input is provided



# view.py
class NetworkView:
    def display_network_info(self, network):#, subnet):
        print(f"1. Subnet Mask: {network.subnet_mask}")
        print(f"2. Subnet in CIDR: /{network.cidr}")
        print(f"3. Number of subnets: {network.total_subnets}")
        print(f"4. Number of valid hosts: {network.total_valid_hosts}")
        print(f"5. Network Address: {network.network_address}")
        print(f"6. Broadcast Address: {network.broadcast_address}")

    def display_subnets_info(self, network, subnets):
        print(f"\n 7. For (maximum) two first and two last subnets:")
        if network.total_subnets < 1:
            print("\tNot subnets to display.")
        else:
            for i, subnet in enumerate(subnets, start=1):
                try:
                    print(f"\nSubnet {i}:")
                    print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
                    print(
                        f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}" if
                            subnet.subnet_valid_host_size > 3 else "")
                except Exception as e:
                    print(f"\nError processing Subnet {i}: {e}")
    # def get_subnet_info(self):
    #     """Retrieve information about subnets."""
    #     #         return [{'subnet_address': subnet.subnet_address,
    #     #                  'broadcast_address': subnet.subnet_broadcast_address,
    #     #                  'valid_host_range': subnet.subnet_valid_host_range}
    #     #                 for subnet in self.subnets]
    #     print(f"\n 5. For (maximum) two first and two last subnets:")
    #     for i, subnet in enumerate(NetworkController.network.subnets_list, start=1):
    #         try:
    #             print(f"\nSubnet {i}:")
    #             print(f"  Network Range: {subnet.subnet_} - {subnet.subnet_broadcast_address}")
    #             print(f"  Usable Host Range: {subnet.subnet_valid_host_range[0]} - {subnet.subnet_valid_host_range[1]}" if len(subnet) > 3 else "")
    #         except Exception as e:
    #             print(f"\nError processing Subnet {i}: {e}")
    #

    def prompt_for_ip_input(self):
        return input("Enter IP address (e.g., 192.168.1.1): ").strip()

    def prompt_for_cidr_input(self):
        return input("Enter CIDR (e.g., /24): ").strip()

    def prompt_for_partition_type_input(self):
        return input("Would you like to calculate by [S]ubnets or [H]osts? (Enter other key to skip that part): ").strip().lower()

    def prompt_for_partition_input(self, partition_type):
        return input(f"Enter number of {partition_type}: ").strip()


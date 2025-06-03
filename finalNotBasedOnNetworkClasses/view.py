# view.py
class NetworkView:
    def display_network_info(self, network):#, subnet):
        print(f"1. Subnet Mask: {network.subnet_mask}")
        print(f"2. Subnet in CIDR: /{network.cidr}")
        print(f"3. Number of subnets: {network.total_subnets}")
        print(f"4. Number of valid hosts: {network.total_valid_hosts}")
        print(f"5. Network Address: {network.network_address}")
        print(f"6. Broadcast Address: {network.broadcast_address}")

    def display_first_subnets_info(self, first_subnets):
        print(f"\n 7. For (maximum) two first and two last subnets:")
        if not first_subnets:  # Check if the list is empty
            print("\tNo subnets to display.")
        elif len(first_subnets) == 1:
            print("\t(Not enough subnets to display two from each side.)")
            subnet = first_subnets[0]  # Access the only subnet in the list
            print(f"\nSubnet 1:")
            print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
            print(f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}")
        else:
            print("\nTwo first subnets:")
            for i, subnet in enumerate(first_subnets[:2], start=1):  # Display at most two subnets
                try:
                    print(f"\nSubnet {i}:")
                    print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
                    print(f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}"
                          if subnet.subnet_valid_host_size > 3 else "")
                except Exception as e:
                    print(f"\nError processing Subnet {i}: {e}")

    def display_last_subnets_info(self, last_subnets):
        if not last_subnets:  # Check if the list is empty
            print("\tNo last subnets to display.")
        else:
            print("\nTwo last subnets:")
            for i, subnet in enumerate(last_subnets[-2:], start=1):  # Display at most two subnets
                try:
                    print(f"\nSubnet {i}:")
                    print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
                    print(f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}"
                          if subnet.subnet_valid_host_size > 3 else "")
                except Exception as e:
                    print(f"\nError processing Subnet {i}: {e}")

    def prompt_for_ip_input(self):
        return input("Enter IP address (e.g., 192.168.1.1): ").strip()

    def prompt_for_cidr_input(self):
        return input("Enter CIDR (leave blank to infer) (e.g., /24 or 24): ").strip()

    def prompt_for_partition_type_input(self):
        return input(
            "Would you like to calculate by [S]ubnets or [H]osts? (Enter other key to skip that part): ").strip().lower()

    def prompt_for_partition_input(self, partition_type):
        return input(f"Enter number of {partition_type}: ").strip()

# need to check if works
# def display_subnets_info(self, subnets):
#     print(f"\n7. For (maximum) two first and two last subnets:")
#
#     if not subnets:
#         print("\tNo subnets to display.")
#         return
#
#     total = len(subnets)
#
#     if total == 1:
#         subnet = subnets[0]
#         print("\t(Only one subnet available)")
#         print(f"\nSubnet 1:")
#         print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
#         if subnet.subnet_valid_host_size > 3:
#             print(f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}")
#         return
#
#     # Show first two
#     print("\nTwo first subnets:")
#     for i, subnet in enumerate(subnets[:2], start=1):
#         print(f"\nSubnet {i}:")
#         print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
#         if subnet.subnet_valid_host_size > 3:
#             print(f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}")
#
#     # Show last two, only if there are more than 2 and they aren't duplicates of the first ones
#     if total > 2:
#         print("\nTwo last subnets:")
#         for i, subnet in enumerate(subnets[-2:], start=total - 1):
#             print(f"\nSubnet {i + 1}:")
#             print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
#             if subnet.subnet_valid_host_size > 3:
#                 print(f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}")

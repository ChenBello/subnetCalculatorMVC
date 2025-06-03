class NetworkView:
    def display_network_info(self, network):
        print(f"1. Subnet Mask: {network.subnet_mask}")
        print(f"2. Subnet in CIDR: /{network.cidr}")
        print(f"3. Number of subnets: {network.total_subnets}")
        print(f"4. Number of valid hosts: {network.total_valid_hosts}")
        print(f"5. Network Address: {network.network_address}")
        print(f"6. Broadcast Address: {network.broadcast_address}")

    def display_subnets_info(self, network, subnets):
        print("\n7. Displaying up to two first and two last subnets:")
        if network.total_subnets < 1:
            print("\tNo subnets to display.")
            return

        # Select the first two and last two subnets, or all if less than 5 subnets
        to_display = subnets[:2] + subnets[-2:] if network.total_subnets > 4 else subnets

        for i, subnet in enumerate(to_display, start=1):
            try:
                print(f"\nSubnet {i}:")
                print(f"  Network Range: {subnet.subnet_address} - {subnet.subnet_broadcast_address}")
                if subnet.subnet_valid_host_size > 3:
                    print(f"  Usable Host Range: {subnet.subnet_first_valid_host} - {subnet.subnet_last_valid_host}")
            except Exception as e:
                print(f"\nError processing Subnet {i}: {e}")

    def prompt_for_ip_input(self):
        return input("Enter IP address (e.g., 192.168.1.1): ").strip()

    # Uncomment if you want to enable CIDR input prompt in the future
    # def prompt_for_cidr_input(self):
    #     return input("Enter CIDR (e.g., /24), leave blank for default Class: ").strip()

    def prompt_for_partition_type_input(self):
        return input("Would you like to calculate by [S]ubnets or [H]osts? (Enter other key to skip that part): ").strip().lower()

    def prompt_for_partition_input(self, partition_type):
        return input(f"Enter number of {partition_type}: ").strip()

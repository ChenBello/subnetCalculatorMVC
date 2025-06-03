# from ip_utils import IPUtils

class IPUtils:
    @staticmethod
    def ip_to_bin(ip: str) -> str:
        """Convert an IP address from dotted-decimal format to binary."""
        octets = ip.split('.')
        bin_ip = ''.join([format(int(octet), '08b') for octet in octets])
        return bin_ip

    @staticmethod
    def bin_to_ip(bin_ip: str) -> str:
        """Convert a binary string back to an IP address in dotted-decimal format."""
        octets = [str(int(bin_ip[i:i + 8], 2)) for i in range(0, 32, 8)]
        return '.'.join(octets)

    @staticmethod
    def cidr_based_on_class(ip_address: str) -> int:
        cidr = 0
        first_octet = int(ip_address.split('.')[0])
        if 1 <= first_octet <= 126:
            cidr = 8
        elif 128 <= first_octet <= 191:
            cidr = 16
        elif 192 <= first_octet <= 223:
            cidr = 24
        return cidr

    @staticmethod
    def is_valid_ip(ip_address):
        is_valid = False

        try:
            if ip_address == "":
                is_valid = True
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
        return is_valid  # Return the valid IP address

class Network:
    def __init__(self, cidr: int, base_ip: str, subnets_size: int = 0, hosts_size: int = 0):
        """Initialize a network with CIDR and base IP address."""
        if not IPUtils.is_valid_ip(base_ip):
            raise ValueError(f"Invalid IP address: {base_ip}")

        self.base_ip = base_ip
        self.original_cidr = cidr

        # Determine host and subnet bits based on sizes provided
        if subnets_size > 0 and hosts_size > 0:
            self.host_bits = max(1, (hosts_size + 2 - 1).bit_length())  # +2 for network and broadcast addresses
            self.subnet_bits = max(0, 32 - (self.host_bits + cidr))
        elif subnets_size > 0:
            self.subnet_bits = max((subnets_size - 1).bit_length(), 0)
            self.host_bits = 32 - (cidr + self.subnet_bits)
        elif hosts_size > 0:
            self.host_bits = max(1, (hosts_size + 2 - 1).bit_length())
            self.subnet_bits = max(0, 32 - (cidr + self.host_bits))
        else:
            self.host_bits = max(0, 32 - cidr)  # No subnets or hosts specified
            self.subnet_bits = max(0, cidr - IPUtils.cidr_based_on_class(base_ip))

        # Adjust CIDR if necessary
        self.cidr = min(32, cidr + self.subnet_bits)

        # Ensure CIDR is valid
        if not (0 <= self.cidr <= 32):
            raise ValueError(f"Invalid CIDR: {self.cidr}")

        if self.cidr > self.original_cidr:
            print(f"Note: CIDR has been adjusted from {self.original_cidr} to {self.cidr} due to subnet size requirements.")

        # Binary representations for network and broadcast addresses
        self.network_address_bin = IPUtils.ip_to_bin(base_ip)[:self.cidr] + '0' * (32 - self.cidr)
        self.broadcast_address_bin = IPUtils.ip_to_bin(base_ip)[:self.cidr] + '1' * (32 - self.cidr)

        # # Convert back to IP format for easier access
        # self.network_address = IPUtils.bin_to_ip(self.network_address_bin)
        # self.broadcast_address = IPUtils.bin_to_ip(self.broadcast_address_bin)
    @property
    def total_subnets(self):
        """Calculate the total number of subnets based on CIDR."""
        return 2 ** self.subnet_bits if self.subnet_bits > 0 else 1

    @property
    def subnets_list(self):
        """Generate a list of subnets within this network."""
        network_prefix = self.network_address_bin[:self.cidr-self.subnet_bits]

        return [
            Subnet(
                IPUtils.bin_to_ip(network_prefix + format(i, f'0{self.subnet_bits}b') + '0' * self.host_bits),
                IPUtils.bin_to_ip(network_prefix + format(i, f'0{self.subnet_bits}b') + '1' * self.host_bits)
            )
            for i in range(self.total_subnets)
        ]

    @property
    def subnets_list_first_two(self):
        """Generate a list of the first two subnets within this network."""
        network_prefix = self.network_address_bin[:self.cidr - self.subnet_bits]
        return [
            self._create_subnet(network_prefix, i)
            for i in range(min(2, self.total_subnets))
        ]

    @property
    def subnets_list_last_two(self):
        """Generate a list of the last two subnets within this network."""
        if self.total_subnets < 2:
            raise ValueError("Not enough subnets to display the last 2.")

        network_prefix = self.network_address_bin[:self.cidr - self.subnet_bits]
        return [
            self._create_subnet(network_prefix, i)
            for i in range(self.total_subnets - 2, self.total_subnets)
        ]

    def _create_subnet(self, network_prefix, i):
        """Helper method to create a Subnet object."""
        subnet_part = format(i, f'0{self.subnet_bits}b')
        return Subnet(
            IPUtils.bin_to_ip(network_prefix + subnet_part + '0' * self.host_bits),
            IPUtils.bin_to_ip(network_prefix + subnet_part + '1' * self.host_bits)
        )

    @property
    def network_address(self):
        """Get the network address in dotted-decimal format."""
        return IPUtils.bin_to_ip(self.network_address_bin)

    @property
    def broadcast_address(self):
        """Get the broadcast address in dotted-decimal format."""
        return IPUtils.bin_to_ip(self.broadcast_address_bin)

    @property
    def subnet_mask(self):
        """Calculate and return the subnet mask in dotted-decimal format."""
        mask_bin = '1' * self.cidr + '0' * (32 - self.cidr)
        return IPUtils.bin_to_ip(mask_bin)

    @property
    def total_valid_hosts(self):
        """Calculate the total number of valid hosts in the network."""
        return 2 ** (32 - self.cidr) - 2

    def __str__(self):
        return (f"Network: {self.network_address}/{self.cidr}, "
                f"Broadcast: {self.broadcast_address}, "
                f"Host Bits: {self.host_bits}, "
                f"Subnet Bits: {self.subnet_bits}")
    # @property
    # def total_subnets(self):
    #     """Calculate the total number of subnets based on CIDR."""
    #     return 2 ** self.subnet_bits



class Subnet:
    def __init__(self, subnet_address: str, broadcast_address: str):
        self.subnet_address = subnet_address
        self.subnet_broadcast_address = broadcast_address
        self.first_host_bin = IPUtils.ip_to_bin(self.subnet_address)[:-1] + '1'
        self.last_host_bin = IPUtils.ip_to_bin(self.subnet_broadcast_address)[:-1] + '0'

    @property
    def subnet_first_valid_host(self):
        """Calculate the first valid host in the subnet."""
        # first_host_bin = IPUtils.ip_to_bin(self.subnet_address)[:-1] + '1'
        return IPUtils.bin_to_ip(self.first_host_bin)

    @property
    def subnet_last_valid_host(self):
        """Calculate the last valid host in the subnet."""
        # last_host_bin = IPUtils.ip_to_bin(self.subnet_broadcast_address)[:-1] + '0'
        return IPUtils.bin_to_ip(self.last_host_bin)

    @property
    def subnet_valid_host_size(self):
        """Calculate the valid host range in the subnet."""
        # Subtract the first from the last and add 1 to get the total number of hosts.
        # The subtraction last - first gives us the number of addresses between the first and last host.
        # Adding 1 includes both the first and last addresses in the count.
        return int(self.last_host_bin, 2) - int(self.first_host_bin, 2) + 1

    def __str__(self):
        return (f"Network: {self.subnet_address}, "
                f"Broadcast: {self.subnet_broadcast_address}, "
                f"Valid hosts range: {self.subnet_first_valid_host} - {self.subnet_last_valid_host}, "
                f"Valid hosts size: {self.subnet_valid_host_size}")

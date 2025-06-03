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
    def validate_ip(ip: str) -> bool:
        """Validate the format of the IP address."""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not (0 <= int(part) <= 255):
                return False
        return True

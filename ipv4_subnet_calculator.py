''' 
SUBNET MASK CALCULATOR v0.0.1
'''

import re
import sys


class InvalidIPAddress(Exception):
    pass

class InvalidSubnetMaskNumber(Exception):
    pass

class InvalidIPV4CIDRNotation(Exception):
    pass


class IPAddress():

    def __init__(self, ip_address: str, subnet_mask_number: int):
        self.ip_address = ip_address
        self.subnet_mask_number = subnet_mask_number
        self.subnet_mask = [0] * 32

        for i in range(self.subnet_mask_number):
            self.subnet_mask[i] = 1
        
        self.ip_address_decimal_octets = [int(decimal_octet) for decimal_octet in ip_address.split('.')]
        self.ip_address_binary_octets  = [format(decimal_octet, '08b') for decimal_octet in self.ip_address_decimal_octets]

    @classmethod
    def validate(cls, ipv4_cidr):
        ipv4_cidr_notation_regex = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}"
        matching = re.fullmatch(ipv4_cidr_notation_regex, ipv4_cidr)
        
        if (matching == None):
            raise InvalidIPV4CIDRNotation

        subnetmask_number_aux = int(ipv4_cidr.split("/")[1])
        if (subnetmask_number_aux < 1 or subnetmask_number_aux > 31):
            raise InvalidSubnetMaskNumber

        octets_aux = ipv4_cidr.split("/")[0].split(".")
        for octet in octets_aux:
            if (int(octet) < 0 or int(octet) > 255):
                raise InvalidIPAddress


    def get_decimal_subnet_mask_as_str(self):
        binary_subnet_mask = self.get_binary_subnet_mask_as_str()
        decimal_subnet_mask = ''

        octets = binary_subnet_mask.split('.')
        for i, octet in enumerate(octets, start = 1):
            decimal_subnet_mask += str(int(octet, 2))
            if (i < 4): decimal_subnet_mask += '.' 

        return decimal_subnet_mask


    def get_binary_subnet_mask_as_str(self):

        binary_subnet_mask_as_string = ''

        for (index, subnet_bit) in enumerate(self.subnet_mask):
            binary_subnet_mask_as_string += str(subnet_bit)

            if (index in (7, 15, 23)):
                binary_subnet_mask_as_string += '.'

        return binary_subnet_mask_as_string
    

    def get_ip_class(self):
        if (self.subnet_mask_number >= 8 and self.subnet_mask_number < 16):
            return 'A'
        elif (self.subnet_mask_number >= 16 and self.subnet_mask_number < 24):
            return 'B'
        elif (self.subnet_mask_number >= 24 and self.subnet_mask_number < 32):
            return 'C'
        
        return None
    

    def get_network_address(self):
        ip_address_binary_octets_str_without_point = ''.join(self.ip_address_binary_octets)
        binary_network_address_str_without_point = ip_address_binary_octets_str_without_point[0:self.subnet_mask_number] + '0' * (32 - self.subnet_mask_number)

        binary_octets_network_address = [binary_network_address_str_without_point[i:i+8] for i in range(0, len(binary_network_address_str_without_point), 8)]

        network_address_octets = []
        for bin_octet_network_address in binary_octets_network_address:
            network_address_octets.append(int(bin_octet_network_address, base = 2))
        
        return '.'.join([str(network_address_octet) for network_address_octet in network_address_octets])


    def get_broadcast_address(self):
        ip_address_binary_octets_str_without_point = ''.join(self.ip_address_binary_octets)
        binary_network_address_str_without_point = ip_address_binary_octets_str_without_point[0:self.subnet_mask_number] + '1' * (32 - self.subnet_mask_number)

        binary_octets_network_address = [binary_network_address_str_without_point[i:i+8] for i in range(0, len(binary_network_address_str_without_point), 8)]

        network_address_octets = []
        for bin_octet_network_address in binary_octets_network_address:
            network_address_octets.append(int(bin_octet_network_address, base = 2))
        
        return '.'.join([str(network_address_octet) for network_address_octet in network_address_octets])
    
    
    def get_total_number_of_hosts(self):
        return (2 ** (32 - self.subnet_mask_number))


    def get_total_number_of_usable_hosts(self):
        return (self.get_total_number_of_hosts() - 2)


    def print_report(self):
        print(f"*** IP ADDRESS: {self.ip_address}")
        print(f"*** SUBNET MASK ({self.subnet_mask_number} bits): {self.get_decimal_subnet_mask_as_str()}")
        print(f"*** BINARY SUBNET MASK: {self.get_binary_subnet_mask_as_str()}")
        print(f"*** IP CLASS: {self.get_ip_class()}")
        print(f"*** NETWORK ADRESS: {self.get_network_address()}")
        print(f"*** BROADCAST ADRESS: {self.get_broadcast_address()}")
        print(f"*** TOTAL NUMBER OF HOSTS: {self.get_total_number_of_hosts()}")
        print(f"*** TOTAL NUMBER OF USABLE HOSTS: {self.get_total_number_of_usable_hosts()}")


def main():
    print('''
            ******************************************************************
            ********************* IPv4 SUBNET CALCULATOR *********************
            ******************************************************************
    ''')
    print('*** Type the IPV4 address in CIDR notation (e.g.: 192.168.1.55/24):')
    ipv4_cidr_typed = input()

    try:
        IPAddress.validate(ipv4_cidr_typed)
    except InvalidIPV4CIDRNotation as ex:
        print('*** Invalid notation.')
    except InvalidIPAddress as ex:
        print('*** Invalid IP addreess. Octets must be between 0 and 255.')
    except InvalidSubnetMaskNumber as ex:
        print('*** Invalid subnet mask number.')
    else:
        print('')
        print('*** Calculating...')
        print('')
        ip_address_typed, subnet_mask_typed = ipv4_cidr_typed.split('/')

        ip_address = IPAddress(str(ip_address_typed), int(subnet_mask_typed))
        ip_address.print_report()
    finally:
        sys.exit()

main()


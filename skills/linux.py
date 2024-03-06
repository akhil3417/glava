from utils.input_output import send_notification
import requests


def ip_address():
    """
    This function retrieves both IPv4 and IPv6 addresses using a free IP address service.
    """
    # This is a free service that returns your IP address
    ipv6 = requests.get("https://api64.ipify.org?format=json")
    ip_datav6 = ipv6.json()
    ip_addressv6 = ip_datav6["ip"]

    ipv4 = requests.get("https://api.ipify.org?format=json")
    ip_datav4 = ipv4.json()
    ip_addressv4 = ip_datav4["ip"]

    return ip_addressv4, ip_addressv6


async def ip_address_command_async():
    """
    A function to asynchronously retrieve the IP addresses and send a notification.
    """
    # Get the IP addresses
    ipv4, ipv6 = ip_address()

    # Send the notification
    send_notification("IP Addresses", f"IPv4: {ipv4}\nIPv6: {ipv6}")

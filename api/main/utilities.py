import socket


def create_socket():
    try:
        api_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        api_client.settimeout(2)
        return api_client
    except socket.error:
        print('Failed to create socket')
        return None

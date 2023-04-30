import os
import sys
from socket import AF_INET, SOCK_STREAM, socket
from utils import send_message, get_message
import time


def create_presence_message(account_name):
    message = {
        os.getenv('ACTION'): os.getenv('PRESENCE'),
        os.getenv('TIME'): time.time(),
        os.getenv('USER'): {
            os.getenv('ACCOUNT_NAME'): account_name
        }
    }
    return message


def parse_response(message):
    if os.getenv('RESPONSE') in message:
        if message[os.getenv('RESPONSE')] == 200:
            return '200 : OK'
        return f'400 : {message[os.getenv("ERROR")]}'
    raise ValueError


def main():
    global server_address, server_port

    try:
        if sys.argv[1] and sys.argv[2]:
            server_address, server_port = sys.argv[1], sys.argv[2]
    except IndexError:
        server_address, server_port = os.getenv('DEFAULT_IP_ADDRESS'), os.getenv('DEFAULT_PORT')

    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, int(server_port)))
    presence_message = create_presence_message('Guest')
    send_message(transport, presence_message)
    response = get_message(transport)

    print('Ответ сервера: ', response)
    print(parse_response(response))


if __name__ == '__main__':
    main()


import os
from socket import AF_INET, SOCK_STREAM, socket
import sys
from utils import send_message, get_message


def parse_message(message):
    if os.getenv('ACTION') in message \
            and message[os.getenv('ACTION')] == os.getenv('PRESENCE') \
            and os.getenv('TIME') in message \
            and os.getenv('USER') in message \
            and message[os.getenv('USER')][os.getenv('ACCOUNT_NAME')] == 'Guest':
        return {os.getenv('RESPONSE'): 200}
    return {
        os.getenv('RESPONSE'): 400,
        os.getenv('ERROR'): 'Bad Request'
    }


def main():
    global server_address, server_port
    try:
        if sys.argv[1] == '-a' and sys.argv[3] == '-p':
            head, a, server_address, p, server_port, *tail = sys.argv
            print(f'Сервер запущен с адресом {server_address} на {server_port} порту\n'
                  f'Для выхода нажмите CTRL+C')
        else:
            raise NameError
    except (IndexError, NameError):
        server_address = ''
        server_port = os.getenv('DEFAULT_PORT')
        print(f'Сервер запущен с настройками по умолчанию на {server_port} порту.\n'
              f'Для более точной кнфигурации задайте адресс и порт сервера: '
              f'$ python3 server.py -a [ip-адрес] -p [порт сервера]\n\n'
              f'Для выхода нажмите CTRL+C\n')

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((server_address, int(server_port)))
    transport.listen(int(os.getenv('MAX_CONNECTIONS')))

    while True:
        client, address = transport.accept()
        message = get_message(client)
        response = parse_message(message)
        send_message(client, response)
        client.close()

        print(f'Запрос от клиента: {message}\n'
              f'Код ответа для клиента: {response}')


if __name__ == '__main__':
    main()
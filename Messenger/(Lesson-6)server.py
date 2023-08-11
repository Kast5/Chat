from socket import *
import time
import json
import argparse
import logging
import server_log_config

serv_log = logging.getLogger('server')


def server_response(client_msg, client):
    json_resp = {}
    if client_msg["action"] == 'presence':
        json_resp = {
            "response": 200,
            "time": time.time(),
            "alert": "Подтрерждаю"
        }
    elif client_msg["action"] == 'msg':
        json_resp = {
            "response": 200,
            "time": time.time(),
            "alert": "Сообщение отправлено пользователю " + client_msg["to"]
        }
    msg = json.dumps(json_resp)
    client.send(msg.encode('utf-8'))
    client.close()


def recv_message(client, addr):
    data = client.recv(1024)
    serv_log.info("Сообщение %s было отправлено клиентом: %s" % (data.decode('utf-8'), str(addr)))
    json_mess = {}
    try:
        json_mess = json.loads(data.decode('utf-8'))
        serv_log.info("Сообщение: Action=%s длиной %s байт" % (str(json_mess["action"]),
                                                               str(len(data))))
    except json.decoder.JSONDecodeError:
        serv_log.critical("Сообщение от клиента не распознано %s" % data.decode('utf-8'))
    return json_mess


def server_communicate(s: socket):
    client, addr = s.accept()
    serv_log.info("Получен запрос на соединение от %s" % str(addr))
    msg_from_client = recv_message(client, addr)
    server_response(msg_from_client, client)


def parse_args():
    parser = argparse.ArgumentParser(description='Server App')
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777,
                        help="enter port number, default is 7777")
    parser.add_argument("-a", action="store", dest="addr", type=str, default='0.0.0.0',
                        help="enter IP address, default is 0.0.0.0")
    return parser.parse_args()


def main():
    args = parse_args()
    port = args.port
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)
    serv_log.info("Запущено прослушивание порта %s" % str(port))
    while True:
        server_communicate(s)



if __name__ == '__main__':
    main()
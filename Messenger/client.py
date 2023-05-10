from socket import *
import time
import argparse
import json
import logging
import client_log_config

cli_log = logging.getLogger('client')


def parse_message(str1):  # разобрать сообщение сервера;
    serv_message = {}
    try:
        serv_message = json.loads(str1.decode('utf-8'))
        if serv_message["response"] in (100, 101, 102, 200, 201, 202):
            cli_log.info("Сообщение доставлено на сервер, код возврата %s, %s " % (
            str(serv_message["response"]), serv_message["alert"]))
    except json.decoder.JSONDecodeError:
        cli_log.critical("Сообщение от сервера не распознано: %s ", str1)


def presence(username, status):
    return {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": username,
            "status": status
        }
    }


def message_from_user(from_user):
    to_user = ""
    while (len(to_user) == 0) or (len(to_user) > 25):
        to_user = input("Кому отправить сообщение:")
        if (len(to_user) == 0) or (len(to_user) > 25):
            print("имя пользователя/название чата должно содержать от 1 до 25 символов")
    msg = ""
    while (len(msg) == 0) or (len(msg) > 500):
        msg = input("Введите сообщение:")
        if (len(msg) == 0) or (len(msg) > 500):
            print("сообщение должно содержать максимум 500 символов")
    return {
        "action": "msg",
        "time": time.time(),
        "to": to_user,
        "from": from_user,
        "encoding": "utf-8",
        "message": msg
    }


def send_message(msg, s):
    cli_log.info("Sending message %s" % msg)
    s.send(msg.encode('utf-8'))


def get_response(s):
    data = s.recv(1024)
    parse_message(data)


def communicate(msg, resp, host, port):
    cli_log.info("Попытка соединения с %s по порту %s" % (host, port))
    my_socket = socket(AF_INET, SOCK_STREAM)
    try:
        my_socket.connect((host, port))
    except ConnectionRefusedError:
        cli_log.critical("Сервер %s недоступен по порту %s" % (host, port))
        return
    except OSError as err:
        cli_log.critical("OS error: {0}".format(err))
        return
    else:
        cli_log.info("Подключен к %s по порту %s" % (host, port))
    send_message(msg, my_socket)
    resp = get_response(my_socket)
    my_socket.close()



def parse_args():
    parser = argparse.ArgumentParser(description='Client App')
    parser.add_argument("-a", action="store", dest="addr", type=str, default='localhost',
                        help="enter IP address, default is localhost")
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777,
                        help="enter port number, default is 7777")
    return parser.parse_args()


def main():
    cli_log.debug('Старт приложения')
    args = parse_args()
    port = args.port
    host = args.addr
    resp = ''
    msg = json.dumps(presence("Artem", "Yes, I am here!"))
    communicate(msg, resp, host, port)
    msg = json.dumps(message_from_user("Artem"))
    communicate(msg, resp, host, port)



if __name__ == '__main__':
    main()
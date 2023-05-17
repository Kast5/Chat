from socket import *
import select
import time
import json
import argparse
import logging
import server_log_config

serv_log = logging.getLogger('server')

def server_response(incoming_msg):
    client_msg={}
    try:
        client_msg = json.loads(incoming_msg)
        serv_log.info("Сообщение: Action=%s длиной %s байт" % (str(client_msg["action"]),
                                                               str(len(incoming_msg))))
    except json.decoder.JSONDecodeError:
        serv_log.critical("Сообщение от клиента не распознано %s" % incoming_msg)
    json_resp = {}
    if client_msg["action"] == 'presence':
        json_resp = {
            "response": 200,
            "time": time.time(),
            "alert": "Соединение установлено"
        }
        print("%s вошел в чат" % client_msg["user"]["account_name"])
    elif client_msg["action"] == 'msg':
        json_resp = {
            "response": 200,
            "time": time.time(),
            "alert": "Сообщение отправлено пользователю " + client_msg["to"]
        }
        print("Сообщение от %s: %s" % (client_msg["from"], client_msg["message"]))
    msg = json.dumps(json_resp)
    return msg


def read_requests(r_clients, all_clients):
    requests = {}      # Список запросов от клиентов  вида {сокет: запрос}
    responses = {}     # Список ответов вида {сокет: запрос}
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            requests[sock] = data
            responses[sock] = server_response(data)
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
    return requests, responses


def write_responses(responses, w_clients, all_clients):

    for sock in w_clients:
        if sock in responses:
            try:

                resp = responses[sock].encode('utf-8')

                for client in all_clients:
                    client.sendall(resp)
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


def parse_args():
    parser = argparse.ArgumentParser(description='Server App')
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777,
                        help="enter port number, default is 7777")
    parser.add_argument("-a", action="store", dest="addr", type=str, default='0.0.0.0',
                        help="enter IP address, default is 0.0.0.0")
    return parser.parse_args()


def mainloop():
    args = parse_args()
    port = args.port
    clients = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)
    s.settimeout(1)
    serv_log.info("Запущено прослушивание порта %s" % str(port))
    while True:
        try:
            conn, addr = s.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:

            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass
            requests, responses = read_requests(r, clients)
            write_responses(responses, w, clients)



if __name__ == '__main__':
    mainloop()
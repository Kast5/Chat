import logging
import logging.handlers
import sys
import os


curr_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(curr_dir, 'log')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
logging_file = os.path.join(log_dir, 'server.log')
print("Логирование настроено в %s" % logging_file)


serv_log = logging.getLogger('server')

_format = logging.Formatter("%(asctime)s %(levelname)-10s %(module)s: %(message)s")


crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(_format)


applog_hand = logging.handlers.TimedRotatingFileHandler(logging_file, when='D', interval=1, encoding='utf-8',
                                                        backupCount=10)
applog_hand.setFormatter(_format)
applog_hand.setLevel(logging.DEBUG)


serv_log.addHandler(applog_hand)
serv_log.addHandler(crit_hand)
serv_log.setLevel(logging.DEBUG)

if __name__ == '__main__':

    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.DEBUG)
    console.setFormatter(_format)
    serv_log.addHandler(console)
    serv_log.info('Тестовый запуск логирования')
    serv_log.critical('critical!')
    serv_log.error('error!')
    serv_log.warning('warning!')
    serv_log.info('info!')
    serv_log.debug('debug!')
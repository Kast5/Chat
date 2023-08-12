import logging
import sys
import os


curr_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(curr_dir, 'log')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
logging_file = os.path.join(log_dir, 'client.log')
print("Логирование настроено в %s" % logging_file)

cli_log = logging.getLogger('client')

_format = logging.Formatter("%(asctime)s %(levelname)-10s %(module)s: %(message)s")


crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(_format)


applog_hand = logging.FileHandler(logging_file, encoding='utf-8')
applog_hand.setFormatter(_format)
applog_hand.setLevel(logging.DEBUG)


cli_log.addHandler(applog_hand)
cli_log.addHandler(crit_hand)
cli_log.setLevel(logging.DEBUG)

if __name__ == '__main__':

    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.DEBUG)
    console.setFormatter(_format)
    cli_log.addHandler(console)
    cli_log.info('Тестовый запуск логирования')
    cli_log.critical('critical!')
    cli_log.error('error!')
    cli_log.warning('warning!')
    cli_log.info('info!')
    cli_log.debug('debug!')
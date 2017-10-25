#
# Bench testing 3 common log file handlers and the impact of sudden file
# rotation by one process amoungst a group all writing to the same
# log file.
#
#
# Joel Knight
# www.packetmischief.ca


import argparse
import datetime
import logging
import logging.handlers
import time


logger = logging.getLogger('logtest')

def setup_logging(htype):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt='%(asctime)s pid/%(process)d %(message)s')
    handlers = {
        'rotating': logging.handlers.RotatingFileHandler(
                    'rotating/logtest.log',
                    maxBytes=1024 * 1024,
                    backupCount=10),
        'timed': logging.handlers.TimedRotatingFileHandler(
                    'timed/logtest.log', when='M', interval=1, backupCount=10),
        'watched': logging.handlers.WatchedFileHandler(
                    'watched/logtest.log')
    }
    handler = handlers[htype]
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    try:
        seq = 0
        while True:
            logger.info('Hello {}'.format(seq))
            time.sleep(1)
            seq = seq + 1
    except KeyboardInterrupt:
        logger.info('Goodbye')

def rotate():
    for h in list(logger.handlers):
        if type(h) is logging.handlers.RotatingFileHandler:
            print("Rolling over {} now ({})".format(h, datetime.datetime.now()))
            h.doRollover()
    print("Logging to {} now".format(h))
    main()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='rotate', action='store_true')
    parser.add_argument('-t', '--type', action='store')
    args = parser.parse_args()

    setup_logging(htype=args.type)

    if args.rotate:
        rotate()
    else:
        main()


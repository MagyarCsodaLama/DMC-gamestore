import logging


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

__version__ = '0.1.0'

def main():
    logger.info('Starting Gamestore %s', __version__)



if __name__ == '__main__':
    main()
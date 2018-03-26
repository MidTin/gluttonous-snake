import logging


logger = logging.getLogger('gluttonous-snake')
logger.setLevel(logging.DEBUG)

fmt = '[%(levelname)s] %(asctime)s %(funcName)s (%(pathname)s%(filename)s:%(lineno)d) > %(message)s'
formatter = logging.Formatter(fmt)

handler = logging.FileHandler('gluttonous-snake.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.addHandler(handler)

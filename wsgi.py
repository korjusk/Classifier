import time
import logging

f = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'
logging.basicConfig(filename=f'log/{int(time.time())}.log', filemode='a',
                    level=logging.DEBUG, format=f)
logging.info(f'{__name__} started.')

from flaskproject import app

if __name__ == "__main__":
    app.run(debug=False)
    logging.info(f'{__name__} ended.')

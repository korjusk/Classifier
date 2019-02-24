import logging

f = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'
logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO, format=f)
logging.info(f'{__name__} started.')

from flaskproject import app

if __name__ == "__main__":
    app.run(debug=True)
    logging.info(f'{__name__} ended.')

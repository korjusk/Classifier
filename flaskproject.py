import logging

logging.info(f'{__name__} started.')

from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True

logging.info('Imported flask.')

@app.route("/")
def greeting():
    logging.info('greeting() called.')
    index_html = open('index.html', 'r')
    return index_html.read()

@app.route('/handle_data', methods=['POST'])
def handle_data():
    logging.info('handle_data() called.')
    try:
        c1 = request.form['first']
        c2 = request.form['second']
        url = request.form['url']
        return classify([c1, c2], url)
    except Exception as ex:
        logging.exception('handle_data() exception.')
        import traceback
        return f'error <br>{traceback.format_exc()}'

@app.route('/test')
def test():
    logging.info('test() called.')
    try:
        import sys
        return f'{sys.version} <br>{sys.executable}'
    except Exception as ex:
        logging.exception('test() exception.')
        import traceback
        return f'error <br>{traceback.format_exc()}'


import json
import urllib.request
import http.client
http.client._MAXHEADERS = 1000


class GoogleImages:
    def __init__(self):
        pass

    # Downloading entire Web Document (Raw Page Content)
    def download_page(self, url):
        try:
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            return str(resp.read())
        except Exception as e:
            print("Could not open URL.")

    # Finding 'Next Image' from the given raw page
    def _get_next_item(self, s):
        start_line = s.find('rg_meta notranslate')
        if start_line == -1:  # If no links are found then give an error!
            end_quote = 0
            link = "no_links"
            return link, end_quote
        else:
            start_line = s.find('class="rg_meta notranslate">')
            start_object = s.find('{', start_line + 1)
            end_object = s.find('</div>', start_object + 1)
            object_raw = str(s[start_object:end_object])

            try:
                object_decode = bytes(object_raw, "utf-8").decode(
                    "unicode_escape")
                final_object = json.loads(object_decode)
            except:
                final_object = ""

            return final_object, end_object

    # Getting all links with the help of '_images_get_next_image'
    def _get_all_items(self, page, limit):
        items = []
        i = 0
        count = 1
        while count < limit+1:
            obj, end_content = self._get_next_item(page)
            if obj == "no_links":
                break
            elif obj == "":
                page = page[end_content:]
            else:
                items.append(obj['ou'])

                page = page[end_content:]
            i += 1

        return items

    def save_url(self, key):
        search_keyword = key.replace('_', '+')

        main_directory = "data"
        fname = f'{main_directory}/urls_{key}'

        # Image, Medium size, full color
        url = f'https://www.google.com/search?q={search_keyword}&tbm=isch&tbm=isch&tbs=isz:m,ic:color'
        print(f'{key}: {url}')

        raw_html = self.download_page(url)
        limit = 1 # if limit > 101: use 'chromedriver'
        items = self._get_all_items(raw_html, limit)

        with open(fname, 'w') as f:
            for item in items:
                f.write("%s\n" % item)

        print(f'Saved {len(items)} URLs to {fname}')


from fastai.vision import *
import save_urls
import subprocess

path = Path('data')
t_url = 'https://pbs.twimg.com/profile_images/759735485388427265/LeMLP89w.jpg'
image_size = 224


def urls_to_pics(c):
    file = f'urls_{c}'
    dest = path / 'train' / c

    print(f'Downloading "{c}" pictures into {dest}. [{len(dest.ls())}]')

    download_images(path / file, dest, max_pics=100, timeout=1)
    print(f'Download completed. [{len(dest.ls())}]')

    verify_images(dest, delete=True, max_size=image_size * 2)
    print(f'Verifycation complete. \n\nTotal {len(dest.ls())} {c} images.\n\n')


def gather_data(classes):
    for c in classes:
        dest = path / 'train' / c
        dest.mkdir(parents=True, exist_ok=True)
        c_len = len(dest.ls())

        if c_len > 60:
            print(f'Downloading skipped. {c_len} images in {dest}')
        else:
            response = save_urls.GoogleImages()
            response.save_url(c)
            urls_to_pics(c)


def classify(classes, url):
    logging.info(f"classify({classes}, '{url}') called.")
    Path('data/test').mkdir(parents=True, exist_ok=True)
    res = subprocess.check_output(f'wget -q -P ./data/test {url}'.split(' '))
    gather_data(classes)

    np.random.seed(42)
    data = ImageDataBunch.from_folder(path/'train', valid_pct=0.2, ds_tfms=get_transforms(), size=image_size, num_workers=4, test='test').normalize(imagenet_stats)

    print(f'Classes: {data.classes}')

    learn = create_cnn(data, models.resnet34, metrics=error_rate)
    learn.fit_one_cycle(5)
    #learn.save('stage-1')

    img = learn.data.test_ds[0][0]
    result = learn.predict(img)
    return f'Success. <br>Classes: {data.classes} <br>Url: {url} <br>Result: {result}'


if __name__ == "__main__":
    app.run(host='0.0.0.0')



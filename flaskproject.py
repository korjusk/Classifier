import logging

logging.info(f'{__name__} started.')

from flask import Flask
from flask import request
from fastai.vision import *
import urllib.request
import http.client
import shutil

path = Path('data')
image_size = 224
http.client._MAXHEADERS = 1000

app = Flask(__name__)
app.debug = False

logging.info('Flask started')


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
        result = classify([c1.strip().lower(), c2.strip().lower()], url.strip())
        logging.info('handle_data() Success!')
        return result
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


def class_to_url(c):
    c = c.replace('_', '+')
    # Image, Medium size, full color
    return f'https://www.google.com/search?q={c}&tbm=isch&tbm=isch&tbs=isz:m,ic:color'


class GoogleImages:
    def __init__(self):
        pass

    # Downloading entire Web Document (Raw Page Content)
    def download_page(self, url):
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            return str(resp.read())
        except Exception as e:
            logging.exception('Could not open URL.')

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
        while count < limit + 1:
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
        url = class_to_url(key)
        logging.info(f'{key}: {url}')

        raw_html = self.download_page(url)
        limit = 100  # if limit > 101: use 'chromedriver'
        items = self._get_all_items(raw_html, limit)

        fname = f'data/urls_{key}'
        with open(fname, 'w') as f:
            for item in items:
                f.write("%s\n" % item)

        logging.info(f'Saved {len(items)} URLs to {fname}')


def urls_to_pics(c):
    file = f'urls_{c}'
    dest = Path(f'sets/{c}')

    logging.info(f'Downloading "{c}" pictures into {dest}. [{len(dest.ls())}]')

    download_images(path / file, dest, max_pics=100, timeout=1)
    logging.info(f'Download completed. [{len(dest.ls())}]')

    verify_images(dest, delete=True, max_size=image_size * 2)
    logging.info(
        f'Verification complete. Total {len(dest.ls())} {c} images.')


def gather_data(classes):
    for c in classes:
        c = c.replace(" ", "_")
        train = path / 'train'
        train.mkdir(parents=True, exist_ok=True)

        sets = Path(f'sets/{c}')
        sets.mkdir(parents=True, exist_ok=True)

        if len(sets.ls()) > 50:
            logging.info(
                f'Downloading skipped. {len(sets.ls())} images in {sets}')
        else:
            google_img = GoogleImages()
            google_img.save_url(c)
            urls_to_pics(c)

        shutil.copytree(f'sets/{c}', f'data/train/{c}')


def classify(classes, url):
    logging.info(f"classify({classes}, '{url}') called.")

    path.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(path)
    logging.info(f'Deleted {path}')

    path.mkdir(parents=True, exist_ok=True)
    with open("data/test_urls", "w") as text_file:
        print(url, file=text_file)

    download_images('data/test_urls', 'data/test')
    logging.info('Downloaded test image')

    gather_data(classes)

    np.random.seed(42)

    logging.info(f'Got images, make DataBunch')
    data = ImageDataBunch.from_folder(path / 'train', valid_pct=0.2,
                                      ds_tfms=get_transforms(), size=image_size,
                                      num_workers=4, bs=8).normalize(
        imagenet_stats)

    logging.info(f'data.classes: {data.classes}')

    learn = create_cnn(data, models.resnet34, metrics=error_rate)
    logging.info('Created CNN')

    learn.fit_one_cycle(5)
    logging.info('Finished training CNN')
    # learn.save('stage-1')

    test_path = Path('data/test')
    test_files = test_path.ls()

    if len(test_files) == 0:
        err = f'Failed to load image from: {url}'
        logging.error(err)
        return err

    logging.info(f'Open image {test_files[0]}')
    img = open_image(test_files[0])

    logging.info('Starting to predict.')
    result = learn.predict(img)
    logging.info(f'::Result:: {result}')

    c0 = data.classes[0]
    c1 = data.classes[1]

    c0_url = class_to_url(c0)
    c1_url = class_to_url(c1)

    with open('success.html', 'r') as success:
        html = success.read()

    return html % (result[0], url, url, url, c0_url, c0, c1_url, c1, result[2])


if __name__ == "__main__":
    app.run(host='0.0.0.0')

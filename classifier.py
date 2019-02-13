# coding: utf-8

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
    Path('data/test').mkdir(parents=True, exist_ok=True)
    res = subprocess.check_output(f'wget -q -P ./data/test {url}'.split(' '))
    gather_data(classes)
    return f'{classes}, {url}'


#np.random.seed(42)
#data = ImageDataBunch.from_folder(path/'train', valid_pct=0.2, ds_tfms=get_transforms(),
#                                  size=image_size, num_workers=4, test='test').normalize(imagenet_stats)

#print(f'Classes: {data.classes}')


# learn = create_cnn(data, models.resnet34, metrics=error_rate)
# learn.fit_one_cycle(5)
# learn.save('stage-1')

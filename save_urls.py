#!/usr/bin/env python
#  coding: utf-8

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
        limit = 100 # if limit > 101: use 'chromedriver'
        items = self._get_all_items(raw_html, limit)

        with open(fname, 'w') as f:
            for item in items:
                f.write("%s\n" % item)

        print(f'Saved {len(items)} URLs to {fname}')


if __name__ == "__main__":
    response = GoogleImages()
    response.save_url('cat')

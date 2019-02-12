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

    def save_url(self, search_keyword):
        # if limit > 101: download_extended_page(url,arguments['chromedriver'])
        limit = 100

        main_directory = "data"
        paths = {}
        dir_name = search_keyword.replace(' ', '_')

        url = f'https://www.google.com/search?q={search_keyword}&tbm=isch'
        print(f'{search_keyword}: {url}')

        raw_html = self.download_page(url)
        items = self._get_all_items(raw_html, limit)

        with open(f'{main_directory}/urls_{dir_name}', 'w') as f:
            for item in items:
                f.write("%s\n" % item)

        print(f'Saved {len(items)} URLs to {main_directory}/urls_{dir_name}')

        return paths


if __name__ == "__main__":
    response = GoogleImages()
    response.save_url('cat')

'''
Scrap web page and downloads pictures for the PC screen background.
Scrap links in web pages for download of files with picture (for the PC screen background).
Srapping is executed per picture theme.
Picture themes for download are set to: Switzerland, Poland, fractal, paintings reproductions, nature
'''

import urllib.request
import urllib
import re
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests

import time

# Below is formed in this way: key-theme hava a list as value,
# list under [0] has initial-theme-page-link and under [1] number of pages within this theme to be scrapped.
# Number of scrapped pages is set to few only out of all available. It is to limit required time and space.
picture_themes = { 
    'Switzerland': ['https://www.tapeciarnia.pl/szwajcaria?st=', 2], # 2 set instead of 23 available
    'Poland' : ['https://www.tapeciarnia.pl/polska?st=', 2], # 2 set instead of 34 available
    'fractal' : ['https://www.tapeciarnia.pl/fraktal?st=', 2], # 2 set instead of 23 available
    'paintings reproductions' : ['https://www.tapeciarnia.pl/reprodukcje_obrazow?st=', 2], # 2 set instead of 149 available
    'nature' : ['https://www.tapeciarnia.pl/przyroda?st=', 2] } # 2 set instead of 2977 available


def get_pics(picture_themes):

    for theme in picture_themes:
        url_theme = picture_themes[theme][0]
        num_of_pages_in_the_theme = picture_themes[theme][1]

        print('Getting pictures for the theme {}.\n'.format(theme))
        start_time = time.time()

        for page in range(1, num_of_pages_in_the_theme):
            url = url_theme + str(page)

            resp = requests.get(url)
            http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
            html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
            encoding = html_encoding or http_encoding
            soup = BeautifulSoup(resp.content, features="html.parser", from_encoding=encoding)

            linki = []
            counter_all = 0
            counter_all_non_https = 0
            for link in soup.find_all('a', href=True):
                linki.append(link)

                smalllink = link.find('img', src=True)
                if smalllink:
                    for key in smalllink.attrs.keys():
                        if key == 'src' and ('tapety/srednie' in smalllink.attrs[key]):
                            counter_all += 1
                        
                        if key == 'src' and ('tapety/srednie' in smalllink.attrs[key]) and not ('https://www.tapeciarnia.pl/tapety' in smalllink.attrs[key]) :
                            counter_all_non_https += 1
                            address_parts = smalllink.attrs[key].split('/srednie/')
                            jpg_file_name = address_parts[1]
                            new_address = 'https://www.tapeciarnia.pl/tapety/normalne/'+jpg_file_name

                            f = open(jpg_file_name,'wb')
                            f.write(urllib.request.urlopen(new_address).read())
                            f.close()
                            print('\t', jpg_file_name)

            print('Scrapped from:', url)
        print('Total time for download of', page, 'pages with the', theme, 'theme was {:.1f} seconds.\n'.format((time.time() - start_time)))
        print('-' * 32)


def main():
    get_pics(picture_themes)


if __name__ == "__main__":
    main()

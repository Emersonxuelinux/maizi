# -*- coding: utf-8 -*-
import requests
from HTMLParser import HTMLParser


class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []
        # 这个标记标识标签内部师父有电影，默认无
        self.in_movies = False

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None

        if tag == 'li' and _attr(attrs, 'data-title') and _attr(attrs, 'data-category') == 'nowplaying':
            movie = {}
            movie['title'] = _attr(attrs, 'data-title')
            movie['score'] = _attr(attrs, 'data-score')
            movie['director'] = _attr(attrs, 'data-director')
            movie['actors'] = _attr(attrs, 'data-actors')
            self.movies.append(movie)
            print('%(title)s|%(score)s|%(director)s|%(actors)s' % movie)
            # 如果该标签存在电影，就改为true
            self.in_movies = True

        # 只下载内部有电影信息的img标签的图片
        if tag == 'img' and self.in_movies:
            self.in_movies = False
            movie = self.movies[len(self.movies) - 1]
            movie['cover-url'] = _attr(attrs, 'src')
            _download_poster_cover(movie)

# 这个方法专门用于下载电影海报
def _download_poster_cover(movie):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    url = movie['cover-url']
    print('downloading post cover from %s' % url)
    # 用requests的get方法来获取图片文件，不同于urllib.urlretrieve
    s = requests.get(url, headers=headers)
    fname = url.split('/')[-1]
    # 因为是图片文件，注意用二进制方式打开
    with open(fname, 'wb') as f:
        f.write(s.content)
    movie['cover-file'] = fname


def nowplaying_movies(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    s = requests.get(url, headers=headers)
    parser = MovieParser()
    # request用不同的输出数据方式
    parser.feed(s.content)
    return parser.movies


if __name__ == '__main__':
    url = 'http://movie.douban.com/nowplaying/xiamen/'
    movies = nowplaying_movies(url)

    import json
    print('%s' % json.dumps(movies, sort_keys=True, indent=4, separators=(',', ': ')))

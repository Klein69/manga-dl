from manga_py.provider import Provider
from .helpers.std import Std


class TuMangaOnlineCom(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}-{}'.format(*self.chapter)

    def get_chapter_index(self) -> str:
        return '{}-{}'.format(*self.chapter)

    def get_main_content(self):
        url = '{}/api/v1/mangas/{}'.format(self.domain, self._get_id())
        data = self.http_get(url=url, headers=self._get_headers())
        return self.json.loads(data)

    def get_manga_name(self) -> str:
        url = self.get_url()
        re = r'/mangas/\d+/([^/]+)'
        if ~url.find('/lector/'):
            re = '/lector/([^/]+)'
        return self.re.search(re, url).group(1)

    @staticmethod
    def _get_subidas(items, n):
        return [(n, i.get('idScan')) for i in items.get('subidas', [])]

    def get_chapters(self):
        url = '{}/api/v1/mangas/{}/capitulos?page=1&tomo=-1'
        idx = self._get_id()

        url = url.format(self.domain, idx)
        data = self.http_get(url=url, headers=self._get_headers())
        items = self.json.loads(data).get('data', [])

        pages = []
        for i in items:
            n = i.get('numCapitulo')
            pages += self._get_subidas(i, n)
        return pages

    def _get_id(self):
        url = self.get_url()
        re = r'/mangas/(\d+)'
        if ~url.find('/lector/'):
            re = r'/lector/[^/]+/(\d+)'
        return self.re.search(re, url).group(1)

    @staticmethod
    def _get_headers():
        return {'Cache-mode': 'no-cache', 'X-Requested-With': 'XMLHttpRequest'}

    def prepare_cookies(self):
        self._base_cookies()

    def get_files(self):
        idx = self._get_id()
        domain = self.domain
        url = '{}/api/v1/imagenes?idManga={}&idScanlation={}&numeroCapitulo={}&visto=true'
        ch = self.chapter
        data = self.http_get(url=url.format(domain, idx, *ch), headers=self._get_headers())

        items = self.json.loads(self.json.loads(data).get('imagenes', '[]'))
        url = 'https://img1.tumangaonline.com/subidas/{}/{}/{}/{}'

        return [url.format(idx, *ch, i) for i in items]

    def get_cover(self) -> str:
        url = self.domain, self.content.get('imageUrl', None)
        if url:
            return '{}/{}'.format(self.domain, url)

    def book_meta(self) -> dict:
        # todo meta
        pass


main = TuMangaOnlineCom

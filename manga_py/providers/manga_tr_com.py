from manga_py.provider import Provider
from .helpers.std import Std


class MangaTrCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = self.re.search('-chapter-(.+)\.html', chapter).group(1)
        return '-'.join(idx.split('.'))

    def get_main_content(self):
        return self._get_content('{}/manga-{}.html')

    def get_manga_name(self) -> str:
        url = self.get_url()
        re = r'\d-read-(.+)-chapter-'
        if ~url.find('/manga-'):
            re = r'/manga-(.+)\.html'
        return self.re.search(re, url).group(1)

    def get_chapters(self):
        return self._elements('#results td.left a')

    def get_files(self):
        img_selector = 'img.chapter-img'
        parser = self.html_fromstring(self.chapter)
        pages = self._first_select_options(parser, '.chapter-content select')
        images = self._images_helper(parser, img_selector)
        n = self.http().normalize_uri
        for i in pages:
            parser = self.html_fromstring(n(i))
            images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('img.thumbnail')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaTrCom

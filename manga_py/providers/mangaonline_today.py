from manga_py.provider import Provider
from .helpers.std import Std


class MangaOnlineToday(Provider, Std):
    _img_selector = '#sct_content img'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('.')
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\.today/[^/]+/([^/]+)', self.chapter)
        return idx.group(1)

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.today/([^/]+)')

    def get_chapters(self):
        return self._elements('ul.chp_lst a')

    def _pages_helper(self, options):
        images = []
        chapter = self.chapter
        for n in range(1, int(options)):
            content = self.html_fromstring('{}{}/'.format(chapter, n * 2 + 1))
            img = content.cssselect(self._img_selector)
            for i in img:
                images.append(i.get('src'))
        return images

    def get_files(self):
        images = []
        content = self.html_fromstring(self.chapter)
        img = content.cssselect(self._img_selector)
        if img:
            images = [i.get('src') for i in img]

        options = len(content.cssselect('.cbo_wpm_pag')[0].cssselect('option')) / 2 + .5
        return images + self._pages_helper(options)

    def get_cover(self):
        pass  # TODO

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaOnlineToday

from manga_py.provider import Provider
from .helpers.std import Std


class PornComixInfo(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.info/([^/]+)')

    def get_chapters(self):
        return [b'']

    def get_files(self):
        items = self._elements('.gallery-item a > img')
        images = []
        re = self.re.compile(r'(.+/images/.+\d)-\d+x\d+(\.\w+)')
        for i in items:
            g = re.search(i.get('data-lazy-src')).groups()
            images.append('{}{}'.format(*g))
        return images

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = PornComixInfo

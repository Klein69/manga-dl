from manga_py.provider import Provider
from .helpers.std import Std


class MangaBoxMe(Provider, Std):
    _local_storage = False

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._storage['current_chapter'])

    def get_chapter_index(self) -> str:
        return self.re.search(r'/episodes/(\d+)', self.chapter).group(1)

    def get_main_content(self):
        if not self._local_storage:
            idx = self._get_name(r'/reader/(\d+)/episodes/')
            self._local_storage = True
            return self.http_get('{}/reader/{}/episodes/'.format(self.domain, idx))
        return self.content

    def get_manga_name(self) -> str:
        selector = 'meta[property="og:title"]'
        title = self.document_fromstring(self.content, selector, 0)
        return title.get('content').strip()

    def get_chapters(self):
        selector = '.episodes_list .episodes_item > a'
        return self._elements(selector)

    def get_files(self):
        items = self.html_fromstring(self.chapter, 'ul.slides li > img')
        return [i.get('src') for i in items]

    def get_cover(self):
        return self._cover_from_content('.episodes_img_main', 'data-src')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaBoxMe

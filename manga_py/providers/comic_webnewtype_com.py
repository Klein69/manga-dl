from manga_py.provider import Provider
from .helpers.std import Std


class ComicWebNewTypeCom(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.compile('/contents/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/contents/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/contents/([^/]+)')

    def get_chapters(self):
        return self._elements('#episodeList li.ListCard a')

    def get_files(self):
        url = self.chapter
        items = self.http_get(url + 'json/', headers={'x-requested-with': 'XMLHttpRequest'})
        return self.json.loads(items)

    def get_cover(self) -> str:
        return self._cover_from_content('.WorkSummary-content img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ComicWebNewTypeCom

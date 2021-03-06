from manga_py.provider import Provider
from .helpers.std import Std


class ReadmangaMe(Provider, Std):

    def get_archive_name(self):
        name = self.re.search('/.+/([^/]+/[^/]+)/?', self.chapter)
        return name.group(1).replace('/', '-')

    def get_chapter_index(self):
        name = self.re.search('/.+/(?:vol)?([^/]+/[^/]+)/?', self.chapter)
        return name.group(1).replace('/', '-')

    def get_main_content(self):
        return self._get_content('{}/{}?mature=1&mtr=1')

    def get_manga_name(self):
        return self._get_name(r'\.me/([^/]+)')

    def get_chapters(self):
        return self._elements('div.chapters-link tr > td > a')

    def get_files(self):
        _uri = self.http().normalize_uri(self.chapter)
        content = self.http_get(_uri)
        result = self.re.search(r'rm_h\.init.+?(\[\[.+\]\])', content, self.re.M)
        if not result:
            return []
        return [i[1] + i[0] + i[2] for i in self.json.loads(result.groups()[0].replace("'", '"'))]

    def get_cover(self):
        return self._cover_from_content('.picture-fotorama > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadmangaMe

from src.provider import Provider
from .helpers.std import Std


class PecintaKomikCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}'
        return fmt.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.get_current_chapter()
        idx = self.re.search('/manga/[^/]+/(\d+(?:,\d)?)', idx)
        return '-'.join(idx.group(1).split(','))

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,5}/([^/]+)')

    def get_chapters(self):
        return self._elements('.post-cnt ul > li > a')

    def get_files(self):
        url = self.get_current_chapter() + '/full'
        parser = self.html_fromstring(url)
        items = parser.cssselect('td a .picture')
        base = parser.cssselect('base[href]')
        if base:
            base = base[0].get('href')
        else:
            base = url
        n = self.http().normalize_uri
        return [n(i.get('src'), base) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('img.pecintakomik')


main = PecintaKomikCom

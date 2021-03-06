from .gomanga_co import GoMangaCo


class JapScanCom(GoMangaCo):
    _name_re = r'\.c(?:om|c)/[^/]+/([^/]+)/'
    _content_str = '{}/mangas/{}/'
    _chapters_selector = '#liste_chapitres ul li a'

    def get_archive_name(self) -> str:
        idx = self.chapter_id, self.get_chapter_index()
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'\.c(?:om|c)/[^/]+/[^/]+/(\d+)/'
        url = self.chapter
        return self.re.search(selector, url).group(1)

    def get_files(self):
        img_selector = '#image'
        n = self.http().normalize_uri
        parser = self.html_fromstring(self.chapter)
        pages = parser.cssselect('#pages option + option')
        images = self._images_helper(parser, img_selector)
        for i in pages:
            parser = self.html_fromstring(n(i.get('value')))
            images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self) -> str:
        pass


main = JapScanCom

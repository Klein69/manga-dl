from src.provider import Provider


class MangaChanMe(Provider):
    _full_name_selector = '/(?:online|manga|related)/(\\d+\\-.+\\.html)'
    _idx_selector = '/(?:online|manga|related)/(\\d+)\\-'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        name = self.get_current_chapter()
        idx = self.re.search('_v(\\d+)_ch(\\d+)', name).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        pass

    def _online_(self, url):
        if self.re.search('/online/\\d+', url):
            content = self.http_get(url)
            url = self.re.search('content_id.+?(/manga/.+\\.html)', content).group(1)
        return url

    def get_manga_name(self) -> str:
        _name_selector = '/(?:online|manga|related)/\\d+\\-(.+)\\.html'
        url = self._online_(self.get_url())
        return self.re.search(_name_selector, url).group(1)

    def get_chapters(self):
        url = self._online_(self.get_url())
        url = '{}/manga/{}'.format(
            self.get_domain(),
            self.re.search(self._full_name_selector, url).group(1)
        )
        items = self.html_fromstring(url, '.table_cha .manga a')
        nu = self.http().normalize_uri
        return [nu(i.get('href')) for i in items]

    def prepare_cookies(self):
        pass

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        items = self.re.search('"?fullimg"?\\s?:\\s?(\[.+\])', content).group(1)
        images = self.json.loads(items.replace('",]', '"]'))  # patch
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaChanMe
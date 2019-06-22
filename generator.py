import requests
from pyquery import PyQuery as pq
from urllib.parse import urlparse


class Generator:
    def __init__(self, url, depth):
        parsed_url = urlparse(url)
        self.url = parsed_url.scheme + '://' + parsed_url.netloc
        self.netloc = parsed_url.netloc.lstrip('www.')
        self.depth = depth
        self.hyperlinks_homepage = []

    def generate(self):
        level = 1

        # first gather all homepage links to avoid loop
        self.get_hyperlinks(self.url)

        # build sitemap tree
        return self.build_hyperlinks_tree(self.hyperlinks_homepage, level+1, hyperlinks_raw=False)

    def get_hyperlinks(self, url, level=None):
        try:
            response = requests.get(url)
        except Exception as e:
            print(e)
            return {}

        if response.status_code == 200:
            pyquery = pq(response.content)
            selector = pyquery("a[href]")
            hyperlinks = [pq(element).attr.href for element in selector]

            if level:
                return self.build_hyperlinks_tree(hyperlinks, level)

            # homepage hyperlinks
            for link in hyperlinks:
                parsed_path = self.get_parsed_path(link)

                if parsed_path:
                    self.hyperlinks_homepage.append(parsed_path)

        return {}

    def build_hyperlinks_tree(self, hyperlinks, level, hyperlinks_raw=True):
        hyperlinks_tree = {}
        for link in hyperlinks:

            parsed_path = link
            if hyperlinks_raw:
                parsed_path = self.get_parsed_path(link)

            if parsed_path:

                hyperlinks_tree[parsed_path] = {}
                if level <= self.depth:
                    hyperlinks_tree[parsed_path] = self.get_hyperlinks(parsed_path, level + 1)

        return hyperlinks_tree

    def get_parsed_path(self, hyperlink):
        parsed_link = urlparse(hyperlink.strip())

        if parsed_link.netloc and self.netloc not in parsed_link.netloc:
            return None  # skip external hyperlinks

        if parsed_link.scheme and parsed_link.scheme == 'javascript':
            return None  # skip javascript hyperlinks

        if parsed_link.path:
            parsed_path = parsed_link.path.lstrip('/\t\n\r ').replace('www.', '')
        else:
            return None  # skip empty hyperlinks

        if parsed_path in ['index.html', 'index.php', '#', '']:
            return None  # skip index hyperlinks

        full_path = self.url + '/' + parsed_path
        if parsed_link.scheme and parsed_link.netloc:
            full_path = parsed_link.scheme + '://' + parsed_link.netloc + '/' + parsed_path

        if full_path in self.hyperlinks_homepage:
            return None  # skip homepage hyperlinks (avoid looping)

        return full_path


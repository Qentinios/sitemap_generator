import requests
from pyquery import PyQuery as pq
from urllib.parse import urlparse


class Generator:
    def __init__(self, url, depth):
        parsed_url = urlparse(url)
        self.url = parsed_url.scheme + '://' + parsed_url.netloc
        self.netloc = parsed_url.netloc
        self.depth = depth
        self.hyperlinks_homepage = []

    def generate(self):
        level = 1
        self.get_homepage_links()

        return self.build_hyperlinks_tree(self.hyperlinks_homepage, level+1, hyperlinks_raw=False)

    def get_homepage_links(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            pyquery = pq(response.content)
            selector = pyquery("a[href]")
            homepage_links = [pq(element).attr.href for element in selector]

            for link in homepage_links:
                parsed_path = self.get_parsed_path(link)

                if parsed_path:
                    self.hyperlinks_homepage.append(parsed_path)

    def get_parsed_path(self, hyperlink):
        parsed_link = urlparse(hyperlink)

        if parsed_link.netloc and parsed_link.netloc != self.netloc:
            return None  # skip external hyperlinks

        if parsed_link.scheme and parsed_link.scheme == 'javascript':
            return None  # skip javascript hyperlinks

        if parsed_link.path:
            parsed_path = parsed_link.path.lstrip('/')
        else:
            return None  # skip empty hyperlinks

        if parsed_path in ['index.html', 'index.php', '#']:
            return None  # skip index hyperlinks

        if parsed_path in self.hyperlinks_homepage:
            return None  # skip homepage hyperlinks (avoid looping)

        return parsed_path

    def build_hyperlinks_tree(self, hyperlinks, level, hyperlinks_raw=True):
        hyperlinks_tree = {}
        for link in hyperlinks:
            if hyperlinks_raw:
                parsed_path = self.get_parsed_path(link)
            else:
                parsed_path = link

            if parsed_path:
                if level <= self.depth:
                    hyperlinks_tree[parsed_path] = self.get_links_rec(self.url + '/' + parsed_path, level + 1)
                else:
                    hyperlinks_tree[parsed_path] = {}

        return hyperlinks_tree

    def get_links_rec(self, url, level):
        response = requests.get(url)

        if response.status_code == 200:
            pyquery = pq(response.content)
            selector = pyquery("a[href]")
            hyperlinks = [pq(element).attr.href for element in selector]

            return self.build_hyperlinks_tree(hyperlinks, level)

        return {}


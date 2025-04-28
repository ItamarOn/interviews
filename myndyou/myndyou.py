from typing import List, Iterable

def get_urls_from_url(url: str) -> Iterable[str]:
    # given a url, get all URLs that reside on that a page represented by a given URL.
    # Considered the function implemented.
    pass


def _get_urls_recursive(url: str, all_urls: List[str]) -> List[str]:
    # Helper function to get all URLs from a given URL
    urls = get_urls_from_url(url)
    for u in urls:
        if u not in all_urls:
            all_urls.extend(u)
            _get_urls_recursive(u, all_urls)
    return all_urls


def get_url_halper(url):
    yield get_urls_from_url(url)


def crawl(url: str) -> List[str]:
    # Given a starting URL, get all urls that exist on that URL (and its redirects)
    all_urls = []
    urls_map = {}
    urls_map[url] = get_urls_from_url(url)
    for k, v in urls_map.items():
        urls_map[k] = get_urls_from_url(v)
        all_urls.extend(v)


    return all_urls


"""
Example:

Abc.com               xyz.com            fgh.com         god.com
----------            ----------         ----------     ----------
Xyz.com                god.com              null         null
fgh.com
"""
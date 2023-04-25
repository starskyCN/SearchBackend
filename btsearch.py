import re
import time
import requests
from bs4 import BeautifulSoup


class Bitsearch:
    def __init__(self):
        self.BASE_URL = "https://bitsearch.to"
        self.LIMIT = None

    def _parser(self, htmls):
        try:
            soup = BeautifulSoup(htmls, "lxml")
            my_dict = {"data": []}
            i = 0
            for divs in soup.find_all("li", class_="search-result"):
                i = i + 1
                info = divs.find("div", class_="info")
                name = info.find("h5", class_="title").find("a").text
                url = info.find("h5", class_="title").find("a")["href"]
                category = info.find("div").find("a", class_="category").text
                if not category:
                    continue
                stats = info.find("div", class_="stats").find_all("div")
                if stats:
                    downloads = stats[0].text
                    size = stats[1].text
                    seeders = stats[2].text.strip()
                    leechers = stats[3].text.strip()
                    date = stats[4].text
                    links = divs.find("div", class_="links").find_all("a")
                    magnet = links[1]["href"]
                    torrent = links[0]["href"]

                    img = 'https://images.pexels.com/photos/388898/pexels-photo-388898.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1' if i%2 == 0 else 'https://media.tenor.com/sVvqNXxAF9IAAAAd/michael-oliver-problem-child.gif'
                    my_dict["data"].append(
                        {
                            "name": name,
                            "size": size,
                            "seeders": seeders,
                            "leechers": leechers,
                            "category": category,
                            "hash": re.search(
                                r"([{a-f\d,A-F\d}]{32,40})\b", magnet
                            ).group(0),
                            "magnet": magnet,
                            "torrent": torrent.replace("[Bitsearch.to]", "[MagnetX]"),
                            # "url": self.BASE_URL + url,
                            "date": date,
                            "downloads": downloads,
                            "img": img,
                            "imgLink":"https://hao123.com/"
                        }
                    )
                if len(my_dict["data"]) == self.LIMIT:
                    break
            try:
                total_pages = (
                    int(
                        soup.select(
                            "body > main > div.container.mt-2 > div > div:nth-child(1) > div > span > b"
                        )[0].text
                    )
                    / 20
                )  # !20 search result available on each page
                total_pages = (
                    total_pages + 1
                    if type(total_pages) == float
                    else total_pages
                    if int(total_pages) > 0
                    else total_pages + 1
                )

                current_page = int(
                    soup.find("div", class_="pagination")
                    .find("a", class_="active")
                    .text
                )
                my_dict["current_page"] = current_page
                my_dict["total_pages"] = int(total_pages)
            except:
                pass
            return my_dict
        except:
            return None

    def search(self, query, page, limit, category, sort):
        start_time = time.time()
        self.LIMIT = limit
        url = self.BASE_URL + "/search?q={}&page={}&category={}&sort={}".format(query, page, category, sort)
        return self.parser_result(start_time, url)

    def parser_result(self, start_time, url):
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36"})
        results = self._parser(resp.text)
        if results != None:
            results["time"] = time.time() - start_time
            results["total"] = len(results["data"])
            return results
        return results

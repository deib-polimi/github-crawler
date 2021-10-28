import scrapy
from scrapy.spiders.init import InitSpider
from datetime import datetime


base = "https://github.com"
min_stars = 0
min_datatime = datetime.strptime("2018-01-01", '%Y-%m-%d')

class RepoSpider(InitSpider):
    name = 'repo'
    login_url = base + '/session'
    start_urls = [base + '/search?q=resource+extension%3Atf&type=Code']

    def init_request(self):
        return scrapy.Request(url=self.login_url, callback=self.login)

    def login(self, response):
        yield scrapy.FormRequest.from_response(
         response,
         url=self.login_url,
         method="POST",
         formdata={
            'login':'giovanniquattrocchi@me.com',
            'password':'o392oo47o7'
         },
         callback=self.initialized)

    def parse(self, response):
        for repo in response.css('.flex-auto.min-width-0.col-10'):
            url = repo.css('a.text-bold::attr("href")').get()
            dt = repo.css('.updated-at relative-time::attr("datetime")').get()
            dt = datetime.strptime(dt[:10], '%Y-%m-%d')
            if dt >= min_datatime:
                path = repo.css('a[title]::attr("href")').get()
                path = "/".join(path.split("/")[5:])
                print(path)
                yield scrapy.Request(base+url, callback=self.analyze_repo(base+url, path))

        next = response.css('.next_page::attr("href")').get()
        if next 

    def analyze_repo(self, repo, path):
        def _analyze_repo(response):
            stars = int(response.css('.social-count.js-social-count::text').get())
            if stars >= min_stars:
                yield {'repo' : repo, 'file' : path, 'stars' : stars }
        return _analyze_repo

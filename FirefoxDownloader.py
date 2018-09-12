from GithubDriversDownloader import GithubDriversDownloader 


class FirefoxDownloader(GithubDriversDownloader):


    url = "https://github.com/mozilla/geckodriver/releases{0}"

    name =  "geckodriver"
    browser = 'firefox'


    def __init__(self):
        super().__init__()


    def getVersions(self):
        return super().getVersions(self.url)


    def download(self, version = None):
        return super().download(self.browser, self.name, version)

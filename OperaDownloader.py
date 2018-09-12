from GithubDriversDownloader import GithubDriversDownloader 


class OperaDownloader(GithubDriversDownloader):


    url = "https://github.com/operasoftware/operachromiumdriver/releases{0}"

    name =  "operadriver"
    browser = 'opera'


    def __init__(self):
        super().__init__()


    def getVersions(self):
        return super().getVersions(self.url)


    def download(self, version = None):
        return super().download(self.browser, self.name, version)

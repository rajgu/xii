import re
from DriversDownloader import DriversDownloader 


class EdgeDownloader(DriversDownloader):


    url = "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
    linkRegex = '<li class=\"driver-download\"><a.*?href=\"(.*?)\".*?>Release (\d+).*?Version: ([\d\.]+).*?Edge version supported: ([\d\.]+)'
    destination =  "MicrosoftWebDriver.exe"
    versions = None
    links = None


    def __init__(self):
        super().__init__()


    def getVersions(self):
        if self.versions:
            return self.versions

        site = super().getSite(self.url)
        links = self.parseSite(site)

        self.links = links
        self.versions = sorted(list(links.keys())) 
        return self.versions


    def download(self, version = None):
        if not self.versions:
            self.getVersions()
        if not version:
            version = self.versions[-1]
        if version not in self.versions:
            raise Exception("Version: '{0}' of edge is not available: '{1}'".format(version, self.versions))
        system = super().getSystem()
        if system not in super().getAvailableSystems('edge'):
            raise Exception("Browser: {0} is not available for system: {1}".format('Edge', system))

        print("Downloading version: '{0}' for system: {1}".format(version, system))

        link = self.links[version]
        super().getFile(link, self.destination)
        return True


    def parseSite(self, site):
        result = re.findall(self.linkRegex, site, re.M|re.S)
        versions = dict(map(lambda x: (x[2], x[0]), result))
        return versions 

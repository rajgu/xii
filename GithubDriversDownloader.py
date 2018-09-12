from DriversDownloader import DriversDownloader
import re


class GithubDriversDownloader(DriversDownloader):


    linkRegex = '<a href=\"(.*?releases/download/([A-Za-z0-9\.\-\_]+)\/.*?(.zip|.tar.gz))\"'
    githubUrl = 'https://github.com/{0}'


    def __init__(self):
        self.versions = []
        self.links = []
        super().__init__()


    def download(self, browser, name, version = None):
        if not self.versions:
            self.getVersions()
        if not version:
            version = self.versions[0]
        if version not in self.versions:
            raise Exception("Version: '{0}' of {1} is not available: '{2}'".format(version, browser, self.versions))
        system = super().getSystem()
        if system not in super().getAvailableSystems(browser):
            raise Exception("Browser: {0} is not available for system: {1}".format(browser, system))

        print("Downloading {0} version: '{1}' for system: {2}".format(browser, version, system))

        file = None
        if super().is64bit():
            file = [x for x in self.links if version in x and system in x and '64' in x]
        if not file:
            file = [x for x in self.links if version in x and system in x and '32' in x]

        link = self.githubUrl.format(file[0])
        super().getFile(link, name)
        return True



    def getVersions(self, url):
        oldestVersion = ""
        while True:
            link = url.format("?after=" + oldestVersion)
            print(link)
            site = super().getSite(link)
            versions, links = self.parseSite(site)
            if not versions:
                break
            self.versions += versions
            self.links += links
            oldestVersion = versions[-1]

        return self.versions


    def parseSite(self, site):
        versions = []
        links = []
        result = re.findall(self.linkRegex, site, re.M)

        if not result:
            return None, None

        for item in result:
            if item[1] not in versions:
                versions.append(item[1])
            links.append(item[0])

        return versions, links

import re
from DriversDownloader import DriversDownloader


class ChromeDownloader(DriversDownloader):

    fileParseReg = "<Contents><Key>(.*?)</Key><Generation>(.*?)</Generation><MetaGeneration>(.*?)</MetaGeneration><LastModified>(.*?)</LastModified><ETag>\"(.*?)\"</ETag><Size>(.*?)</Size></Contents>"
    dirsParseReg = "<CommonPrefixes><Prefix>(.*?)</Prefix></CommonPrefixes>"
    url =          "https://chromedriver.storage.googleapis.com/?delimiter=/&prefix="
    link =         "https://chromedriver.storage.googleapis.com/{0}"
    versions =     []
    destination =  "chromedriver"

    def __init__(self):
        super().__init__()


    def getDestination(self):
        return self.destination


    def getVersions(self):
        if len(self.versions) == 0:
            site = str(super().getSite(self.url))
            null, dirs = self.parseSite(site)
            for i in dirs:
                if re.match('^[0-9\.]+$', i):
                    self.versions.append(i)
        return self.versions


    def download(self, version = None):
        if not self.versions:
            self.getVersions()
        if not version:
            version = self.versions[-1]
        if version not in self.versions:
            raise Exception("Version: '{0}' of chromedriver is not available: '{1}'".format(version, self.versions))
        system = super().getSystem()
        if system not in super().getAvailableSystems('chrome'):
            raise Exception("Browser: {0} is not available for system: {1}".format('chrome', system))

        print("Downloading version: '{0}' for system: {1}".format(version, system))

        site = str(super().getSite(self.url + version + '/'))
        files, null = self.parseSite(site)


        file = None
        if super().is64bit():
            file = [x for x in files if system in x['name'] and '64' in x['name']]
        if not file:
            file = [x for x in files if system in x['name'] and '32' in x['name']]

        link = self.link.format(file[0]['name'])

        if super().getFile(link, self.destination):
            return self.destination
        else:
            raise Exception("Could not download: {0} to: {1}".format(link, self.destination))


    def parseSite(self, site):
        files = re.findall(self.fileParseReg, site, re.M|re.S)
        dirs  = re.findall(self.dirsParseReg, site, re.M|re.S)
        files = list(map(lambda x: {'name': x[0], 'lastModified':x[3],'size':x[5]}, files))
        dirs  = list(map(lambda x: x.split('/')[0], dirs))
        return files, dirs

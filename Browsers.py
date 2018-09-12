import os
from selenium import webdriver
from selenium.webdriver.chrome import service
from ChromeDownloader import ChromeDownloader
from EdgeDownloader import EdgeDownloader
from FirefoxDownloader import FirefoxDownloader
from OperaDownloader import OperaDownloader


class Browser:


    driversLocation = 'drivers/'
    driversNames = {
        'chrome': 'chromedriver',
        'edge': 'MicrosoftWebDriver.exe',
        'opera': 'operadriver',
        'firefox': 'geckodriver',
    }


    def __init__(self):
        os.environ["PATH"] += os.pathsep + self.getDriversLocation()


    def verifyBinary(self, browser):
        if os.path.isfile('{0}/{1}'.format(self.getDriversLocation(), self.driversNames[browser])):
            return True
        return False


    def getDriversLocation(self):
        return os.path.dirname('{0}/{1}'.format(os.getcwd(), self.driversLocation))


    def getDriverName(self, name):
        return self.driversNames[name]



class ChromeBrowser(Browser):

    browser = 'chrome'

    def __init__(self):
        super().__init__()
        if not super().verifyBinary(self.browser):
            self.downloader = ChromeDownloader()
            self.availableVersions = self.downloader.getVersions()
            print("Available versions: {0}".format(self.availableVersions))
            self.downloader.download()
        self.webdriver = webdriver.Chrome('{0}/{1}'.format(super().getDriversLocation(), super().getDriverName(self.browser)))


class FirefoxBrowser(Browser):

    browser = 'firefox'

    def __init__(self):
        super().__init__()
        if not super().verifyBinary(self.browser):
            self.downloader = FirefoxDownloader()
            self.availableVersions = self.downloader.getVersions()
            print("Available versions: {0}".format(self.availableVersions))
            self.downloader.download()
        self.webdriver = webdriver.Firefox()


class EdgeBrowser(Browser):

    browser = 'edge'

    def __init__(self):
        super().__init__()
        if not super().verifyBinary(self.browser):
            self.downloader = EdgeDownloader()
            self.availableVersions = self.downloader.getVersions()
            print("Available versions: {0}".format(self.availableVersions))
            self.downloader.download()
        self.webdriver = webdriver.Edge()


class SafariBrowser(Browser):

    browser = 'safari'

    def __init__(self):
        super().__init__()
        try:
            self.driver = webdriver.Safari()
        except:
            print("No Safari browser installed on machine")
            return None



class OperaBrowser(Browser):

    browser = 'opera'

    def __init__(self):
        super().__init__()
        if not super().verifyBinary(self.browser):
            self.downloader = OperaDownloader()
            self.availableVersions = self.downloader.getVersions()
            print("Available versions: {0}".format(self.availableVersions))
            self.downloader.download()

        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/opera"
        self.webdriver = webdriver.Opera(options=options)

import hashlib
import os
import platform
import requests
import shutil
import stat
import sys
import tarfile
import zipfile


class DriversDownloader:

    systems = {
        'Linux':   'linux',
        'Darwin':  'macos',
        'Windows': 'windows',
    }

    availableSystems = {
        'chrome': ['linux', 'windows', 'macos'],
        'firefox': ['linux', 'windows', 'macos'],
        'edge': ['linux', 'windows'],
        'safari': ['windows', 'macos'],
        'opera': ['linux', 'windows', 'macos'],
    }

    downloadDirectory = 'drivers/'
    tmpDirectory = 'tmp/'

    def __init__(self):
        system = platform.system()
        if system not in self.systems.keys():
            raise Exception("System: {0} is uknown".format(system))
        self.system = self.systems[system]


    def is64bit(self):
        return sys.maxsize > 2**32


    def getAvailableSystems(self, browserName):
        if browserName not in self.availableSystems:
            raise Exception("Browser: {0} is not supported".format(browserName))
        return self.availableSystems[browserName]


    def getSystem(self):
        return self.system


    def getSite(self, url):
        response = requests.get(url)
        if not response:
            raise Exception("Error while downloading: {0}".format(url))

        if response.status_code != 200:
            raise Exception("Error while downloading: {0}, response_code: {1}".format(url, response.status_code))
        return response.text


    def getFile(self, url, file):
        fname = '{0}/{1}'.format(self.tmpDirectory, url.split('/')[-1])
        with open(fname, "wb") as f:
                print("Downloading: {0}".format(url))
                response = requests.get(url, stream=True)
                fsize = response.headers.get('content-length')

                if fsize is None:
                    f.write(response.content)
                else:
                    dl = 0
                    fsize = int(fsize)
                    for data in response.iter_content(chunk_size=65536):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / fsize)
                        sys.stdout.write("\r[{0}{1}]".format('=' * done, ' ' * (50-done)))    
                        sys.stdout.flush()

        print("\ndone")

        if zipfile.is_zipfile(fname):
            zip_ref = zipfile.ZipFile(fname, 'r')
            zip_ref.extractall(self.downloadDirectory)
            for name in zip_ref.namelist():
                if name.endswith('/'):
                    from_file = "{0}/{1}/{2}".format(self.downloadDirectory, name, file)
                    to_file = "{0}/{1}".format(self.downloadDirectory, file)
                    os.rename(from_file, to_file)
                    shutil.rmtree("{0}/{1}".format(self.downloadDirectory, name), ignore_errors=True)
                    break
            zip_ref.close()
        elif fname.endswith('.tar.gz'):
            tar = tarfile.open  (fname, "r:gz")
            tar.extractall(path=self.downloadDirectory)
        elif fname.endswith('.exe'):
            os.rename(fname, "{0}/{1}".format(self.downloadDirectory, fname.split('/')[-1]))
        else:
            raise Exception("Could not determine file type")

        fullPath = "{0}/{1}".format(self.downloadDirectory, file)

        if not os.path.isfile(fullPath):
            raise Exception("File: {0} does not exists".format(fullPath))

        if os.path.isfile(fname):
            os.remove(fname)

        st = os.stat(fullPath)
        os.chmod(fullPath, st.st_mode | stat.S_IEXEC)

        return True

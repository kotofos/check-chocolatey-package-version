import xml.etree.ElementTree as ET
import zipfile
from io import BytesIO
from urllib.request import urlretrieve, urlopen

driver_url_map = {
    'nvidia': 'https://chocolatey.org/api/v2/package/nvidia-display-driver',
    'intel': 'https://chocolatey.org/api/v2/package/intel-graphics-driver',
}


def download(url):
    f = BytesIO()
    response = urlopen(url)
    f.write(response.read())
    return f


def get_current_version(name):
    url = driver_url_map[name]
    archive = download(url)
    zip = zipfile.ZipFile(archive)

    string = zip.read(url.rpartition('/')[-1] + '.nuspec').decode()
    string = "\n".join(string.split("\r\n"))
    root = ET.fromstring(string)

    tag_name = ('{http://schemas.microsoft.com/packaging/2011/08/nuspec.xsd}'
                'version')
    for elem in root.iter():
        if elem.tag == tag_name:
            return elem.text


if __name__ == '__main__':
    for name in ('nvidia', 'intel'):
        res = get_current_version(name)
        print('version for', name, res)

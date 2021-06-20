#!/usr/bin/env python3
import os
import json
import requests as req


## Utils
def parse_url(url):
    # Remove GET params
    url1 = url.split('?', 1)
    # Parse path
    url2 = url1[0].split('/')
    # Restore GET params
    url2[-1] += '?' + url1[-1]
    return url2


def deparse_url(url_list):
    url = ''
    for item in url_list:
        url += item + '/'
    return url[:-1]


## Classes
class Channel:
    """
    Abstraction for a generic channel.
    """
    def __init__(self):
        self.chUrl = None
        self.name = None

    def getChUrl(self):
        return self.chUrl

    def getName(self):
        return self.name


class RaiChannel(Channel):
    """
    Abstraction for a Rai channel.
    """
    def __init__(self, id):
        """
        Initialize the Rai streaming channel and load playlist.

        Arguments:
            id (string) : identifier of the channel (e.g. 'rai1')
        """
        super().__init__()
        self.jsonUrl = 'https://www.raiplay.it/dirette/{}.json'.format(id)

        # Get channel JSON
        jsonReq = req.get(self.jsonUrl)
        if not jsonReq.ok:
            raise Exception('connection error {}'.format(jsonReq.status_code))
        self.chJson = json.loads(jsonReq.text)

        # Get playlists URL
        if 'video' not in self.chJson.keys():
            raise Exception('Cannot retrieve channel M3U!')
        elif 'content_url' not in self.chJson['video'].keys():
            raise Exception('Cannot retrieve channel M3U!')
        self.chUrl = self.chJson['video']['content_url']

        # Get name
        if 'channel' not in self.chJson.keys():
            raise Exception('Cannot retrieve channel name!')
        self.name = self.chJson['channel']


class M3U:
    def __init__(self, filepath, logos_url=None):
        self.filepath = filepath
        if os.path.isdir(self.filepath):
            raise IsADirectoryError("'{}' exists and is a directory.".format(self.filepath))
        self.logos_url = logos_url
        self.channels = []

    def addChannel(self, channel):
        self.channels.append(channel)

    def dump(self):
        with open(self.filepath, 'w+') as f:
            f.write('#EXTM3U\n')
            if self.logos_url is not None:
                for channel in self.channels:
                    lines = ['#EXTINF: -1 tvg-logo="{0}/{1}.png", {1}\n'.format(self.logos_url, channel.getName()),
                             str(channel.getChUrl())+'\n']
                    f.writelines(lines)
            else:
                for channel in self.channels:
                    lines = ['#EXTINF: -1, {}\n'.format(channel.getName()),
                             str(channel.getChUrl())+'\n']
                    f.writelines(lines)


## Channels
# Rai Channels
rai1 = RaiChannel('rai1')
rai2 = RaiChannel('rai2')
rai3 = RaiChannel('rai3')
rai4 = RaiChannel('rai4')
rai5 = RaiChannel('rai5')
raimovie = RaiChannel('raimovie')
raipremium = RaiChannel('raipremium')
raistoria = RaiChannel('raistoria')
raiyoyo = RaiChannel('raiyoyo')
raigulp = RaiChannel('raigulp')
rainews24 = RaiChannel('rainews24')
raisportpiuhd = RaiChannel('raisportpiuhd')
raisport = RaiChannel('raisport')
raiscuola = RaiChannel('raiscuola')
rairadio2 = RaiChannel('rairadio2')


if __name__ == '__main__':
    m3u = M3U('iptv-italy.m3u')
    m3u.addChannel(rai1)
    m3u.addChannel(rai2)
    m3u.addChannel(rai3)
    m3u.addChannel(rai4)
    m3u.addChannel(rai5)
    m3u.addChannel(raimovie)
    m3u.addChannel(raipremium)
    m3u.addChannel(raistoria)
    m3u.addChannel(raiyoyo)
    m3u.addChannel(raigulp)
    m3u.addChannel(rainews24)
    m3u.addChannel(raisportpiuhd)
    m3u.addChannel(raisport)
    m3u.addChannel(raiscuola)
    m3u.addChannel(rairadio2)
    m3u.dump()
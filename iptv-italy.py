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


class MediasetChannel(Channel):
    """
    Abstraction for a Mediaset channel.
    """
    def __init__(self, id, name):
        """
        Initialize the Mediaset streaming channel and load playlist.

        Arguments:
            id (string) : identifier of the channel (e.g. 'C5')
        """
        super().__init__()
        self.name = name
        self.jsonUrl = 'https://static3.mediasetplay.mediaset.it/apigw/nownext/{}.json'.format(id)

        # Get channel JSON
        jsonReq = req.get(self.jsonUrl)
        if not jsonReq.ok:
            raise Exception('connection error {}'.format(jsonReq.status_code))
        self.chJson = json.loads(jsonReq.text)

        # Get playlists URL
        if 'response' not in self.chJson.keys():
            raise Exception('Cannot retrieve channel M3U!')
        elif 'tuningInstruction' not in self.chJson['response'].keys():
            raise Exception('Cannot retrieve channel M3U!')
        elif 'urn:theplatform:tv:location:any' not in self.chJson['response']['tuningInstruction'].keys():
            raise Exception('Cannot retrieve channel M3U!')
        tuning_data = self.chJson['response']['tuningInstruction']['urn:theplatform:tv:location:any']
        for tuning_datum in tuning_data:
            if tuning_datum['format'] == 'application/x-mpegURL':
                self.chUrl = tuning_datum['publicUrls'][0]
                break
        else:
            raise Exception('Cannot retrieve channel M3U!')


class ParamountChannel(Channel):
    """
    Abstraction for a Paramount channel.
    """
    def __init__(self):
        """
        Initialize the Paramount streaming channel and load playlist.
        """
        super().__init__()
        self.name = 'Paramount Channel'
        self.chUrl = 'http://viacomitalytest-lh.akamaihd.net/i/sbshdlive_1@195657/master.m3u8'


class La7(Channel):
    """
    Abstraction for a La7 channel.
    """
    def __init__(self):
        """
        Initialize the La7 streaming channel and load playlist.
        """
        super().__init__()
        self.name = 'La7'
        self.chUrl = 'https://d15umi5iaezxgx.cloudfront.net/LA7/DRM/HLS/Live.m3u8'


class La7d(Channel):
    """
    Abstraction for a La7d channel.
    """
    def __init__(self):
        """
        Initialize the La7d streaming channel and load playlist.
        """
        super().__init__()
        self.name = 'La7d'
        self.chUrl = 'https://d15umi5iaezxgx.cloudfront.net/LA7D/DRM/HLS/Live.m3u8'


class M3U:
    """
    Creates a M3U playlist with all the required channels.
    """
    def __init__(self, filepath, logos_url=None):
        """
        Arguments:
            filepath (string) : path of the M3U file to dump
            logos_url (string): URL of the directory containing all
                                the channels logos (optional)
        """
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

# Mediaset Channels
rete4 = MediasetChannel('R4', 'Rete 4')
canale5 = MediasetChannel('C5', 'Canale 5')
italia1 = MediasetChannel('I1', 'Italia 1')
canale20 = MediasetChannel('LB', 'Canale 20')
la5 = MediasetChannel('KA', 'La5')
italia2 = MediasetChannel('I2', 'Italia 2')
cine34 = MediasetChannel('B6', 'Cine 34')
medextra = MediasetChannel('KQ', 'Mediaset Extra')
focus = MediasetChannel('FU', 'Focus')
topcrime = MediasetChannel('LT', 'Top Crime')
iris = MediasetChannel('KI', 'Iris')
boing = MediasetChannel('KB', 'Boing')
cartoonito = MediasetChannel('LA', 'Cartoonito')
tgcom24 = MediasetChannel('KF', 'TGcom24')
radio105 = MediasetChannel('EC', 'Radio 105')
radio101 = MediasetChannel('ER', 'Radio 101')
virginradio = MediasetChannel('EW', 'Virgin Radio')
radiomontecarlo = MediasetChannel('BB', 'Radio Monte Carlo')


# La7
la7 = La7()
la7d = La7d()


# Paramount Channel
paramount = ParamountChannel()


if __name__ == '__main__':
    m3u = M3U('iptv-italy.m3u')
    m3u.addChannel(rai1)
    m3u.addChannel(rai2)
    m3u.addChannel(rai3)
    m3u.addChannel(rete4)
    m3u.addChannel(canale5)
    m3u.addChannel(italia1)
    #m3u.addChannel(la7)
    m3u.addChannel(rai4)
    m3u.addChannel(rai5)
    m3u.addChannel(raimovie)
    m3u.addChannel(la5)
    m3u.addChannel(italia2)
    m3u.addChannel(topcrime)
    m3u.addChannel(iris)
    m3u.addChannel(focus)
    m3u.addChannel(medextra)
    m3u.addChannel(canale20)
    m3u.addChannel(raipremium)
    m3u.addChannel(raistoria)
    m3u.addChannel(raiyoyo)
    m3u.addChannel(raigulp)
    m3u.addChannel(boing)
    m3u.addChannel(cartoonito)
    m3u.addChannel(cine34)
    m3u.addChannel(paramount)
    #m3u.addChannel(la7d)
    m3u.addChannel(rainews24)
    m3u.addChannel(tgcom24)
    m3u.addChannel(raisportpiuhd)
    m3u.addChannel(raisport)
    m3u.addChannel(raiscuola)
    m3u.addChannel(rairadio2)
    m3u.addChannel(radio101)
    m3u.addChannel(radio105)
    m3u.addChannel(virginradio)
    m3u.addChannel(radiomontecarlo)
    m3u.dump()
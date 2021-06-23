#!/usr/bin/env python3
import os
import json
import requests as req


WEBPATH = 'https://jurijnota.github.io/iptv-italy'


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
        """
        Init class attributes.
        """
        self.chUrl = None
        self.name = None
        self.id = None
        self.number = None
        self.logo = None
        self.lines = []
    
    def M3ULines(self):
        """
        Return the lines to write in the M3U file.
        """
        self.lines.append('#EXTINF: -1 ')
        if self.number is not None:
            self.lines.append('channel-number="{}" '.format(self.number))
        if self.logo is not None:
            self.lines.append('tvg-logo="{}" '.format(self.logo))
        if self.id is not None:
            self.lines.append('tvg-id="{}" '.format(self.id))
        elif self.name is not None:
            self.lines.append('tvg-id="{}" '.format(''.join(c.lower() for c in self.name if not c.isspace())))
        if self.name is not None:            
            self.lines.append('tvg-name="{}" '.format(self.name))
            self.lines.append(', {}'.format(self.name))
        self.lines.append('\n')
        self.lines.append(self.chUrl)
        self.lines.append('\n')
        return self.lines


class RaiChannel(Channel):
    """
    Abstraction for a Rai channel.
    """

    NAME_ID = {
        'Rai 1': 'rai1',
        'Rai 2': 'rai2',
        'Rai 3': 'rai3',
        'Rai 4': 'rai4',
        'Rai 5': 'rai5',
        'Rai Movie': 'raimovie',
        'Rai Premium': 'raipremium',
        'Rai Storia': 'raistoria',
        'Rai Yoyo': 'raiyoyo',
        'Rai Gulp': 'raigulp',
        'Rai News 24': 'rainews24',
        'Rai Sport Piu HD': 'raisportpiuhd',
        'Rai Sport': 'raisport',
        'Rai Scuola': 'raiscuola',
        'Rai Radio 2': 'rairadio2'
    }

    def __init__(self, name, number=None):
        """
        Initialize the Rai streaming channel and load playlist.

        Arguments:
            name (string): name of the channel (e.g. 'Rai 1')
            number (int) : number of the channel (e.g. 1)
        """
        super().__init__()
        self.name = name
        self.id = self.NAME_ID[self.name]
        self.number = number
        self.logo = WEBPATH + '/logos/{}.png'.format(self.id)

        # Get playlists URL
        jsonUrl = 'https://www.raiplay.it/dirette/{}.json'.format(self.id)
        jsonReq = req.get(jsonUrl)
        if not jsonReq.ok:
            raise Exception('connection error {}'.format(jsonReq.status_code))
        chJson = json.loads(jsonReq.text)
        if 'video' not in chJson.keys():
            raise Exception('Cannot retrieve channel M3U!')
        elif 'content_url' not in chJson['video'].keys():
            raise Exception('Cannot retrieve channel M3U!')
        self.chUrl = chJson['video']['content_url']

    def M3ULines(self):
        """
        This updated parser solves the issue that prevent Rai channels
        from being played on VLC.
        """
        self.lines.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0\n')
        return super().M3ULines()


class MediasetChannel(Channel):
    """
    Abstraction for a Mediaset channel.
    """

    NAME_ID = {
        'Rete 4': 'r4',
        'Canale 5': 'c5',
        'Italia 1': 'i1',
        'Canale 20': 'lb',
        'La5': 'ka',
        'Italia 2': 'i2',
        'Cine 34': 'b6',
        'Mediaset Extra': 'kq',
        'Focus': 'fu',
        'Top Crime': 'lt',
        'Iris': 'ki',
        'Boing': 'kb',
        'Cartoonito': 'la',
        'TGcom24': 'kf',
        'Radio 105': 'ec',
        'Radio 101': 'er',
        'Virgin Radio': 'ew',
        'Radio Monte Carlo': 'bb'
    }

    def __init__(self, name, number=None):
        """
        Initialize the Mediaset streaming channel and load playlist.

        Arguments:
            name (string): name of the channel (e.g. 'Canale 5')
            number (int) : number of the channel (e.g. 5)
        """
        super().__init__()
        self.name = name
        self.id = self.NAME_ID[self.name]
        self.number = number
        self.chUrl = 'https://live3-mediaset-it.akamaized.net/Content/hls_h0_clr_vos/live/channel({})/index.m3u8'.format(self.id)
        self.logo = WEBPATH + '/logos/{}.png'.format(self.id)


class ParamountChannel(Channel):
    """
    Abstraction for a Paramount channel.
    """
    def __init__(self, number=None):
        """
        Initialize the Paramount streaming channel and load playlist.

        Arguments:
            number (int): number of the channel
        """
        super().__init__()
        self.name = 'Paramount Channel'
        self.number = number
        self.chUrl = 'http://viacomitalytest-lh.akamaihd.net/i/sbshdlive_1@195657/master.m3u8'


class La7(Channel):
    """
    Abstraction for a La7 channel.
    """
    def __init__(self, number=None):
        """
        Initialize the La7 streaming channel and load playlist.

        Arguments:
            number (int): number of the channel
        """
        super().__init__()
        self.name = 'La7'
        self.number = number
        self.chUrl = 'https://d15umi5iaezxgx.cloudfront.net/LA7/DRM/HLS/Live.m3u8'


class La7d(Channel):
    """
    Abstraction for a La7d channel.
    """
    def __init__(self, number=None):
        """
        Initialize the La7d streaming channel and load playlist.

        Arguments:
            number (int): number of the channel
        """
        super().__init__()
        self.name = 'La7d'
        self.number = number
        self.chUrl = 'https://d15umi5iaezxgx.cloudfront.net/LA7D/DRM/HLS/Live.m3u8'


class M3U:
    """
    Creates a M3U playlist with all the required channels.
    """
    def __init__(self, filepath):
        """
        Arguments:
            filepath (string) : path of the M3U file to dump
            logos_url (string): URL of the directory containing all
                                the channels logos (optional)
        """
        self.filepath = filepath
        if os.path.isdir(self.filepath):
            raise IsADirectoryError("'{}' exists and is a directory.".format(self.filepath))
        self.channels = []

    def addChannel(self, channel, number=None):
        """
        Add channel to M3U playlist

        Arguments:
            channel     : the channel to add
            number (int): the channel number (optional)
        """
        if number is not None:
            channel.number = number
        else:
            if channel.number is None:
                channel.number = len(self.channels) + 1
            self.channels.append(channel)

    def dump(self):
        with open(self.filepath, 'w+') as f:
            f.write('#EXTM3U\n')
            for channel in self.channels:
                f.writelines(channel.M3ULines())


## Channels
# Rai Channels
rai1 = RaiChannel('Rai 1', 1)
rai2 = RaiChannel('Rai 2', 2)
rai3 = RaiChannel('Rai 3', 3)
rai4 = RaiChannel('Rai 4')
rai5 = RaiChannel('Rai 5')
raimovie = RaiChannel('Rai Movie')
raipremium = RaiChannel('Rai Premium')
raistoria = RaiChannel('Rai Storia')
raiyoyo = RaiChannel('Rai Yoyo')
raigulp = RaiChannel('Rai Gulp')
rainews24 = RaiChannel('Rai News 24')
raisportpiuhd = RaiChannel('Rai Sport Piu HD')
raisport = RaiChannel('Rai Sport')
raiscuola = RaiChannel('Rai Scuola')
rairadio2 = RaiChannel('Rai Radio 2')

# Mediaset Channels
rete4 = MediasetChannel('Rete 4', 4)
canale5 = MediasetChannel('Canale 5', 5)
italia1 = MediasetChannel('Italia 1', 6)
canale20 = MediasetChannel('Canale 20')
la5 = MediasetChannel('La5')
italia2 = MediasetChannel('Italia 2')
cine34 = MediasetChannel('Cine 34')
medextra = MediasetChannel('Mediaset Extra')
focus = MediasetChannel('Focus')
topcrime = MediasetChannel('Top Crime')
iris = MediasetChannel('Iris')
boing = MediasetChannel('Boing')
cartoonito = MediasetChannel('Cartoonito')
tgcom24 = MediasetChannel('TGcom24')
radio105 = MediasetChannel('Radio 105')
radio101 = MediasetChannel('Radio 101')
virginradio = MediasetChannel('Virgin Radio')
radiomontecarlo = MediasetChannel('Radio Monte Carlo')

# La7
la7 = La7()
la7d = La7d()

# Paramount Channel
paramount = ParamountChannel()


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    m3u = M3U('{}/iptv-italy.m3u'.format(script_dir))
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
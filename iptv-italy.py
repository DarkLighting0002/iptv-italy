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
            self.lines.append('tvg-chno="{}" '.format(self.number))
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

    CHANNELS = {
        'Rai 1': {'id': 'rai1', 'number': 1},
        'Rai 2': {'id': 'rai2', 'number': 2},
        'Rai 3': {'id': 'rai3', 'number': 3},
        'Rai 4': {'id': 'rai4', 'number': 21},
        'Rai 5': {'id': 'rai5', 'number': 23},
        'Rai Movie': {'id': 'raimovie', 'number': 24},
        'Rai Premium': {'id': 'raipremium', 'number': 25},
        'Rai Storia': {'id': 'raistoria', 'number': 54},
        'Rai Yoyo': {'id': 'raiyoyo', 'number': 43},
        'Rai Gulp': {'id': 'raigulp', 'number': 42},
        'Rai News 24': {'id': 'rainews24', 'number': 48},
        'Rai Sport Piu HD': {'id': 'raisportpiuhd', 'number': 57},
        'Rai Sport': {'id': 'raisport', 'number': 58},
        'Rai Scuola': {'id': 'raiscuola', 'number': 146},
        'Rai Radio 2': {'id': 'rairadio2', 'number': 156}
    }

    def __init__(self, name, id=None, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the Rai streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            id (string)     : id of the channel (e.g. 'rai1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        if id is not None:
            self.id = id
        else:
            self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)

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

    CHANNELS = {
        'Rete 4': {'id': 'r4', 'number': 4},
        'Canale 5': {'id': 'c5', 'number': 5},
        'Italia 1': {'id': 'i1', 'number': 6},
        '20': {'id': 'lb', 'number': 20},
        'La5': {'id': 'ka', 'number': 30},
        'Italia 2': {'id': 'i2', 'number': 66},
        'Cine34': {'id': 'b6', 'number': 34},
        'Mediaset Extra': {'id':'kq', 'number': 55},
        'Focus': {'id': 'fu', 'number': 35},
        'Top Crime': {'id': 'lt', 'number': 39},
        'Iris': {'id': 'ki', 'number': 22},
        'Boing': {'id': 'kb', 'number': 40},
        'Cartoonito': {'id': 'la', 'number': 46},
        'TGcom24': {'id': 'kf', 'number': 51},
        'Radio 105': {'id': 'ec', 'number': 157},
        'Radio 101': {'id': 'er', 'number': 167},
        'Virgin Radio': {'id': 'ew', 'number': 257},
        'Radio Monte Carlo': {'id': 'bb', 'number': 772}
    }

    def __init__(self, name, id=None, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the Mediaset streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            id (string)     : id of the channel (e.g. 'rai1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        if id is not None:
            self.id = id
        else:
            self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'https://live3-mediaset-it.akamaized.net/Content/hls_h0_clr_vos/live/channel({})/index.m3u8'.format(self.id)


class ParamountNetwork(Channel):
    """
    Abstraction for the Paramount Network.
    """
    def __init__(self, id='paramountchannel', number=27, logo=WEBPATH + '/logos'):
        """
        Initialize the Paramount streaming channel and load playlist.

        Arguments:
            id (string)     : id of the channel (e.g. 'rai1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        self.name = 'Paramount Network'
        self.id = id
        self.number = number
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'http://viacomitalytest-lh.akamaihd.net/i/sbshdlive_1@195657/master.m3u8'


class La7(Channel):
    """
    Abstraction for a La7 channel.
    """

    CHANNELS = {
        'La7': {'id': 'LA7', 'number': 7},
        'La7d': {'id': 'LA7D', 'number': 29}
    }

    def __init__(self, name, id=None, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the La7 streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            id (string)     : id of the channel (e.g. 'rai1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        if id is not None:
            self.id = id
        else:
            self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'https://d15umi5iaezxgx.cloudfront.net/{}/DRM/HLS/Live.m3u8'.format(self.id)      


class Cielo(Channel):
    """
    Abstraction for Cielo channel.
    """
    def __init__(self):
        """
        
        """
        super().__init__()


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
        self.channels.append(channel)

    def dump(self):
        with open(self.filepath, 'w+') as f:
            f.write('#EXTM3U\n')
            for channel in self.channels:
                f.writelines(channel.M3ULines())


if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.realpath(__file__))
    m3u = M3U('{}/iptv-italy.m3u'.format(script_dir))

    # Add Rai channels
    for ch_name in RaiChannel.CHANNELS.keys():
        m3u.addChannel(RaiChannel(ch_name))

    # Add Mediaset channels
    for ch_name in MediasetChannel.CHANNELS.keys():
        m3u.addChannel(MediasetChannel(ch_name))

    # Add Paramount channel
    m3u.addChannel(ParamountNetwork())

    m3u.dump()
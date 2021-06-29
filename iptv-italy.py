#!/usr/bin/env python3
import os
import json
import requests as req


WEBPATH = 'https://jurijnota.github.io/iptv-italy'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

with open('{}/channels.json'.format(SCRIPT_DIR), 'r') as f:
    CHANNELS = json.load(f)


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


class Rai(Channel):
    """
    Abstraction for a Rai channel.
    """

    CHANNELS = CHANNELS['Rai']

    def __init__(self, name, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the Rai streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
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


class TGR(Channel):
    """
    Abstraction for a TGR channel.
    """

    CHANNELS = CHANNELS['TGR']

    def __init__(self, name, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the Rai streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/tgr.png'

        # Get playlists URL
        self.chUrl = 'https://mediapolis.rai.it/relinker/relinkerServlet.htm?cont={}'.format(self.id)


class Mediaset(Channel):
    """
    Abstraction for a Mediaset channel.
    """

    CHANNELS = CHANNELS['Mediaset']

    def __init__(self, name, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the Mediaset streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'https://live3-mediaset-it.akamaized.net/Content/hls_h0_clr_vos/live/channel({})/index.m3u8'.format(self.id)


class Paramount(Channel):
    """
    Abstraction for the Paramount channel.
    """

    CHANNELS = CHANNELS['Paramount']

    def __init__(self, name, number=27, logo=WEBPATH + '/logos'):
        """
        Initialize the Paramount streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'http://127.0.0.1:10293/?id={}'.format(self.id)


class Sky(Channel):
    """
    Abstraction for Sky channels.
    """

    CHANNELS = CHANNELS['Sky']

    def __init__(self, name, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the Cielo streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'http://127.0.0.1:10293/?id={}'.format(self.id)


class Norba(Channel):
    """
    Abstraction for Norba channels.
    """

    CHANNELS = CHANNELS['Norba']

    def __init__(self, name, number=None, logo=WEBPATH + '/logos'):
        """
        Initialize the Cielo streaming channel and load playlist.

        Arguments:
            name (string)   : name of the channel (e.g. 'Rai 1')
            number (int)    : number of the channel (e.g. 1)
            webpath (string): path to the logos directory (the name of the logo
                              is by default set to '<id>.png')
        """
        super().__init__()
        if name in self.CHANNELS.keys():
            self.name = name
        else:
            raise Exception('channel {} does not exist!'.format(name))
        self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'https://flash5.xdevel.com/tgnorba_24/smil:tgnorba_24.smil/playlist.m3u8'


class La7(Channel):
    """
    Abstraction for a La7 channel.
    """

    CHANNELS = CHANNELS['La7']

    def __init__(self, name, number=None, logo=WEBPATH + '/logos'):
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
        self.id = self.CHANNELS[self.name].get('id')
        if number is not None:
            self.number = number
        else:
            self.number = self.CHANNELS[self.name].get('number')
        self.logo = logo + '/{}.png'.format(self.id)
        self.chUrl = 'https://d15umi5iaezxgx.cloudfront.net/{}/DRM/HLS/Live.m3u8'.format(self.id)      


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

    m3u = M3U('{}/iptv-italy.m3u'.format(SCRIPT_DIR))

    # Add Rai channels
    for ch_name in Rai.CHANNELS.keys():
        m3u.addChannel(Rai(ch_name))

    # Add Mediaset channels
    for ch_name in Mediaset.CHANNELS.keys():
        m3u.addChannel(Mediaset(ch_name))

    # Add Sky channels
    for ch_name in Sky.CHANNELS.keys():
        m3u.addChannel(Sky(ch_name))

    # Add Paramount channels
    for ch_name in Paramount.CHANNELS.keys():
        m3u.addChannel(Paramount(ch_name))

    # Add Norba channels
    for ch_name in Norba.CHANNELS.keys():
        m3u.addChannel(Norba(ch_name))

    # Add TGR Live streaming
    for ch_name in TGR.CHANNELS.keys():
        m3u.addChannel(TGR(ch_name))

    m3u.dump()
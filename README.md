# iptv-italy
This repository contains a collection of **free** and **legal** italian IPTV channels which were retrieved from the official websites of the following TV companies:
- [*Rai*](https://www.raiplay.it/dirette)
- [*Mediaset*](https://www.mediasetplay.mediaset.it/diretta)
- [*Paramount Network*](https://www.paramountnetwork.it/diretta-tv/wp5pr2)
- [*Cielo*](https://www.cielotv.it/streaming.html), [*TV8*](https://tv8.it/streaming.html?zoneid=menu_streaming) and [*Sky TG24*](https://video.sky.it/diretta/tg24) provided by *Sky*
- [*TG Norba 24*](http://www.norbaonline.it/live.php?diretta=tgnorba)

The list is designed to be as stable as possible and it is compliant with the [*M3U*](https://en.wikipedia.org/wiki/M3U) standard. However, changes in the streaming settings in the websites of the aforementioned companies may prevent the current configuration from working. This list will be maintained to keep up with this possible changes but no guarantee is given in this sense. Together with the M3U list, the Python script used to generate the list is provided.

## Usage
To install the M3U playlist in the IPTV player, please use the following URL:
```
https://jurijnota.github.io/iptv-italy/iptv-italy.m3u
```

### Advanced Usage
Some streaming channels (e.g. *Cielo*, *Sky TG24* and *TV8*) have cookies features that prevent a simple retrieval of the M3U lists. To circumvent, this issue we provide a very simple proxy server which listens for HTTP connections on `127.0.0.1:80`. Therefore, in order to watch these channels, one should first execute the proxy server using
```
sudo python3 proxy3.py
```
or
```
sudo ./proxy3.py
```
For a **Python 2** version of the program (e.g. to run it in a LibreELEC environment), please execute
```
sudo python2 proxy2.py
```
or
```
sudo ./proxy2.py
```
Be aware of the fact that these scripts need the [`channels.json`](https://github.com/jurijnota/iptv-italy/blob/main/channels.json) file in the directory where they are placed (and not where they are executed!) to work properly.

## Requirements
No specific requirements are needed to use this M3U playlist, however the following Python modules are mandatory to execute the proxy.
| Python 3 (`proxy3.py`) | Python 2 (`proxy2.py`) |
| -- | -- |
| [`re`](https://docs.python.org/3/library/re.html) | [`re`](https://docs.python.org/2.7/library/re.html) |
| [`os`](https://docs.python.org/3.9/library/os.html) | [`os`](https://docs.python.org/2.7/library/os.html) |
| [`json`](https://docs.python.org/3.9/library/json.html) | [`json`](https://docs.python.org/2.7/library/json.html) |
| [`requests`](https://docs.python-requests.org/en/master/index.html) | [`requests`](https://docs.python-requests.org/en/master/index.html) |
| [`socketserver`](https://docs.python.org/3.9/library/socketserver.html) | [`SocketServer`](https://docs.python.org/2.7/library/socketserver.html) |
| [`http.server`](https://docs.python.org/3.9/library/http.server.html) | [`BaseHTTPServer`](https://docs.python.org/2.7/library/basehttpserver.html) |

Of these requirements only `requests` may be missing. Please install it using one of the following commands depending on the installed version of Python.

For **Python 3**
```
sudo python3 -m pip install requests
```
For **Python 2**
```
sudo python2 -m pip install requests
```

### `pip` missing
May the `pip` module be missing on your device, please use these commands to download and install it.

For **Python 3**:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
```
For **Python 2**:
```
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
sudo python2 get-pip.py
```

## Known issues
This list may not work entirely with [*VLC*](https://www.videolan.org/vlc/) and it has been tested with the add-on [*PVR IPTV Simple Client*](https://kodi.wiki/view/Add-on:PVR_IPTV_Simple_Client) of [*Kodi*](https://kodi.tv/). This issue has partially been solved, however some problems can still arise.

Because of the deployment of [*DRM*](https://it.wikipedia.org/wiki/Digital_rights_management) features, [*La7*](https://www.la7.it/dirette-tv) and [*La7d*](https://www.la7.it/live-la7d) are not available in the list provided. To watch La7 channels with **Kodi**, we recommend [LA7-LA7d Kodi plugin](https://github.com/luivit/plugin.video.rivedila7) that can be found also in the official Kodi 19 repository.
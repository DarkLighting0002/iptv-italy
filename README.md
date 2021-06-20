# iptv-italy
This repository contains a collection of **free** and **legal** italian IPTV channels which were retrieved from the official websites of the major TV companies:
- [*Rai*](https://www.raiplay.it/dirette)
- [*Mediaset*](https://www.mediasetplay.mediaset.it/diretta)

The list is designed to be as stable as possible and it is compliant with the [*M3U*](https://en.wikipedia.org/wiki/M3U) standard. However, changes in the streaming settings in the websites of the aforementioned companies may prevent the current configuration from working. This list will be maintained to keep up with this possible changes but no guarantee is given in this sense. Together with the M3U list, a Python script is provided to generate the list querying informations from the original sources.

## Usage
To use the M3U playlist, provide the IPTV player with the following URL:
```
https://jurijnota.github.io/iptv-italy/iptv-italy.m3u
```

## Known issues
This list may not work entirely with [*VLC*](https://www.videolan.org/vlc/) and it has been tested with the add-on [*PVR IPTV Simple Client*](https://kodi.wiki/view/Add-on:PVR_IPTV_Simple_Client) of [*Kodi*](https://kodi.tv/).

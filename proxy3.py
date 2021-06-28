#!/usr/bin/env python3
import re
import os
import json
import requests as req
import socketserver
from http.server import BaseHTTPRequestHandler


PORT = 10293
LISTEN_ADDR = '127.0.0.1'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

with open('{}/channels.json'.format(SCRIPT_DIR), 'r') as f:
    CHANNELS = json.load(f)

_streamIdRegex = re.compile(r'(?:[\?|&]([^\s&=]*)=([^\s&=]*))')


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Simple HTTP proxy server.
    """

    def Sky_proxy(self, id):
        """
        Handle Sky channels proxying. Retrieves cookies 
        and requests from the channel JSON file.
        """
        jsonUrl = 'https://apid.sky.it/vdp/v1/getLivestream?id={}&isMobile=false'.format(id)
        jsonReq = req.get(jsonUrl)
        if not jsonReq.ok:
            self.send_response(jsonReq.status_code)
            self.end_headers()
            self.wfile.write(jsonReq.content)
        else:
            chJson = json.loads(jsonReq.text)
            if 'streaming_url' not in chJson.keys():
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Could not find "streaming_url" in JSON.')
            else:
                self.send_response(301)
                self.send_header('Location', chJson['streaming_url'])
                self.end_headers()

    def Paramount_proxy(self, id):
        """
        Handle Paramount channels proxying. The first link
        in the Paramount Network master playlist is broken, this
        mirror just deletes it.
        """
        chUrl = 'http://viacomitalytest-lh.akamaihd.net/i/sbshdlive_1@195657/master.m3u8'
        chReq = req.get(chUrl)
        if not chReq.ok:
            self.send_response(chReq.status_code)
            self.end_headers()
            self.wfile.write(chReq.content)
        else:
            body = ''
            lines = chReq.text.split('\n')
            # Remove line 1 and 2
            lines.pop(1)
            lines.pop(1)
            for line in lines:
                body += line + '\n'
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body.encode(encoding='UTF-8'))

    def do_GET(self):
        # Get queries from the request
        queries = dict(_streamIdRegex.findall(self.path))
        stream_id = str(queries.get('id'))

        for value in CHANNELS.get('Sky', {}).values():
            id = value.get('id')
            if stream_id == id:
                self.Sky_proxy(id)
                break
        else:
            for value in CHANNELS.get('Paramount', {}).values():
                id = value.get('id')
                if stream_id == id:
                    self.Paramount_proxy(id)
                    break
            else:
                self.send_response(404)
                self.end_headers()
                body = 'Could not find streaming id {}.'.format(stream_id)
                self.wfile.write(body.encode(encoding='UTF-8'))


if __name__ == '__main__':
    with socketserver.TCPServer((LISTEN_ADDR, PORT), HTTPRequestHandler) as httpd:
        print('serving at port {}'.format(PORT))
        httpd.serve_forever()
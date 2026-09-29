#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地静态服务器：用于预览 FTF Values 生成的网站。
从项目根目录提供文件，保证 seo_pages/*.html 中的 ../images/ 能正确解析到 /images/。
"""
import http.server
import socketserver
import os

PORT = 8765
ROOT = os.path.dirname(os.path.abspath(__file__))

EXT_MIME = {
    '.html': 'text/html; charset=utf-8',
    '.htm':  'text/html; charset=utf-8',
    '.js':   'text/javascript; charset=utf-8',
    '.mjs':  'text/javascript; charset=utf-8',
    '.css':  'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg':  'image/svg+xml',
    '.png':  'image/png',
    '.jpg':  'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif':  'image/gif',
    '.webp': 'image/webp',
    '.ico':  'image/x-icon',
    '.woff': 'font/woff',
    '.woff2':'font/woff2',
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        return EXT_MIME.get(ext, super().guess_type(path))

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *args):
        pass  # 静默日志

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', PORT), Handler) as httpd:
        print(f'Serving {ROOT} at http://127.0.0.1:{PORT}/')
        httpd.serve_forever()

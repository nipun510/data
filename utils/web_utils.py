#!/usr/bin/python

import requests
import os

def downloadFile(url, destination):
    requestStream = requests.get(url, stream= True)
    filename = url.split('/')[-1]
    filepath = os.path.join(destination, filename)
    with open(filepath, 'wb') as f:
        for chunk in requestStream.iter_content(chunk_size = 1024 * 1024):
            if chunk:
                f.write(chunk)




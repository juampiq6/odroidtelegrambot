import requests
import json

url = "http://localhost:9091/transmission/rpc"
reqHeaders = {
    'X-Transmission-Session-Id': ""
}

def handleToken():
    response = requests.post(url, json={"method": "torrent-get"})
    if (response.status_code == 409):
        reqHeaders['X-Transmission-Session-Id'] = response.headers['X-Transmission-Session-Id']

def getTorrent(id=None):
    payload = {
        "arguments": {
            "fields": [ "id", "name", "totalSize", "percentDone", "leftUntilDone", "status", "rateDownload"],
        },
        "method": "torrent-get",
    }
    if (id != None):
        payload['ids'] = id
    print(payload)
    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ getTorrents response -> "+ response.text)
    return response

def pauseTorrent(id):
    payload = {
        "arguments": {
             "ids": id
         },
        "method": "torrent-stop",
    }
    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ stopTorrent/"+id+" response -> "+ response.text)
    return response
    

def addTorrent(filename=None, file=None):
    payload = {
        "method":"torrent-add"
    }
    if (filename != None):
        payload["arguments"] = { "filename": filename}
    else:
        import base64
        data = open(file, "r").read()
        encoded = base64.b64encode(data)
        if (file != None):
            payload["arguments"] = { "metainfo": encoded}

    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ addTorrent response -> "+ response.text)
    return response

def deleteTorrent(withFile, id):
    payload = {
        "arguments": {
             "ids": id,
             "delete-local-data": withFile
         },
        "method":"torrent-remove",
    }
    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ deleteTorrent/"+str(id)+" response -> "+ response.text)
    return response


def resumeTorrent(id=None):
    payload = {
        "arguments": {
             "ids": id
         },
        "method": "torrent-start",
    }
    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ startTorrent/"+id+" response -> "+ response.text)
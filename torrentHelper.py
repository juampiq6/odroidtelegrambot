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

def getTorrent():
    payload = {
        "arguments": {
             "fields": [ "id", "name", "totalSize", "percentDone", "status", "rateDownload"]
         },
        "method": "torrent-get",
    }
    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ getTorrents response -> "+ response.text)
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

def startTorrent(id=None):
    payload = {
        "arguments": {
             "ids": id
         },
        "method": "torrent-start",
    }
    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ startTorrent response -> "+ response.text)

def pauseTorrent(id=None):
    payload = {
        "arguments": {
             "ids": id
         },
        "method": "torrent-stop",
    }
    response = requests.post(url, json=payload, headers=reqHeaders)
    print("@@ stopTorrent response -> "+ response.text)


def main():

    handleToken()
    startTorrent(1)
    getTorrent()

if __name__ == "__main__":
    main()




# if __name__ == "__main__":
#     main()
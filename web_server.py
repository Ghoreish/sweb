import socket,_thread,os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0",80))
s.listen(10)
def greq(d):
    # get directory of a http request
    d=str(d)
    if 'GET' == d[2:5]:
        d=d.split('GET /')[1]
        d=d.split(' HTTP')[0]
        return d
    else:
        return ""
def ghost(d):
    d = str(d)
    if '\\r\\nHost: ' in d:
        d = d.split('\\r\\nHost: ')[1]
        d = d.split('\\r\\n')[0]
        return d+"/"
    else:
        return ""
def conn(x):
    data=x.recv(10240)
    req=greq(data)
    hostn=ghost(data)
    hostlist=os.listdir()
    hostlist.remove("files")
    hostlist.remove("pages")
    hostlist.remove("web_server.py")
    if hostn[:-1] not in os.listdir():
        hostn=""
    if req=='':
        req='main.html'
    if req in os.listdir(hostn+'pages') and req.split(".")[-1] == "html":
        # pages dir
        res=open(hostn+"pages/"+req,"rb").read()
        x.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: '+str(len(res)).encode()+b'\r\n\r\n'+res+b'\r\n\r\n')
    elif req in os.listdir(hostn+'files') and req.split(".")[-1] != "html":
        # files dir
        # you can add other types here
        tdic = {"png": "image", "jpg": "image", "jpeg": "image", "x-icon": "image"}
        res = open(hostn+"files/" + req, "rb").read()
        if req.split(".")[-1] == "ico":
            req = req[:-3] + "x-icon"
        x.send(b'HTTP/1.1 200 OK\r\nContent-Type: ' + tdic[req.split(".")[-1]].encode() + b'/' + req.split(".")[-1].encode() + b'\r\nContent-Length: ' + str(len(res)).encode() + b'\r\n\r\n' + res + b'\r\n\r\n')
    else:
        # not found page in pages dir
        res =open(hostn+"pages/notfound.html", "r").read()
        x.send(b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: ' + str(len(res)).encode() + b'\r\n\r\n' + res.encode() + b'\r\n\r\n')
    x.close()
while True:
    # look how simple it is :)
    a,b=s.accept()
    _thread.start_new_thread(conn,(a,))

import socket,_thread,os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",80))
s.listen(10)
def greq(d):
    d=str(d)
    if 'GET' == d[2:5]:
        d=d.split('GET /')[1]
        d=d.split(' HTTP')[0]
        print(d)
        return d
    else:
        return ""
def conn(x):
    data=x.recv(10240)
    req=greq(data)
    if req=='':
        req='main.html'
    if req in os.listdir('pages') and req.split(".")[-1] == "html":
        res=open("pages/"+req,"rb").read()
        x.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: '+str(len(res)).encode()+b'\r\n\r\n'+res+b'\r\n\r\n')
    elif req in os.listdir('files') and req.split(".")[-1] != "html":
        tdic = {"png": "image", "jpg": "image", "jpeg": "image", "x-icon": "image"}
        res = open("files/" + req, "rb").read()
        if req.split(".")[-1] == "ico":
            req = req[:-3] + "x-icon"
        x.send(b'HTTP/1.1 200 OK\r\nContent-Type: ' + tdic[req.split(".")[-1]].encode() + b'/' + req.split(".")[
            -1].encode() + b'\r\nContent-Length: ' + str(len(res)).encode() + b'\r\n\r\n' + res + b'\r\n\r\n')
    else:
        res =open("pages/notfound.html", "r").read()
        x.send(b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: ' + str(len(res)).encode() + b'\r\n\r\n' + res.encode() + b'\r\n\r\n')
    x.close()
while True:
    a,b=s.accept()
    _thread.start_new_thread(conn,(a,))
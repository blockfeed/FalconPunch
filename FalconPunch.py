import os, socket, sys, struct

statinfo = os.stat(sys.argv[1])
fbiinfo = struct.pack('!q', statinfo.st_size)
p = sys.argv[1]
dsip = raw_input('Enter IP: ')

file = open(p, "rb")
sock = socket.socket()
sock.connect((dsip, 5000))

sock.send(fbiinfo)

while True:
    chunk = file.read(16384)
    if not chunk:
        break  # EOF
    sock.sendall(chunk)

sock.close()
sys.exit()

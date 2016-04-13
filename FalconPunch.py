import os, socket, sys, struct, time

def term_move_up (n):
    sys.stdout.write("\033[%sA" % n)

def print_progress (current, total):
    bars = 30
    percent = float(current) / float(total)
    filled = bars * percent
    result = "["
    while filled > 0:
        result += "#"
        filled -= 1
        bars -= 1
    while bars > 0:
        result += " "
        bars -= 1
    result += "]"
    result += str(int(percent * 100)) + "%"
    term_move_up(1)
    print result

def main (args):
    files = []
    opts = {}
    for arg in args:
        if arg.startswith("--"):
            arg = arg[2:].split("=")
            opts[arg[0]] = "=".join(arg[1:])
        else:
            if not arg.lower().endswith(".cia"):
                if not raw_input("File %s is not a '.cia', continue? [y/n] " % arg).strip() == "y":
                    return
            files.append(arg)
    dsip = raw_input("Enter IP: ") if "ip" not in opts else opts["ip"]
    dsip = dsip.strip()
    for p in files:
        statinfo = os.stat(p)
        totalsize = statinfo.st_size
        fbiinfo = struct.pack("!q", totalsize)
        
        print "Sending file %s" % p
        file = open(p, "rb")
        sock = socket.socket()
        trycount = 0
        while True:
        	try:
                print "Trying to connect to %s (#%s)..." % (dsip, trycount+1)
                sock.connect((dsip, 5000))
                break
            except socket.error:
            	time.sleep(1)
            	trycount += 1

        sock.send(fbiinfo)
        sent = 0

        print "Connected!\n"

        while True:
            chunk = file.read(16384)
            sent += len(chunk)
            print_progress(sent, totalsize)
            time.sleep(.1)
            if not chunk:
                break  # EOF
            sock.sendall(chunk)

        sock.close()
        file.close()
    return

main(sys.argv[1:])
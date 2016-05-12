import sched
import subprocess
import time

class ProcessData:
    def __init__(self, process, name, path,monitorstatus=None,cycles=None):
        self.process = process
        self.name = name
        self.path = path
        self.monitorstatus = monitorstatus
        self.cycles = cycles

class UrlData:
    def __init__(self, url, port, timeout,monitorstatus=None,cycles=None):
        self.url = url
        self.port = port
        self.timeout = timeout
        self.monitorstatus = monitorstatus
        self.cycles = cycles
s = sched.scheduler(time.time, time.sleep)

processes=[]
connectivity=[]
def addprocess(path):
    from subprocess import STDOUT
    # Start process
    executable="/bin/sh"
    p = subprocess.Popen([executable,'-c', path],shell=False,stdout=subprocess.PIPE,stderr=STDOUT)
    out, err = p.communicate()
    print(out.decode())
    processes.append(ProcessData(p,executable,path))
    print("Starting program "+ path +" with PID :"+str(p.pid))
    return p.pid

def addmonitorurl(url,port,timeout):
    connectivity.append(UrlData(url,port,timeout))

def check_pids():
    if processes is not None and len(processes)>0:
        for p in processes :
            poll = p.process.poll()
            if poll is None:
                print("Program "+ p.path +" with PID "+str(p.process.pid) +" is running")
                continue
            else:
                print(str(p.process.pid) +" is dead or Z")
                processes.remove(p)
                addprocess(p.path)


def makeconnection(url,port,timeout):
    import socket
    try:
        serv = socket.socket()
        serv.settimeout(timeout)
        serv.connect((url,port))
        serv.send("hello\n")
        serv.close()
        return True
    except Exception as e:
        print ("Error during connection to "+url+":"+str(port)+" "+e.message)
        serv.close()
        return False


def monitorurl():
    if connectivity is not None and len(connectivity)>0:
        for c in connectivity :
                response=makeconnection(c.url,c.port,c.timeout)
                if(response):
                    print("Connection to "+c.url+":"+str(c.port)+" success ")
                else:
                    print("Connection to "+c.url+":"+str(c.port)+" failed ")


def addconnectivitycheck(url):
    connectivity.append(url)
    pass


def main():
    addprocess("keeprnning.sh")
    addprocess("keeprunning1.sh")
    addmonitorurl("apg-test1.corp.apple.com",443,1)
    addmonitorurl("test1-worldpayproxy.corp.apple.com",443,1)
    while True:
        check_pids()
        monitorurl()
        time.sleep(5)
    s.run()

main()

import threading
import time
import nmap
from pexpect import pxssh

log_lock = threading.RLock()

class MonitorTask(threading.Thread):

    last_result = False

    def __init__(self, host, ip_address, port, delay=15):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.delay = delay
        self.host = host

    def run(self):
        while True:
            res = self.check_if_host_is_up()
            if res != self.last_result:
                if res and not self.last_result:
                    self.host_back_online()
                else:
                    self.host_went_offline()
            time.sleep(self.delay)

    def check_if_host_is_up(self):
        nm = nmap.PortScanner()

        if self.port > 0:
            nm.scan(self.ip_address, str(self.port))
            if len(nm.all_hosts()) > 0:
                return nm[self.ip_address].has_tcp(self.port)
        else:
            p = abs(self.port)
            nm.scan(self.ip_address, 'U:{}'.format(p))
            if len(nm.all_hosts()) > 0:
                return nm[self.ip_address].has_udp(p)
        return False

    def host_went_offline(self):
        self.log("Port {} on IP {} went offline".format(self.port, self.ip_address))

    def host_back_online(self):
        self.log("Port {} on IP {} came up".format(self.port, self.ip_address))
        for attack in self.host.attacks:
            attack(self.host)

    def log(self, to_log):
        with log_lock:
            with open('data/logs/uptime.log', 'a') as logfile:
                logfile.write(to_log + '\n')

def ssh_to_host(host, cmd='', port=22):
    s = pxssh.pxssh()
    for u, p in host.credentials:
        print("Attempting to SSH to {} with creds {}".format(host.parent.ip, (u,p)))
        if s.login (host.parent.ip, u, p, port=port):
            s.sendline (cmd)
            s.prompt()
            with log_lock:
                with open('data/logs/attacks.log', 'a') as logfile:
                    logfile.write(s.before + '\n')
            print("Got into host {} with credentials {}".format(host.parent.ip, (u,p)))
            s.close()
            break
        else:
            print("Login failed on {}".format(host.parent.ip))
    print("SSH run complete on {}:{}".format(host.parent.ip, port))
    return s.before

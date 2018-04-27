import threading
import time
import nmap

log_lock = threading.RLock()

class MonitorTask(threading.Thread):

    last_result = False

    def __init__(self, ip_address, port, delay=1):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.port = port
        self.delay = delay

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

    def log(self, to_log):
        with log_lock:
            with open('data/logs/uptime.log', 'a') as logfile:
                logfile.write(to_log + '\n')

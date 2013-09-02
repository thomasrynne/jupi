#!/usr/bin/python
import websocket
import thread
import time
from jenkinsapi import api
import hubctrl
import sys
import argparse

class Jupi:
    def __init__(self, hostname, http_port, ws_port):
        self.hostname = hostname
        self.http_port = http_port
        self.ws_port = ws_port
        def on_message(ws, message):
            self.do_check()
        jenkins_ws = "ws://" + hostname + ":" + str(ws_port) + "/jenkins"
        print jenkins_ws
        self.ws =  websocket.WebSocketApp(jenkins_ws, on_message = on_message)
        self._rules = []

    def add_binding(self, devnum, portnum, expression):
        self._rules.append( [devnum,portnum,expression] )
        
    def do_check(self):
        for (devnum, portnum, expression) in self._rules:
            on = expression()
            hubctrl.switch(devnum, portnum, on)

    def is_good(self, job_name):
        job = api.get_latest_complete_build("http://" + self.hostname + ":" + str(self.http_port), job_name)
        return job.is_good()
    def is_bad(self, jobname):
        return not self.is_good(jobname)

    def start(self):
        self.do_check()
        self.ws.run_forever()
        print "ran"

def list_hubs():
    hubs = hubctrl.list_power_switching_hubs().values()
    for hub in hubs:
        print hub
        print "Hub: " + str(hub["busnum"]) + " (" + str(hub["num_ports"]) + " ports)"
    if len(hubs) == 0:
        print "No hubs with power switching support found"

def main():
    parser = argparse.ArgumentParser(description='JUPI: Jenkins USB Power Indicator')
    parser.add_argument('--list-hubs', action="store_true",
                   help='list hubs with power switching support')
    parser.add_argument('--hub', metavar='hubnum', nargs=1,
                   help='the usb hub number (defaults to the only avaliable hub)')
    parser.add_argument('--port', metavar='portnum', nargs=1,
                   help='the port number to switch on (1)')
    parser.add_argument('--host', metavar='hostname', nargs=1,
                   help='the host running jenkins (localhost)')
    parser.add_argument('--http-port', metavar='http_port', nargs=1,
                   help='the jenkings http port (8080)')
    parser.add_argument('--ws-port', metavar='ws_port', nargs=1,
                   help='the jenkins websocket port (8081)')
    parser.add_argument('--test-on', action="store_true",
                   help='switch the port on then exit')
    parser.add_argument('--test-off', action="store_true",
                   help='switch the port off then exit')
    parser.add_argument('--test', action="store_true",
                   help='switch the port off then on')
    parser.add_argument('--job', metavar='jobname', nargs=1,
                   help='the job to monitor')
    args = parser.parse_args()

    hostname = "localhost"
    if args.host: hostname = args.host[0]
    http_port = 8080
    if args.http_port: http_port = int(args.http_port[0])
    ws_port = 8081
    if args.ws_port: ws_port = int(args.ws_port[0])
    hub = None
    if args.hub: hub = int(args.hub[0])
    port = 1
    if args.port: port = int(args.port[0])
    job = "Test1"
    if args.job: job = args.job[0]

    if args.list_hubs:
        list_hubs()
    elif args.test:
            print "port " + str(port) + " off-1s-on"
            hubctrl.switch(hub, port, False)
            time.sleep(1)
            hubctrl.switch(hub, port, True)
    elif args.test_on:
            print "port " + str(port) + " on"
            hubctrl.switch(hub, port, True)
    elif args.test_off:
            print "port " + str(port) + " off"
            hubctrl.switch(hub, port, False)
    else:
        jupi = Jupi(hostname, http_port, ws_port)
        jupi.add_binding(hub, port, lambda : jupi.is_bad(job))
        jupi.start()

if __name__ == "__main__":
    main()


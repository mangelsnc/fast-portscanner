#!/usr/bin/env python3

import socket
import argparse
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

open_sockets = []

def portscanner(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    open_sockets.append(s)

    try:
        s.connect((host, port))
        print(colored(f"[+] Port {port} is open in {host}", 'green'))
    
    except(TimeoutError, ConnectionError, ConnectionRefusedError, ConnectionAbortedError):
        pass

    finally:
        open_sockets.remove(s)
        s.close()

def get_arguments():
    parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", dest="target", required=True, help="Target host to scan. Ex: -t 192.168.1.1")
    parser.add_argument("-p", "--port", dest="ports", required=True, help="Ports to scan. Ex: -p 1-1000, -p 21,22,80, -p 443")
    options = parser.parse_args()
    
    return options.target, options.ports

def parse_ports(ports):
    if '-' in ports:
        ports = ports.split('-')

        return range(int(ports[0]), int(ports[1]) + 1)
    
    if ',' in ports:
        return [int(port) for port in ports.split(',')]

    return [int(ports)]

def handle_sigint(signal, frame):
    print(colored(f"\n[!] Aborting port scan...\n", 'red'))

    for socket in open_sockets:
        socket.close()

    sys.exit(1)

if __name__ == "__main__":
 
    signal.signal(signal.SIGINT, handle_sigint)
    host, ports = get_arguments()
    ports = parse_ports(ports)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda port: portscanner(host, port), ports)

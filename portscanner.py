#!/usr/bin/env python3

import socket
import argparse
import threading
from termcolor import colored

def portscanner(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
        s.connect((host, port))
        print(colored(f"[+] Port {port} is open in {host}", 'green'))
    
    except(TimeoutError, ConnectionError, ConnectionRefusedError, ConnectionAbortedError):
        pass

    finally:
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

if __name__ == "__main__":
 
    host, ports = get_arguments()
    ports = parse_ports(ports)

    for port in ports:
        thread = threading.Thread(target=portscanner, args=[host, port])
        thread.start()
        thread.join()

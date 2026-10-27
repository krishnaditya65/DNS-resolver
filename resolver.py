import socket
import struct
import random

def build_query(domain: str):
    header = struct.pack("!HHHHHH", random.randint(1, 65535), 0x0100, 1, 0, 0, 0)  # ID + flags + 1 question
    qname = b''.join(struct.pack("!B", len(part)) + part.encode() for part in domain.split('.')) + b'\x00'
    question = qname + struct.pack("!HH", 1, 1)  # A record, IN class
    return header + question

def parse_ip(answer):
    return '.'.join(str(b) for b in answer[-4:])

def resolve(domain):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    query = build_query(domain)
    sock.sendto(query, ("8.8.8.8", 53))          # Google DNS as starting point
    data, _ = sock.recvfrom(1024)
    # Very naive parsing — just grab the last 4 bytes as IP for learning
    ip = parse_ip(data)
    print(f"{domain} → {ip}")
    return ip

if __name__ == "__main__":
    resolve("example.com")
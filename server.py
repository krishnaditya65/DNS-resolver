import socket
import struct
import random

# Hardcoded "zone" for learning
ZONE = {
    "test.local": "192.168.1.100",
}

def build_response(query_data, ip):
    # Copy header + set response flags
    header = query_data[:12]
    header = header[:2] + b'\x81\x80' + header[4:6] + b'\x00\x01\x00\x01\x00\x00\x00\x00'  # 1 answer
    question = query_data[12:]
    answer = question[:len(question)-4] + struct.pack("!HHHIH", 1, 1, 300, 4, 4) + socket.inet_aton(ip)
    return header + question + answer

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5353))   # ← change to 53 later if you want real port

print("Authoritative server running on :5353...")
while True:
    data, addr = sock.recvfrom(512)
    # Super simple — assume it's asking for test.local
    response = build_response(data, ZONE.get("test.local", "127.0.0.1"))
    sock.sendto(response, addr)
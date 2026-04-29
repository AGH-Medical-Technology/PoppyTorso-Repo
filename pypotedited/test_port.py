#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple raw port test"""

import sys
import serial
import time

sys.path.insert(0, '/home/mist/Desktop/techmed/poppy/pypotedited')
from dynamixel import get_available_ports

ports = get_available_ports()

if not ports:
    print("❌ BRAK PORTÓW!")
    sys.exit(1)

print(f"Znaleziono {len(ports)} port(y): {ports}\n")

for port in ports:
    print(f"="*60)
    print(f"Testing: {port}")
    print(f"="*60)
    
    try:
        # Test 1: Open port
        print(f"[1/3] Otwieranie portu...", end="", flush=True)
        ser = serial.Serial(port, 1000000, timeout=0.05)
        print(" ✓")
        
        # Test 2: Send ping packet (ID=1, broadcast ping)
        print(f"[2/3] Wysyłanie ping do ID=1...", end="", flush=True)
        # DXL v1 Ping packet format: FF FF ID LEN INSTR CHECKSUM
        # ID=1, LEN=2, INSTR=1 (ping)
        ping_packet = bytes([0xFF, 0xFF, 0x01, 0x02, 0x01, 0xFB])
        
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        written = ser.write(ping_packet)
        if written == len(ping_packet):
            print(" ✓ (wysłano)")
        else:
            print(f" ✗ (wysłano {written}/{len(ping_packet)} bajtów)")
        
        # Test 3: Read response
        print(f"[3/3] Czekam na odpowiedź (2 sekundy)...", end="", flush=True)
        ser.timeout = 2.0  # Wait longer
        response = ser.read(6)  # Ping response is 6 bytes
        
        if response:
            print(f" ✓")
            print(f"     OTRZYMANO: {response.hex()} ({len(response)} bajtów)")
            print(f"     ✅ PORT DZIAŁA! Urządzenie ODPOWIADA!\n")
        else:
            print(f" ✗")
            print(f"     ⚠️  BRAK ODPOWIEDZI - urządzenie nie odpowiada\n")
        
        ser.close()
        
    except Exception as e:
        print(f" ✗\n     BŁĄD: {e}\n")

print("="*60)
print("\nWNIOSKI:")
print("="*60)
print("✓ OTRZYMANO ODPOWIEDŹ  = Urządzenie działa")
print("✗ BRAK ODPOWIEDZI      = Zmień kablowanie/zasilanie/port")
print("✗ BŁĄD NA PORCIE       = Sprzęt lub uprawnienia")

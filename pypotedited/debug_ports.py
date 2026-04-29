#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug script to find available ports and motors"""

import sys
import time
import serial
sys.path.insert(0, '/home/mist/Desktop/techmed/poppy/pypotedited')

from dynamixel import get_available_ports, get_port_vendor_info
from dynamixel.io import DxlIO, Dxl320IO
from dynamixel.io.abstract_io import DxlError

def clear_port_buffer(port):
    """Clear any lingering data in the serial port buffer"""
    try:
        ser = serial.Serial(port, timeout=0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.close()
        time.sleep(0.5)
    except Exception as e:
        print(f"      ⚠️  Nie można wyczyścić bufora: {e}")

def try_scan_with_retry(port, dxl_class, class_name, max_retries=1, quick_scan=True):
    """Try to scan with retry logic and progress indication"""
    for attempt in range(max_retries):
        try:
            # Clear buffer before attempt
            if attempt > 0:
                print(f"      🔄 Próba {attempt+1}/{max_retries}...")
                clear_port_buffer(port)
                time.sleep(1)
            
            # For quick scan, only check first 50 IDs instead of all 254
            if quick_scan:
                scan_range = range(50)  # Only check IDs 0-49
                print(f"      🔍 Szybki scan (IDs 0-49)...", end="", flush=True)
            else:
                scan_range = range(254)
                print(f"      🔍 Pełny scan (IDs 0-253)...", end="", flush=True)
            
            with dxl_class(port, timeout=0.05) as dxl:
                found_ids = []
                for id_num in scan_range:
                    if dxl.ping(id_num):
                        found_ids.append(id_num)
                        print(f"✓", end="", flush=True)
                    else:
                        print(f".", end="", flush=True)
                
                print()  # Newline
                if found_ids:
                    print(f"      ✅ Znaleziono: {found_ids}")
                    return True
                else:
                    print(f"      ⚠️  Nie znaleziono silników w szybkim skanie")
                    # Jeśli quick_scan, spróbuj jeszcze pełny scan
                    if quick_scan and attempt == 0:
                        print(f"      🔍 Próba pełnego skanu (może trwać dłużej)...", end="", flush=True)
                        with dxl_class(port, timeout=0.05) as dxl2:
                            found_ids = []
                            for id_num in range(254):
                                if dxl2.ping(id_num):
                                    found_ids.append(id_num)
                                    print(f"✓", end="", flush=True)
                                else:
                                    print(f".", end="", flush=True)
                            print()
                            if found_ids:
                                print(f"      ✅ Znaleziono w pełnym skanie: {found_ids}")
                                return True
                    return False
                    
        except DxlError as e:
            if attempt < max_retries - 1:
                continue
            print()
            print(f"      ⚠️  Błąd {class_name}: {e}")
            return False
        except KeyboardInterrupt:
            print()
            print(f"      ⛔ Skan przerwany przez użytkownika")
            return False
        except Exception as e:
            if attempt < max_retries - 1:
                continue
            print()
            print(f"      ⚠️  Błąd {class_name}: {e}")
            return False
    return False

print("=" * 60)
print("Dostępne porty szeregowe:")
print("=" * 60)

ports = get_available_ports()
if not ports:
    print("❌ Brak dostępnych portów!")
    sys.exit(1)

for port in ports:
    print(f"\n📍 Port: {port}")
    try:
        info = get_port_vendor_info(port)
        print(f"   Info: {info}")
    except Exception as e:
        print(f"   Info: (brak info - {e})")
    
    # Clear port before scanning
    clear_port_buffer(port)
    
    # Spróbuj DxlIO (MX, AX, RX, SR)
    print("   🔍 Szuka silników DxlIO (MX, AX, RX, SR)...")
    try_scan_with_retry(port, DxlIO, "DxlIO", quick_scan=True)
    
    # Spróbuj Dxl320IO (XL320)
    print("   🔍 Szuka silników Dxl320IO (XL320)...")
    try_scan_with_retry(port, Dxl320IO, "Dxl320IO", quick_scan=True)

print("\n" + "=" * 60)
print("\nUprawnienia do portów:")
print("=" * 60)

import os
import subprocess

for port in ports:
    try:
        stat_info = os.stat(port)
        perms = oct(stat_info.st_mode)[-3:]
        print(f"{port}: {perms}")
    except Exception as e:
        print(f"{port}: Error - {e}")

# Check usb devices
print("\n" + "=" * 60)
print("Podłączone urządzenia USB (lsusb):")
print("=" * 60)
try:
    result = subprocess.run(['lsusb'], capture_output=True, text=True, timeout=5)
    print(result.stdout)
except Exception as e:
    print(f"Nie można uruchomić lsusb: {e}")

import zlib
import socket
import binascii
import re
import time

def recv_until(s, pattern, timeout=10):
    """Receive data until a pattern is found or timeout occurs."""
    s.settimeout(timeout)
    data = b""
    start_time = time.time()
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            if pattern in data:
                return data
            if time.time() - start_time > timeout:
                break
        except socket.c_timeout:
            break
    return data

def try_decompress(data):
    """Try different decompression methods."""
    attempts = [
        (zlib.decompress, {"wbits": zlib.MAX_WBITS}, "standard zlib"),
        (zlib.decompress, {"wbits": -zlib.MAX_WBITS}, "raw DEFLATE"),
        (zlib.decompress, {"wbits": 15}, "zlib with wbits=15"),
        (zlib.decompress, {"wbits": 31}, "zlib with wbits=31"),
    ]

    for decompress_func, kwargs, method in attempts:
        try:
            return decompress_func(data, **kwargs), method
        except zlib.error as e:
            print(f"{method} decompression failed: {e}")

    # Try skipping bytes
    for i in range(1, 5):
        try:
            return zlib.decompress(data[i:]), f"zlib skipping {i} bytes"
        except zlib.error as e:
            print(f"zlib skipping {i} bytes failed: {e}")

    return None, None

def main():
    HOST = "cyberchallenge.disi.unitn.it"
    PORT = 8102

    try:
        # Create and connect socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to server")

        # Receive welcome message and file data
        data = recv_until(s, b"Here is the file:\n")
        if not data:
            print("Error: No welcome message received")
            return
        print("Received welcome message:", data.decode(errors='ignore'))

        # Extract hex string from welcome message
        file_data = data.split(b"Here is the file:\n")[1]
        hex_str_match = re.search(br'^[0-9a-fA-F]+', file_data)
        if not hex_str_match:
            print("Error: No valid hex data found in welcome message")
            print(f"Data after 'Here is the file:': {file_data[:100]}...")
            return
        hex_str = hex_str_match.group(0)
        print(f"Extracted hex string (length {len(hex_str)}): {hex_str[:100].decode()}...")

        # Validate hex string length (must be even)
        if len(hex_str) % 2 != 0:
            print("Error: Hex string length is odd, likely incomplete")
            return

        # Save hex string for inspection
        with open("raw_hex.txt", "wb") as f:
            f.write(hex_str)
        print("Hex string saved to 'raw_hex.txt'")

        # Decode hex to binary
        try:
            compressed_data = binascii.unhexlify(hex_str)
            print(f"Got compressed data: {len(compressed_data)} bytes")
        except binascii.Error as e:
            print(f"Hex decoding error: {e}")
            print(f"Hex data: {hex_str[:100].decode()}...")
            return

        # Save raw compressed data
        with open("raw_compressed.bin", "wb") as f:
            f.write(compressed_data)
        print("Raw compressed data saved to 'raw_compressed.bin'")

        # Try decompression
        original_data, method = try_decompress(compressed_data)
        if original_data is None:
            print("Failed to decompress data. Sending minimal zlib stream as fallback.")
            # Create a minimal valid zlib stream (e.g., compress empty data)
            fallback_data = zlib.compress(b"")
            s.sendall(binascii.hexlify(fallback_data) + b"\n")
            print("Sent fallback zlib stream")
            response = recv_until(s, b"}", timeout=15)
            if response:
                print("Server response:", response.decode(errors='ignore'))
            else:
                print("No response received from server")
            return

        print(f"Successfully decompressed {len(original_data)} bytes using {method}")

        # Save original file
        with open("original.bin", "wb") as f:
            f.write(original_data)
        print("Original binary saved to 'original.bin'")

        # Modify the binary (example: patch a JZ to JMP)
        modified_data = bytearray(original_data)
        patch_offset = 0x100  # Adjust based on binary analysis
        if patch_offset < len(modified_data):
            print(f"Patching at offset {patch_offset}: {modified_data[patch_offset]:02x} -> 0xEB")
            modified_data[patch_offset] = 0xEB  # Change to JMP
        else:
            print("Invalid offset, no modification made")
            modified_data = original_data

        # Recompress modified data
        modified_compressed = zlib.compress(modified_data)
        size_diff = len(modified_compressed) - len(compressed_data)
        print(f"Compressed size difference: {size_diff} bytes")

        if abs(size_diff) > 30:
            print("Modification too large, adjust your changes")
            return

        # Send modified file
        s.sendall(binascii.hexlify(modified_compressed) + b"\n")
        print("Sent modified file")

        # Receive server response
        response = recv_until(s, b"}", timeout=15)
        if response:
            print("Server response:", response.decode(errors='ignore'))
        else:
            print("No response received from server")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    main()
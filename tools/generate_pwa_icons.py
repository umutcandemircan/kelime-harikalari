import struct
import zlib
import math

def create_png(width, height, filename):
    # Generates a clean compass & gold badge PNG for Sözcük Seferî
    raw_data = bytearray()
    cx, cy = width / 2, height / 2
    r_outer = width * 0.46
    r_inner = width * 0.38
    
    # Colors (RGBA)
    c_bg = (11, 19, 43, 255)       # Slate navy #0b132b
    c_gold = (245, 158, 11, 255)    # Amber gold #f59e0b
    c_turq = (13, 148, 136, 255)    # Teal turquoise #0d9488
    c_ivory = (248, 249, 250, 255)  # Ivory #f8f9fa
    
    for y in range(height):
        raw_data.append(0) # Filter byte: None
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > r_outer:
                # Transparent outside
                raw_data.extend((0, 0, 0, 0))
            elif dist > r_outer - (width * 0.04):
                # Gold border ring
                raw_data.extend(c_gold)
            elif dist > r_inner:
                # Outer ring navy
                raw_data.extend(c_bg)
            else:
                # Inner compass star
                # 8-point compass star math
                angle = math.atan2(dy, dx)
                # Modulo 45 deg
                star_r = (width * 0.30) * (0.6 + 0.4 * abs(math.cos(angle * 4)))
                if dist < width * 0.16:
                    # Center ivory hub
                    raw_data.extend(c_ivory)
                elif dist < star_r:
                    # Compass blades
                    raw_data.extend(c_turq)
                else:
                    raw_data.extend(c_bg)
                    
    # PNG File Structure
    def make_chunk(chunk_type, data):
        crc = zlib.crc32(chunk_type + data) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', crc)
        
    png_header = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    idat = make_chunk(b'IDAT', zlib.compress(bytes(raw_data), level=9))
    iend = make_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(png_header + ihdr + idat + iend)
        
    print(f"Generated {filename} ({width}x{height}) successfully.")

if __name__ == '__main__':
    create_png(192, 192, 'icon-192.png')
    create_png(512, 512, 'icon-512.png')

import sys, os

CSIZE = 0x1000

def get_dword(bts, pos):
    return int.from_bytes(bts[pos:pos+4], byteorder="little")

def read_header(fw, offset=0x0):
    rptr_lo = get_dword(fw, offset+0x0)
    aoff_lo  = get_dword(fw, offset+0xFFC)
    code_size = get_dword(fw, rptr_lo+aoff_lo+0xC)
    if rptr_lo == 0xFFFFFFFF or  aoff_lo  == 0xFFFFFFFF or code_size == 0xFFFFFFFF:
        return None

    code_offset = rptr_lo+aoff_lo+CSIZE

    return (rptr_lo, aoff_lo, code_offset,code_size)

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print("cd3215_tps6598_code_extractor.py [file_name]")
        return 0

    firmware_file_name = sys.argv[1]
    firmware = bytes()
    with open(firmware_file_name, "rb") as f:
        firmware = f.read()

    rptr_lo, aoff_lo, code_offset_lo, code_size_lo = read_header(firmware)

    print("")
    print("rptr_lo = " + hex(rptr_lo))
    print("aoff_lo = " + hex(aoff_lo) )
    print("code_offset_lo = " + hex(code_offset_lo))
    print("code_size_lo = " + hex(code_size_lo))
    print("")

    with open(firmware_file_name+"_lo.bin", "wb") as f:
        f.write(firmware[code_offset_lo:code_offset_lo+code_size_lo])

    header_hi = read_header(firmware, offset=0x1000)
    if header_hi == None:
        print("High region not found.")
    else:
        rptr_hi, aoff_hi, code_offset_hi, code_size_hi = header_hi

        print("")
        print("rptr_hi = " + hex(rptr_hi))
        print("aoff_hi = " + hex(aoff_hi) )
        print("code_offset_hi = " + hex(code_offset_hi))
        print("code_size_hi = " + hex(code_size_hi))
        print("")
        with open(firmware_file_name+"_hi.bin", "wb") as f:
            f.write(firmware[code_offset_hi:code_offset_hi+code_size_hi])
        print("High region code is written to " + firmware_file_name+"_hi.bin")
    
    print("Low region code is written to " + firmware_file_name+"_lo.bin")


if __name__ == "__main__":
    main()
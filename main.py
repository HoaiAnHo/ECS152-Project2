from struct import pack
import struct
import socket
import datetime

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# #Creates a generic header to be concatenated w/ the rest of the DNS payload
# def make_header():
#     #id = 1234
#     header += struct.pack(">H", 1234)
#     header += pack(">H", 256)
#     header += pack(">H", 1)
#     header += pack(">H", 0)
#     header += pack(">H", 0)
#     header += pack(">H", 0)
#     return header


def make_header2( domain):
    payload = struct.pack(">H", 12345)
    payload += struct.pack(">H", 256)
    payload += struct.pack(">H", 1)
    payload += struct.pack(">H", 0)
    payload += struct.pack(">H", 0)
    payload += struct.pack(">H", 0)

    # Website to length + bytes
    domain_split = domain.split('.')
    for segment in domain_split:
        payload += struct.pack(">B", len(segment))
        for byte in bytes(segment, "utf-8"):
            payload += struct.pack(">B", byte)
    payload += struct.pack("B", 0)
    payload += struct.pack(">H", 1)
    payload += struct.pack(">H", 1)
    return payload


# # Uses split to remove "."s and then packs length of segments + segments
# def translate_url(domain):
#     out = ''
#     no_periods = domain.split(".")
#     for x in no_periods:
#         out += pack(">B", len(x))
#         for y in bytes(x):
#             out += y
#     out += '\x00'
#     return out

#
# def build_dns_response(data):
#     TransID = data[0:2]
#     print(TransID)
#

if __name__ == '__main__':
    print_hi('PyCharm')
    #domain = input("What url are we trying to Query?")
    # query = assemble_query(domain)
    query = make_header2("www.tmz.com")
    print("Outputting query to verify format")
    print(query)
    sockOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockOut.bind(('', 8888))
    sockOut.settimeout(20)
    transmit_time = datetime.datetime.now()
    sockOut.sendto(bytes(query), ("198.41.0.4,", 53))
    print("Packet Transmitted at: " + transmit_time.strftime("%m%d%Y, %H:%M:%S.%f")[:-3])
    data, address = sockOut.recvfrom(1024)
    respond_time = datetime.datetime.now()
    print("Received:" + str(data) + "\n Time received: " + respond_time.strftime("%m%d%Y, %H:%M:%S"))
    sockOut.close()
    messageReceived = struct.unpack_from(data, 12)
    messageTranslate = messageReceived.decode("utf-8")
    print(messageReceived)

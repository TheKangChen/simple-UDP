import socket
import pyaudio, queue, threading, time
# from opuslib import Decoder

serverAddressPort = ('127.0.0.1', 5002)
MAX_PACKET_SIZE = 3*1276
# FIFO buffer
q = queue.Queue(maxsize=2048)
buffer = 1024
msg = [b'C', b'D']

# Socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,MAX_PACKET_SIZE)

while True:
    # Start port audio
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=buffer)
    try:
        # Send connect message
        s.sendto(msg[0], serverAddressPort)
        data, _ = s.recvfrom(MAX_PACKET_SIZE)

        while len(data) > 0:
            q.put(data)
            stream.write(data)
        else:
            # Send disconnect message & close socket & port audio
            s.sendto(msg[1], serverAddressPort)
            s.close()
            stream.stop_stream()
            stream.close()
            p.terminate()
            break
    except socket.error:
        print(socket.error)

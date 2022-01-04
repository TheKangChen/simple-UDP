import socket
import time
import pyaudio, queue, wave, sys
# from opuslib import Encoder

serverAddressPort = ('127.0.0.1', 5001)
buffer = 960
# FIFO buffer
q = queue.Queue(maxsize=2048)

# Read file in bytes
wf = wave.open('./Q5_HW3_Piece_CKChen.wav','rb')

# Start port audio
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=buffer)

# Socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,buffer)

while True:
    try:
        # read file in frames
        data = wf.readframes(buffer)
        while len(data) > 0:
            q.put(data)
            frame = q.get()
            s.sendto(data, serverAddressPort)
            time.sleep(0.8*buffer/wf.getframerate()) # Wait buffer to fill before sending
        else:
            # Close socket & port audio
            s.close()
            stream.stop_stream()
            stream.close()
            p.terminate()
            break
    except socket.error:
        print(socket.error)

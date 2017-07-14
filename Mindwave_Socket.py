# Import libraries and packages
from __future__ import division
from mindwavemobile.MindwaveDataPoints import RawDataPoint, EEGPowersDataPoint,MeditationDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import socket
import sys
import math
import csv

# Choose if save EEG data to file
save_to_file = True

# Create csv file to dump brainwaves amplitudes
if save_to_file:
    csvfile = open('brainwaves.csv', 'wb')
    fieldnames = ['highAlpha', 'lowAlpha', 'highBeta', 'lowBeta', 'midGamma', 'lowGamma', 'theta', 'delta', 'meditationValue']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Set up host (self) and port
HOST = ''   # Allow all available interfaces
PORT = 8885 # Designate non-privileged port

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket succesfully created'

# Bind socket
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening for incoming connections (from the Clojure app)
s.listen(10)
print 'Socket is now listening'

# Establish connection with Clojure app
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

# After connection was established - communicate with Mindwave Mobile device
# Extract brainwaves amplitudes, meditaion values, perform normalization,
# Send data to Clojure app
if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()
    if (mindwaveDataPointReader.isConnected()):
        while(True):
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (not dataPoint.__class__ is RawDataPoint):

                # Extract Meditation Value
                if dataPoint.__class__ is MeditationDataPoint:
                    datam = dataPoint
                    vdatam = vars(datam)
                    #vmed = 300-2*vdatam['meditationValue']
                    vmed = vdatam['meditationValue']

                    #print "vmed=%s" % vmed

                # Extract EEG values
                if dataPoint.__class__ is EEGPowersDataPoint:
                    data = dataPoint
                    # Convert datapoint to a dictionary
                    vdata = vars(data)

                    # Save as a row to csv file
                    if save_to_file:
                        writer.writerow({'highAlpha': vdata['highAlpha'], 'lowAlpha': vdata['lowAlpha'], 'highBeta': vdata['highBeta'], 'lowBeta': vdata['lowBeta'], 'midGamma': vdata['midGamma'], 'lowGamma': vdata['lowGamma'], 'theta': vdata['theta'], 'delta': vdata['delta'], 'meditationValue': vdatam['meditationValue']})

                    # For alpha,beta and gamma waves average high and low values
                    valpha = (vdata['highAlpha']+vdata['lowAlpha'])/2
                    vbeta = (vdata['highBeta']+vdata['lowBeta'])/2
                    vgamma = (vdata['midGamma']+vdata['lowGamma'])/2

                    # Since theta and delta waves only report single value use them as they are
                    vtheta = vdata['theta']
                    vdelta = vdata['delta']

                    # Calculate combined sum for all waves
                    vall = valpha+vbeta+vgamma+vtheta+vdelta

                    # Normalize each wave amplitude to the sum
                    valpha = valpha/vall
                    vbeta = vbeta/vall
                    vgamma = vgamma/vall
                    vtheta = vtheta/vall
                    vdelta = vdelta/vall

                    # Calculate a single note (pitch for overtone's piano)
                    vnote = round(30*vdelta+45*vtheta+60*valpha+75*vbeta+90*vgamma)
                    print(vnote)


                    # Form the message (reply) to be sent to Clojure app
                    reply = str(valpha)+' '+str(vbeta)+' '+str(vdelta)+' '+str(vtheta)+' '+str(vgamma)+' '+str(vmed)+' '+str(vnote)
                    print (reply)

                    # Add new line symbol, convert to unicode utf_8
                    reply = reply +'\n'
                    reply = unicode(reply, 'utf_8')

                    # Send the message to Clojure app
                    conn.sendall(reply)

    else:
        print(textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " "))

# Close file, connection and the socket
csvfile.close()
conn.close()
s.close()
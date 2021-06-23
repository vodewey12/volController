from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import serial
from ctypes import cast, POINTER, pointer
from comtypes import CLSCTX_ALL, GUID
import serial

ser = serial.Serial('COM5', 9600)
print("connected to: " + ser.portstr)
count = 1
lpcguid = pointer(GUID.create_new())
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


while True:
    cc = str(ser.readline())
    volume.SetMasterVolumeLevelScalar((float(cc[2:][:-5])/1023.0), None)


ser.close()

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import serial
from ctypes import cast, POINTER, pointer
from comtypes import CLSCTX_ALL, GUID
import serial


class volController(object):

    def __init__(self, serial_port):
        self.serial_port = serial_port

        self._stopped = False

    def start(self):
        ser = serial.Serial(self.serial_port, 9600)

        sessions = AudioUtilities.GetAllSessions()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        while not self._stopped:
            cc = str(ser.readline())
            self.changeVolume(volume, float(cc[2:][:-5])/1023.0)

    def changeVolume(self, volume, decibles):
        volume.SetMasterVolumeLevelScalar(decibles, None)


def attempt_print(s):
    try:
        print(s)
    except:
        pass


def main():
    volume_controller = volController('COM5')
    try:
        volume_controller.start()
    finally:
        attempt_print("Bye!")


if __name__ == "__main__":
    main()

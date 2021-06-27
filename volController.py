from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import serial
from ctypes import cast, POINTER, pointer
from comtypes import CLSCTX_ALL, GUID
import serial
import sounddevice as sd


class volController(object):

    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.currentOutputDevice = ""
        self._stopped = False

    def start(self):
        self.checkCurrentDevice()
        ser = serial.Serial(self.serial_port, 9600)
        sessions = AudioUtilities.GetAllSessions()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        while not self._stopped:
            if sd.query_devices()[sd.default.device[1]]['name'] != self.currentOutputDevice:
                self.currentOutputDevice = sd.query_devices(
                )[sd.default.device[1]]['name']
            cc = str(ser.readline())
            self.changeVolume(volume, float(cc[2:][:-5])/1023.0)

    def checkCurrentDevice(self):
        self.currentOutputDevice = sd.query_devices()[
            sd.default.device[1]]['name']

    def changeVolume(self, volume, decibles):
        volume.SetMasterVolumeLevelScalar(decibles, None)


def attemptPrint(s):
    try:
        print(s)
    except:
        pass


def main():
    volume_controller = volController('COM5')
    try:
        volume_controller.start()
    finally:
        attemptPrint("Bye!")


if __name__ == "__main__":
    main()

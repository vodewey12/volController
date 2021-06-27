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
        self.sessions = AudioUtilities.GetAllSessions()
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

    def start(self):
        self.checkCurrentDevice()
        ser = serial.Serial(self.serial_port, 9600)
        while not self._stopped:
            '''print(sd.query_devices()[sd.default.device[1]]['name'])
            if sd.query_devices()[sd.default.device[1]]['name'] != self.currentOutputDevice:
                self.refreshController()
                self.currentOutputDevice = sd.query_devices(
                )[sd.default.device[1]]['name']
                print("hello")
                '''
            cc = str(ser.readline())[2:][:-5].split("|")
            button = int(cc[0])
            master_volume = float(cc[1])/1023.0
            if button == 1:
                self.refreshController()
            self.changeVolume(self.volume, float(master_volume))

    def checkCurrentDevice(self):
        self.currentOutputDevice = sd.query_devices()[
            sd.default.device[1]]['name']

    def refreshController(self):
        newDevices = AudioUtilities.GetSpeakers()
        newInterface = newDevices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(newInterface, POINTER(IAudioEndpointVolume))

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

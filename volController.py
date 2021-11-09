from __future__ import print_function
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import serial
from ctypes import cast, POINTER, pointer
from comtypes import CLSCTX_ALL, GUID


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
        ser = serial.Serial(self.serial_port, 9600)
        while not self._stopped:
            cc = str(ser.readline())[2:][:-5].split("|")
            button = int(cc[0])
            master_volume = float(cc[1])/1023.0
            app1_volume = float(cc[2])/1023.0
            app2_volume = float(cc[3])/1023.0
            if button == 1:
                self.refreshController()
            self.changeVolume(self.volume, float(master_volume))

            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                app = session._ctl.QueryInterface(ISimpleAudioVolume)
                if (session.Process and session.Process.name() == "firefox.exe"):
                    app.SetMasterVolume(app1_volume, None)
                if session.Process and (session.Process.name() == "TEW2.exe" or session.Process.name() == "Spotify.exe" or
                                        session.Process.name() == "ForzaHorizon4.exe" or session.Process.name() == "za4_dx12.exe"):
                    app.SetMasterVolume(app2_volume, None)

    def refreshController(self):
        newDevices = AudioUtilities.GetSpeakers()
        newInterface = newDevices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(newInterface, POINTER(IAudioEndpointVolume))

    def changeVolume(self, volume, decibles):
        volume.SetMasterVolumeLevelScalar(decibles, None)

    def setApp1Volume(self, volume):
        self.app1.volume = volume


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

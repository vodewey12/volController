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
        self.muteVar = 0

    def start(self):
        ser = serial.Serial(self.serial_port, 9600)
        while not self._stopped:

            cc = str(ser.readline())[2:][:-5].split("|")
            button = cc[4]
            master_volume = float(cc[0])/1023.0
            app1_volume = float(cc[1])/1023.0
            app2_volume = float(cc[2])/1023.0
            app3_volume = float(cc[3])/1023.0

            if button == "Key pressed 6":
                self.refreshController()
            self.changeVolume(self.volume, float(master_volume))
            if button == "Key pressed 5":
                self.setMute(self.volume)
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                app = session._ctl.QueryInterface(ISimpleAudioVolume)
                if (session.Process and session.Process.name() == "firefox.exe"):
                    app.SetMasterVolume(app1_volume, None)
                if session.Process and (session.Process.name() == "TEW2.exe" or
                                        session.Process.name() == "ForzaHorizon5.exe" or session.Process.name() == "za4_dx12.exe"):
                    app.SetMasterVolume(app2_volume, None)
                if session.Process and (session.Process.name() == "Spotify.exe"):
                    app.SetMasterVolume(app3_volume, None)

    def refreshController(self):
        newDevices = AudioUtilities.GetSpeakers()
        newInterface = newDevices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(newInterface, POINTER(IAudioEndpointVolume))

    def changeVolume(self, volume, decibles):
        volume.SetMasterVolumeLevelScalar(decibles, None)

    def setMute(self, volume):
        self.muteVar ^= 1
        volume.SetMute(self.muteVar, None)

    def setApp1Volume(self, volume):
        self.app1.volume = volume


def attemptPrint(s):
    try:
        print(s)
    except:
        pass


def main():
    volume_controller = volController('COM6')
    try:
        volume_controller.start()
    finally:
        attemptPrint("Bye!")


if __name__ == "__main__":
    main()

import subprocess
from time import sleep
from nanoleafapi import Nanoleaf
from nanoleafapi import RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE

CAMERA_MODULE = "uvcvideo"
NANOLEAF_IP = "192.168.0.124"


def is_camera_used():
    """Returns true is camera is in use

    Look into the output of lsmod and see what if the camera kernel
    module is open somewhere
    """

    proc = subprocess.Popen(
        "lsmod", stdout=subprocess.PIPE, universal_newlines=True)
    kernel_modules = proc.communicate()[0].split("\n")
    for kernel_module in kernel_modules:
        output = ' '.join(kernel_module.split()).split()
        if output[0] == CAMERA_MODULE:
            return int(output[2]) > 0
    raise

class MeetingIndicator(object):

    def __init__(self, ip):
        self.nl = Nanoleaf(ip)
        self.init_time_color_mode = self.nl.get_color_mode()  # can be "hs" or "effect"
        self.init_time_effect = self.nl.get_current_effect()  # "*Solid" or effect
        self.init_time_brightness = self.nl.get_brightness()

    def set_camera_in_use(self):
        self.nl.set_color(RED)

    def set_no_meeting(self):
        self.nl.set_color(WHITE)


def main():

    meeting_indicator = MeetingIndicator(NANOLEAF_IP)
    while True:
        if is_camera_used():
            meeting_indicator.set_camera_in_use()
        else:
            meeting_indicator.set_no_meeting()
        sleep(2)


if __name__ == "__main__":
    main()

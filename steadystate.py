#!/usr/bin/env python3
from psychopy import visual, core, event, logging, prefs
from random import shuffle
import psychtoolbox as ptb

prefs.hardware["audioLib"] = ["PTB", "pyo", "pygame"]
from psychopy.sound import Sound


"""
Steady State Auditory task
play 3 tones 150 times each in a block (not interleaved)

port of Presentation to psychopy

Using functions cribbed from MGSEncMem:
https://github.com/LabNeuroCogDevel/mgs_encode_memory.py
"""


def pt(msg):
    print("[%.02f] %s" % (core.getTime(), msg))


def wait_until(stoptime, maxwait=30):
    """
    just like core.wait, but instead of waiting a duration
    we wait until a stoptime.
    optional maxwait will throw an error if we are wating too long
    so we dont get stuck. defaults to 30 seconds
    """
    if stoptime - core.getTime() > maxwait:
        raise ValueError(
            "request to wait until stoptime is more than "
            + "30 seconds, secify maxwait to avoid this error"
        )
    # will hog cpu -- no pyglet.media.dispatch_events here
    while core.getTime() < stoptime:
        continue


def create_window(fullscr, screen=0):
    """create window either fullscreen or 800,600
    hide mouse cursor and make active
    """
    # setup screen
    if fullscr:
        win = visual.Window(fullscr=fullscr, screen=screen)
    else:
        win = visual.Window([800, 600])

    win.winHandle.activate()  # make sure the display window has focus
    win.mouseVisible = False  # and that we don't see the mouse

    # -- change color to black --
    win.color = (-1, -1, -1)
    # flip twice to get the color
    win.flip()
    win.flip()
    return win


class SteadyState:
    def __init__(self):
        "start up the task and load up what we need"
        self.usePP = True
        self.zeroTTL = True
        self.verbose = False
        self.fullscreen = True
        # self.pp_address=0xDFF8
        # 2023-02-20
        self.pp_address = 0xD010

        # load up
        self.init_pp()
        self.sound = {x: Sound("click-%sHzTrain.wav" % x) for x in ["20", "30", "40"]}

        self.win = create_window(self.fullscreen)
        # a fixation cross with 2x normal size
        self.cross = visual.TextStim(
            self.win, text="+", name="iti_fixation", color="white", bold=True
        )
        self.cross.size = 2

        # flip and draw fixation cross
        self.cross.draw()
        self.win.flip()

    def init_pp(self):
        "initialize parallel port if we want it"
        if not self.usePP:
            return
        # initialize parallel port
        if not hasattr(self, "port"):
            # might need to 'pip install pyparallel'
            from psychopy import parallel

            self.port = parallel.ParallelPort(address=self.pp_address)

    def send_ttl(self, thistrigger):
        """
        send ttl trigger to parallel port (setup by init_pp)
        wait (block) 10ms and send 0
        """
        if not self.usePP:
            pt("\tnot sending %d" % thistrigger)
            return
        thistrigger = int(thistrigger)
        self.port.setData(thistrigger)
        if self.verbose:
            print("eeg code %s" % thistrigger)
        if self.zeroTTL:
            core.wait(0.01)  # wait 10ms and send zero
            self.port.setData(0)

    def play_snd(self, snd, when):
        self.sound[snd].stop()
        self.sound[snd].play(when=when)

    def instructions(self):
        # todo. text is too large?
        self.cross.text = "SteadyState. Ready?"
        self.cross.draw()
        self.win.flip()
        event.waitKeys()

        # same screen for duration of task
        self.cross.text = ""  # not "+". but just empty black screen
        self.cross.draw()
        self.win.flip()


if __name__ == "__main__":
    n_each = 150
    dur = 1.1
    order = ["20", "30", "40"]

    # 20221207 - is totally random okay?
    shuffle(order)
    print(f"Order: {order}")

    t = SteadyState()

    t.instructions()

    start = core.getTime()
    first_wait = 1.5  # seconds
    times = [start + first_wait + i * dur for i in range(n_each * len(order))]

    pt("start")
    t.send_ttl(128)

    # 3 different train frequencies
    for sndi, snd in enumerate(order):
        ttl = int(snd) / 10

        # 150 of each
        for i in range(n_each):
            ii = sndi * n_each + i
            stime = times[ii]

            t.play_snd(snd, stime)
            wait_until(stime - 0.001)
            t.send_ttl(ttl)

            pt("%d: %s %d (ideal %.02f)" % (ii, snd, i, stime))

    t.send_ttl(129)
    pt("done")

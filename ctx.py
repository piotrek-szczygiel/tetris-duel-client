from dataclasses import dataclass


@dataclass
class Ctx:
    running = True
    now = 0.0

    surface = None
    font = None
    debug_font = None

    mixer = None


ctx = Ctx()

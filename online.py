import socket
from random import randint
from typing import Optional, Callable, List
from text import Text
from ctx import ctx
import jsonpickle
import protocol
import select
from config import config
from gameplay import Gameplay
from popup import Popup
from state import State
from device import Device

BUFFER_SIZE = 1024


class Online(State):
    def __init__(self) -> None:
        self.gameplay1 = Gameplay()
        self.gameplay2 = Gameplay()

        self.popups1: List[Popup] = []
        self.popups2: List[Popup] = []
        self.current_popup1: Optional[Popup] = None
        self.current_popup2: Optional[Popup] = None

        self.waiting = True
        self.waiting_cycle = 0
        self.last_waiting_cycle = ctx.now

        self.buffer = b""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2.0)

        self.finished = False
        self.end_screen = False

    def is_finished(self) -> bool:
        return self.finished

    def initialize(self) -> None:
        self.gameplay1.set_device(ctx.device1)
        self.gameplay1.initialize()

        self.gameplay2.set_device(Device("dummy"))
        self.gameplay2.initialize()

        try:
            self.socket.connect(config.server)
        except (ConnectionRefusedError, socket.timeout):
            print("unable to connect to server")
            self.finished = True

    def update(self, switch_state: Callable) -> None:
        read, write, error = select.select(
            [self.socket], [self.socket], [self.socket], 0
        )

        if self.waiting:
            self.gameplay1.cancel_input.update()

            if self.socket in read:
                buffer = self.socket.recv(BUFFER_SIZE)
                if buffer == b"go":
                    self.waiting = False
                    self.current_popup2 = None
                elif buffer == b"ping":
                    self.socket.sendall(b"pong")
                elif buffer == b"":
                    print("server disconnected")
                    self.finished = True
            elif self.gameplay1.cancel:
                self.socket.close()
                self.finished = True

            return

        if not self.end_screen:
            if self.gameplay1.game_over and not self.gameplay2.game_over:
                self.gameplay2.game_over = True
                self.end_screen = True
                self.popups1.append(
                    Popup("You lost!", color="red", gcolor="orange")
                )
                self.popups2.append(
                    Popup("You won!", color="green", gcolor="yellow")
                )
            elif self.gameplay2.game_over and not self.gameplay1.game_over:
                self.gameplay1.game_over = True
                self.end_screen = True
                self.popups1.append(
                    Popup("You won!", color="green", gcolor="yellow")
                )
                self.popups2.append(
                    Popup("You lost!", color="red", gcolor="orange")
                )
            elif self.gameplay1.game_over and self.gameplay2.game_over:
                self.end_screen = True
                self.popups1.append(Popup("Draw!", color="cyan"))
                self.popups2.append(Popup("Draw!", color="cyan"))

        if self.gameplay1.cancel:
            self.gameplay1.send = True

            self.gameplay1.cancel = False
            self.gameplay1.game_over = True

            if self.end_screen or self.gameplay1.countdown > 0:
                self.finished = True

        self.gameplay1.update()

        if self.socket in read:
            try:
                self.gameplay2 = jsonpickle.decode(
                    protocol.recv(self.socket).decode()
                )
            except (RuntimeError, ConnectionResetError):
                error = [self.socket]

        if self.socket in write and self.gameplay1.send:
            self.gameplay1.send = False
            try:
                protocol.send(
                    self.socket, jsonpickle.encode(self.gameplay1).encode()
                )
            except (ConnectionResetError, ConnectionAbortedError):
                error = [self.socket]

        if self.socket in error:
            if not self.end_screen:
                print("communication error")
                self.finished = True

        if self.gameplay2.score.duel_lines > 0:
            hole = randint(0, 9)
            self.gameplay1.add_garbage(hole, self.gameplay2.score.duel_lines)
            self.gameplay2.score.duel_lines = 0

        self.gameplay1.score.duel_lines = 0

        self.popups1.extend(self.gameplay1.get_popups())
        self.gameplay1.clear_popups()

        self.popups2.extend(self.gameplay2.get_popups())
        self.gameplay2.clear_popups()

        if not self.current_popup1 and self.popups1:
            self.current_popup1 = self.popups1.pop(0)
        elif self.current_popup1:
            if not self.current_popup1.update():
                self.current_popup1 = None

        if not self.current_popup2 and self.popups2:
            self.current_popup2 = self.popups2.pop(0)
        elif self.current_popup2:
            if not self.current_popup2.update():
                self.current_popup2 = None

    def draw(self) -> None:
        self.gameplay1.draw(130, 80)
        self.gameplay2.draw(880, 80, draw_piece=not self.waiting)

        if self.waiting:
            Text.draw("Awaiting", size=4, centerx=880 + 155, top=220)
            Text.draw(
                "opponent", size=4, gcolor="red", centerx=880 + 155, top=280
            )

            string = "." * self.waiting_cycle

            Text.draw(
                string, size=8, gcolor="black", centerx=880 + 155, top=350
            )

            if ctx.now - self.last_waiting_cycle > 0.5:
                self.last_waiting_cycle = ctx.now
                self.waiting_cycle = (self.waiting_cycle + 1) % 4

        if self.current_popup1:
            self.current_popup1.draw(130 + 155, 80 + 220)

        if self.current_popup2:
            self.current_popup2.draw(880 + 155, 80 + 220)

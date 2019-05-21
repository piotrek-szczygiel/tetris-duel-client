import socket
from pygame.locals import K_ESCAPE
from random import randint
from typing import Optional, Callable, List
from text import Text
from ctx import ctx
import jsonpickle
import protocol
import select
import config
from gameplay import Gameplay
from popup import Popup
from input import Input
from state import State

BUFFER_SIZE = 1024


class Online(State):
    def __init__(self) -> None:
        self.input = Input(Input.KEYBOARD)

        self.gameplay1 = Gameplay(config.input_player1)
        self.gameplay2 = Gameplay(config.input_player1)

        self.popups1: List[Popup] = []
        self.popups2: List[Popup] = []
        self.current_popup1: Optional[Popup] = None
        self.current_popup2: Optional[Popup] = None

        self.waiting = True
        self.waiting_cycle = 0
        self.last_waiting_cycle = ctx.now
        self.ending = False

        self.buffer = b""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2.0)

        self.cancel = False
        self.done = False
        self.game_over = False

    def is_done(self) -> bool:
        return self.done

    def initialize(self) -> None:
        self.gameplay1.initialize()
        self.gameplay2.initialize()

        self.input.subscribe_list([(K_ESCAPE, self.waiting_cancel)])

        try:
            self.socket.connect(config.server)
        except (ConnectionRefusedError, socket.timeout):
            print("unable to connect to server")
            self.done = True

    def waiting_cancel(self) -> None:
        if self.waiting:
            self.done = True
            self.socket.close()
        else:
            self.cancel = True

    def update(self, switch_state: Callable) -> None:
        self.input.update()
        if self.done:
            return

        if not self.waiting:
            self.gameplay1.update()

        read, write, error = select.select(
            [self.socket], [self.socket], [self.socket]
        )

        if self.waiting:
            if self.socket in read:
                buffer = self.socket.recv(BUFFER_SIZE)
                if buffer == b"go":
                    self.waiting = False
                    self.currnet_popup2 = None
                elif buffer == b"ping":
                    self.socket.sendall(b"pong")
                elif buffer == b"":
                    print("server disconnected")
                    self.done = True

            return

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
            print("socket error")
            self.done = True
            return

        if not self.game_over:
            if self.gameplay1.is_over() and not self.gameplay2.is_over():
                self.gameplay2.set_over()
                self.game_over = True
                self.popups1.append(
                    Popup("You lost!", color="red", gcolor="orange")
                )
                self.popups2.append(
                    Popup("You won!", color="green", gcolor="yellow")
                )
            elif self.gameplay2.is_over() and not self.gameplay1.is_over():
                self.gameplay1.set_over()
                self.game_over = True
                self.popups1.append(
                    Popup("You won!", color="green", gcolor="yellow")
                )
                self.popups2.append(
                    Popup("You lost!", color="red", gcolor="orange")
                )
            elif self.gameplay1.is_over() and self.gameplay2.is_over():
                self.game_over = True
                self.popups1.append(Popup("Draw!", color="cyan"))
                self.popups2.append(Popup("Draw!", color="cyan"))
        elif self.game_over and self.cancel:
            self.socket.close()
            self.done = True
            return

        if self.cancel:
            self.cancel = False
            self.gameplay1.set_over()

        self.gameplay1.score.duel_lines = 0

        if self.gameplay2.score.duel_lines > 0:
            hole = randint(0, 9)
            self.gameplay1.add_garbage(hole, self.gameplay2.score.duel_lines)
            self.gameplay2.score.duel_lines = 0

        self.popups1.extend(self.gameplay1.get_popups())
        self.gameplay1.clear_popups()

        foreign_popups = self.gameplay2.get_popups()
        for popup in foreign_popups:
            popup.start = ctx.now

        self.popups2.extend(foreign_popups)
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

import socket
from random import randint
from typing import Optional, Callable, List
import jsonpickle
import protocol
import select
import config
from gameplay import Gameplay
from popup import Popup
from state import State

BUFFER_SIZE = 1024


class Online(State):
    def __init__(self) -> None:
        self.gameplay1 = Gameplay(config.input_player1)
        self.gameplay2 = Gameplay(config.input_player1)

        self.popups1: List[Popup] = []
        self.popups2: List[Popup] = []
        self.current_popup1: Optional[Popup] = None
        self.current_popup2: Optional[Popup] = None

        self.waiting = True
        self.ending = False

        self.buffer = b""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2.0)

        self.done = False
        self.game_over = False

    def __del__(self) -> None:
        self.socket.close()

    def is_done(self) -> bool:
        return self.done

    def initialize(self) -> None:
        self.gameplay1.initialize()
        self.gameplay2.initialize()

        try:
            self.socket.connect(config.server)
        except (ConnectionRefusedError, socket.timeout):
            print("unable to connect to server")
            self.done = True

    def update(self, switch_state: Callable) -> None:
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

        if not self.waiting:
            self.gameplay1.update()

        read, write, error = select.select(
            [self.socket], [self.socket], [self.socket]
        )

        if self.waiting:
            if self.socket in read:
                if self.socket.recv(BUFFER_SIZE) == b"go!":
                    self.waiting = False

            return

        if self.socket in read:
            try:
                self.gameplay2 = jsonpickle.decode(
                    protocol.recv(self.socket).decode()
                )
            except RuntimeError:
                error = [self.socket]

        if self.socket in write and self.gameplay1.send:
            self.gameplay1.send = False
            protocol.send(
                self.socket, jsonpickle.encode(self.gameplay1).encode()
            )

        if self.socket in error:
            print("socket error")
            self.done = True

        if not self.game_over:
            if self.gameplay1.is_over() and not self.gameplay2.is_over():
                self.gameplay2.set_over()
                self.game_over = True
                self.popups1.append(
                    Popup(
                        "You lost!", duration=5.0, color="red", gcolor="orange"
                    )
                )
                self.popups2.append(
                    Popup(
                        "You won!",
                        duration=5.0,
                        color="green",
                        gcolor="yellow",
                    )
                )
            elif self.gameplay2.is_over() and not self.gameplay1.is_over():
                self.gameplay1.set_over()
                self.game_over = True
                self.popups1.append(
                    Popup(
                        "You won!",
                        duration=5.0,
                        color="green",
                        gcolor="yellow",
                    )
                )
                self.popups2.append(
                    Popup(
                        "You lost!", duration=5.0, color="red", gcolor="orange"
                    )
                )
            elif self.gameplay1.is_over() and self.gameplay2.is_over():
                self.game_over = True
                self.popups1.append(Popup("Draw!", duration=5.0, color="cyan"))
                self.popups2.append(Popup("Draw!", duration=5.0, color="cyan"))
        elif (
            self.game_over
            and not self.current_popup1
            and not self.current_popup2
        ):
            self.socket.close()
            self.done = True
            return

        self.popups1.extend(self.gameplay1.get_popups())
        self.gameplay1.clear_popups()

        self.popups2.extend(self.gameplay2.get_popups())
        self.gameplay2.clear_popups()

        self.gameplay1.score.duel_lines = 0

        if self.gameplay2.score.duel_lines > 0:
            hole = randint(0, 9)
            self.gameplay1.add_garbage(hole, self.gameplay2.score.duel_lines)
            self.gameplay2.score.duel_lines = 0

    def draw(self) -> None:
        self.gameplay1.draw(130, 80)
        self.gameplay2.draw(880, 80, draw_piece=not self.waiting)

        if self.waiting:
            self.current_popup2 = Popup(
                "waiting\nfor\nopponent\n...", size=4, duration=0.25
            )

        if self.current_popup1:
            self.current_popup1.draw(130 + 155, 80 + 220)

        if self.current_popup2:
            self.current_popup2.draw(880 + 155, 80 + 220)

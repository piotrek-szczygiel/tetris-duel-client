import pygame as pg
import toml
from device import Device
from resources import path
from typing import Any, Callable, List, MutableMapping, Optional
from input import Input
from state import State
from config import config
from ctx import ctx
from text import Text


class DevicePrompter(State):
    def __init__(self, state: State, players: int) -> None:
        self.state = state
        self.players = players
        self.done_players = 0

        self.controls: MutableMapping[str, Any] = dict()
        self.finished = False

        self.started = ctx.now
        self.last_joystick_refresh = 0.0

    def is_finished(self) -> bool:
        return self.finished

    def initialize(self) -> None:
        with open(path("controls.toml"), "r") as f:
            self.controls = toml.loads(f.read())

    def update(self, switch_state: Callable) -> None:
        if self.done_players == self.players:
            self.finished = True
            switch_state(self.state)
            return

        if ctx.now - self.started < 0.5:
            return

        device = self.get_active_device()
        if device is not None:
            self.started = ctx.now

            if self.done_players == 0:
                ctx.device1 = device
            elif self.done_players == 1:
                if ctx.device1.type == device.type:
                    if ctx.device1.joystick_num == device.joystick_num:
                        return

                ctx.device2 = device

            self.done_players += 1

    def draw(self) -> None:
        if self.players == 1:
            if self.done_players == 0:
                Text.draw(
                    "Press any button",
                    size=5,
                    gcolor="red",
                    centery=350,
                    centerx=650,
                )
        elif self.done_players == 0:
            Text.draw(
                "Player 1 press any button",
                size=5,
                gcolor="green",
                centery=350,
                centerx=650,
            )
        elif self.done_players == 1 and self.players == 2:
            Text.draw(
                "Player 2 press any button",
                size=5,
                gcolor="cyan",
                centery=350,
                centerx=650,
            )

    def get_active_device(self) -> Optional[Device]:
        if ctx.now - self.last_joystick_refresh > 1.0:
            pg.joystick.quit()
            self.last_joystick_refresh = ctx.now

        pg.joystick.init()
        devices: List[Device] = list()

        device_names: List[str] = list()
        if self.done_players == 0:
            device_names = [config.device1, config.device2]
        elif self.done_players == 1:
            device_names = [config.device2, config.device1]

        for device_name in device_names:
            if self.controls[device_name]["type"] == "keyboard":
                devices += [Device(device_name)]
            elif self.controls[device_name]["type"] == "joystick":
                for j in range(pg.joystick.get_count()):
                    devices += [Device(device_name, j)]

        inputs: List[Input] = list()
        for device in devices:
            inputs += [Input(device)]

        for input in inputs:
            if input.update():
                return input.device

        return None

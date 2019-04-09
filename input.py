from typing import Callable, Dict, List, Tuple

import pygame

import config
import ctx

Key = int


class Input:
    def __init__(self) -> None:
        self.pressed_keys: List[Key] = list()
        self.last_press: Dict[Key, float] = dict()
        self.last_repeat: Dict[Key, float] = dict()

        self.subscriptions: Dict[Key, Tuple[bool, Callable]] = dict()

    def subscribe(self, key: Key, repeat: bool, callback: Callable) -> None:
        self.subscriptions[key] = (repeat, callback)

    def update(self) -> None:
        self.pressed_keys = pygame.key.get_pressed()

        for key, (repeat, callback) in self.subscriptions.items():
            if self.key_pressed(key, repeat):
                callback()

    def key_pressed(self, key: Key, repeat: bool) -> bool:
        if not self.pressed_keys[key]:
            if key in self.last_press:
                del self.last_press[key]
            if key in self.last_repeat:
                del self.last_repeat[key]
            return False

        if key not in self.last_press:
            self.last_press[key] = ctx.now
            return True

        if not repeat:
            return False

        if ctx.now - self.last_press[key] < config.key_repeat_delay:
            return False

        if key not in self.last_repeat:
            self.last_repeat[key] = ctx.now
            return True

        if ctx.now - self.last_repeat[key] < config.key_repeat_interval:
            return False

        self.last_repeat[key] = ctx.now
        return True

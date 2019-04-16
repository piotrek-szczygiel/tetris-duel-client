from abc import ABC, abstractmethod
from typing import Callable


class State(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def update(self, switch_state: Callable) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

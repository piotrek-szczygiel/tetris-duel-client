from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def update(self) -> None: pass

    @abstractmethod
    def draw(self) -> None: pass

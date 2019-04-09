from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def is_running(self) -> bool:
        pass

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

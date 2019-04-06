from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def update(self): pass

    @abstractmethod
    def draw(self): pass

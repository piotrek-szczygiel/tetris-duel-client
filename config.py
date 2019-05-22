import toml

from resources import path


class Config:
    def __init__(self) -> None:
        with open(path("config.toml"), "r") as f:
            self.toml = toml.loads(f.read())

        self.window_size = (
            self.toml["window"]["width"],
            self.toml["window"]["height"],
        )

        self.background = self.toml["window"]["background_color"]

        self.key_repeat_delay = self.toml["input"]["repeat_delay"]
        self.key_repeat_interval = self.toml["input"]["repeat_interval"]

        self.device1 = self.toml["input"]["controls_1"]
        self.device2 = self.toml["input"]["controls_2"]

        self.server = (self.toml["online"]["ip"], self.toml["online"]["port"])


config = Config()

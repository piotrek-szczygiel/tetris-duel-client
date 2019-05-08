from ctx import ctx
from text import Text


class Popup:
    def __init__(
        self,
        text: str,
        duration=0.75,
        size=5,
        color="white",
        scolor="black",
        gcolor=None,
    ) -> None:
        self.text = text
        self.duration = duration
        self.size = size
        self.color = color
        self.scolor = scolor
        self.gcolor = gcolor or color

        self.fade = self.duration / 3
        self.alpha = 1.0

        self.start = ctx.now

    def update(self) -> bool:
        if self.start + self.duration < ctx.now:
            return False

        if self.start + self.duration - self.fade < ctx.now:
            ratio = (
                ctx.now - self.start - self.duration + self.fade
            ) / self.fade
            self.alpha = 1.0 - ratio ** 2

        return True

    def draw(self, x: int, y: int, center=True) -> None:
        if center:
            Text.draw(
                self.text,
                centerx=x,
                top=y,
                size=self.size,
                color=self.color,
                alpha=self.alpha,
                shadow=(2.0, 2.0),
                scolor=self.scolor,
                gcolor=self.gcolor,
                lineheight=2,
            )
        else:
            Text.draw(
                self.text,
                left=x,
                top=y,
                size=self.size,
                color=self.color,
                alpha=self.alpha,
                shadow=(2.0, 2.0),
                scolor=self.scolor,
                gcolor=self.gcolor,
                lineheight=2,
            )

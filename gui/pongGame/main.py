from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from random import randint


class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        # manage the ball when it touch the paddle
        if self.collide_widget(ball):
            speedup = 1.1

            # <- <- <-  ·  -> -> ->  --- ball's offset
            # ______________________ --- ball paddle
            offset = 0.02 * Vector(0, ball.center_y - self.center_y)
            ball.velocity = speedup * (offset - ball.velocity)

    def has_won(self, win_score=1):
        # return true if current player wins
        return self.score >= win_score


class PongBall(Widget):
    # velocity (speed) of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # 'move' function will move the ball one step. This
    # will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def reset_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(0, 0)

    def serve_ball(self, vel=(4, 0)):
        self.reset_ball()
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce the paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce off left and right
        if self.ball.x < self.x:
            self.player2.score += 1
            if self.player2.has_won():
                self.reset_ball()
                self.show_win(player="Player2")
            else:
                self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            if self.player1.has_won():
                self.reset_ball()
                self.show_win(player="Player1")
            else:
                self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width * 2 / 3:
            self.player2.center_y = touch.y

    def show_win(self, player: str):
        label = Label(text=f"{player} Win!", font_size=40)
        label.center_x = self.center_x
        label.top = self.top * 2 / 3
        self.add_widget(label)
        self.add_widget(Button())


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball(vel=Vector(4 * (-1 if randint(-1, 1) >= 0 else 1), 0))
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    PongApp().run()

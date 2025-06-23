# widgets/circle.py
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock

class CircularTimer(Widget):
    progress = NumericProperty(0)       # Float: 0.0 to 1.0
    display_text = StringProperty("0")  # The center time display

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas, progress=self.update_canvas, display_text=self.update_canvas)

        # Add a centered label
        self.label = Label(
            text=self.display_text,
            font_size='40sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.add_widget(self.label)
        Clock.schedule_interval(self.update_label_position, 0.1)

    def update_label_position(self, dt):
        self.label.center = self.center
        self.label.text = self.display_text

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.3, 0.3, 0.3, 1)
            Line(circle=(self.center_x, self.center_y, min(self.size) / 2 - 10), width=4)

            Color(0, 1, 0, 1)
            Line(circle=(self.center_x, self.center_y, min(self.size) / 2 - 10, 0, 360 * self.progress),
                 width=8, cap='round')

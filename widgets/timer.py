from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from .circle import CircularTimer

class HIITTimer(BoxLayout):
    current_time: int

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.circular = CircularTimer(size_hint=(1, 1))
        self.circular.opacity = 0
        self.add_widget(self.circular)

        self.phase = 'idle'
        self.current_time = 0
        self.rounds_left = 0
        self.total_rounds = 0
        self.work_time = 0
        self.rest_time = 0
        self.ready_time = 0
        self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)

        # Form layout
        self.form = GridLayout(cols=2, spacing=5, size_hint_y=None)
        self.form.bind(minimum_height=self.form.setter('height'))

        self.ready_input = TextInput(text="10", multiline=False, input_filter='int')
        self.work_input = TextInput(text="30", multiline=False, input_filter='int')
        self.rest_input = TextInput(text="15", multiline=False, input_filter='int')
        self.rounds_input = TextInput(text="5", multiline=False, input_filter='int')

        self.form.add_widget(Label(text="Get Ready Time (sec):", size_hint_y=None, height=40))
        self.form.add_widget(self.ready_input)
        self.form.add_widget(Label(text="Work Time (sec):", size_hint_y=None, height=40))
        self.form.add_widget(self.work_input)
        self.form.add_widget(Label(text="Rest Time (sec):", size_hint_y=None, height=40))
        self.form.add_widget(self.rest_input)
        self.form.add_widget(Label(text="Rounds:", size_hint_y=None, height=40))
        self.form.add_widget(self.rounds_input)

        self.add_widget(self.form)

        # Status label
        self.status_label = Label(
            text="[color=ffffff]Set your HIIT[/color]",
            font_size=32,
            markup=True,
            halign='center',
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.status_label)

        # Buttons
        self.button_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        self.start_button = Button(text="Start")
        self.stop_button = Button(text="Stop")
        self.reset_button = Button(text="Reset")

        self.start_button.bind(on_press=self.start_timer)
        self.stop_button.bind(on_press=self.stop_timer)
        self.reset_button.bind(on_press=self.reset_timer)

        self.button_layout.add_widget(self.start_button)
        self.button_layout.add_widget(self.stop_button)
        self.button_layout.add_widget(self.reset_button)

        self.add_widget(self.button_layout)

        self.set_running_ui(False)

    def set_running_ui(self, running: bool):
        self.form.opacity = 0 if running else 1
        self.form.disabled = running
        self.start_button.disabled = running
        self.circular.opacity = 1 if running else 0

    def reset_state(self):
        self.phase = 'idle'
        self.status_label.text = "[color=ffffff]Set your HIIT[/color]"
        self.rounds_left = 0
        self.total_rounds = 0
        self.work_time = 0
        self.rest_time = 0
        self.ready_time = 0
        self.current_time = 0
        self.set_running_ui(False)

    def start_timer(self, instance):
        try:
            self.work_time = int(self.work_input.text)
            self.rest_time = int(self.rest_input.text)
            self.total_rounds = int(self.rounds_input.text)
            self.ready_time = int(self.ready_input.text)
        except ValueError:
            self.status_label.text = "[color=ff0000]Enter valid numbers[/color]"
            return

        if self.total_rounds <= 0 or self.work_time <= 0 or self.rest_time < 0 or self.ready_time < 0:
            self.status_label.text = "[color=ff0000]All values must be > 0[/color]"
            return

        self.rounds_left = self.total_rounds
        self.phase = 'get_ready'
        self.current_time = self.ready_time
        self.set_running_ui(True)
        self.update_label()

        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer(self, instance):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
            self.status_label.text += " [Paused]"

    def reset_timer(self, instance):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.reset_state()

    def update_timer(self, dt):
        self.current_time -= dt

        # Round down to nearest whole second for display
        seconds_left = max(0, int(self.current_time))
        self.circular.display_text = str(seconds_left)

        if self.phase == 'get_ready':
            total = self.ready_time
            self.circular.progress = max(0, self.current_time / total)
            if self.current_time < 0:
                self.phase = 'work'
                self.current_time = self.work_time
                self.update_label()
            else:
                self.status_label.text = f"[color=00ffff]Get Ready: {seconds_left}s[/color]"
            return

        if self.phase == 'work':
            total = self.work_time
            self.circular.progress = max(0, self.current_time / total)
            if self.current_time < 0:
                self.phase = 'rest'
                self.current_time = self.rest_time
                self.update_label()
            else:
                self.update_label()
            return

        if self.phase == 'rest':
            total = self.rest_time
            self.circular.progress = max(0, self.current_time / total)
            if self.current_time < 0:
                self.rounds_left -= 1
                if self.rounds_left <= 0:
                    self.phase = 'done'
                    self.circular.progress = 0
                    self.circular.display_text = "Done"
                    self.update_label()
                    if self.timer_event:
                        self.timer_event.cancel()
                    return
                self.phase = 'work'
                self.current_time = self.work_time
                self.update_label()
            else:
                self.update_label()

    def update_label(self):
        round_num = self.total_rounds - self.rounds_left + 1
        if self.phase == 'work':
            self.status_label.text = f"[color=00ff00]Work: {self.current_time}s (Round {round_num}/{self.total_rounds})[/color]"
        elif self.phase == 'rest':
            self.status_label.text = f"[color=ffff00]Rest: {self.current_time}s (Round {round_num}/{self.total_rounds})[/color]"
        elif self.phase == 'done':
            self.status_label.text = "[color=ff0000]Workout Complete![/color]"
        elif self.phase == 'get_ready':
            self.status_label.text = f"[color=00ffff]Get Ready: {self.current_time}s[/color]"
        elif self.phase == 'idle':
            self.status_label.text = "[color=ffffff]Set your HIIT[/color]"

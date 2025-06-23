from kivy.app import App
from widgets import HIITTimer

class GymHIITApp(App):
    def build(self):
        return HIITTimer()

if __name__ == '__main__':
    GymHIITApp().run()
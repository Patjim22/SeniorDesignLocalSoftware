from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Container
import time


class Stopwatch(Static):
    def compose(self) -> ComposeResult:
        yield Label("Welcome",id="start")
        
    

class WelcomeApp(App):
    #Textual app to say hi.
    CSS_PATH = "textualTest.css"
    BINDINGS = [("d","toggle_dark","Toggle dark mode")]
    TITLE="Access Control"
    def compose(self)-> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(Stopwatch())
        
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
        

if __name__ == "__main__":
    app = WelcomeApp()
    app.run()
    Label.config(text= time.strftime("%I:%M:%S")) #displays time in 12 hour format
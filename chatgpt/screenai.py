from multiprocessing import Process, Pipe

import dash
from dash import html, ctx
from dash.dependencies import Input
import dash_bootstrap_components as dbc
from PIL import ImageGrab
import pytesseract
from pynput import mouse
import tkinter as tk
import numpy as np
from openai import OpenAI

from env import OPENAI_API_KEY


SIMULATE = False


def ask_llm(text, client):
    prompt = """
        You provice insights to the text you are given as bullet points.
        For algorithmic problems, only provide the the key aspects of the solution.
        Do not write code, do not repeat the question, keep it short and concise.
    """
    # remove \n, multiple spaces and leading spaces
    prompt = " ".join(prompt.split())

    text = text.strip()

    if SIMULATE:
        return prompt

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content


def get_mouse_position():
    with mouse.Controller() as controller:
        return controller.position
        
    
class RemoteRectSelector:
    """
    Starts a dash app allowing a user to select a rectangle on this device.
    
    Attributes
    ----------
    on_rect_selection : callable: (x1, y1), (x2, y2) -> None
    on_active_change: callable: bool -> None
    """

    def __init__(self, on_rect_selection, on_active_change):
        self.on_rect_selection = on_rect_selection
        self.on_active_change = on_active_change

        self.topleft = None
        self.bottomright = None

        self.make_app()

    def check_rect_available(self):
        if self.topleft is not None and self.bottomright is not None:
            tl = self.topleft
            br = self.bottomright
            self.topleft = None
            self.bottomright = None
            if tl[0] < br[0] and tl[1] < br[1]:
                self.on_rect_selection(tl, br)

    def make_app(self):
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )

        self.app.layout = dbc.Row([
            dbc.Col(html.Button("Top Left", id="tl", className="btn btn-primary btn-lg", style={"width": "100%", "height": "40vh"}), width=12, xs=6, md=3),
            dbc.Col(html.Button("Bottom Right", id="br", className="btn btn-secondary btn-lg", style={"width": "100%", "height": "40vh"}), width=12, xs=6, md=3),
            dbc.Col(html.Button("Show", id="show", className="btn btn-success btn-lg", style={"width": "100%", "height": "40vh"}), width=12, xs=6, md=3),
            dbc.Col(html.Button("Hide", id="hide", className="btn btn-danger btn-lg", style={"width": "100%", "height": "40vh"}), width=12, xs=6, md=3)
        ], justify="center", style={"height": "90vh"}),

        @self.app.callback(
            Input("tl", "n_clicks"),
            Input("br", "n_clicks"),
            Input("show", "n_clicks"),
            Input("hide", "n_clicks"),
        )
        def on_click(*args, **kwargs):
            print("Clicked: ", ctx.triggered_id)
            if "tl" == ctx.triggered_id:
                self.topleft = get_mouse_position()
            elif "br" == ctx.triggered_id:
                self.bottomright = get_mouse_position()
            elif "show" == ctx.triggered_id:
                self.on_active_change(True)
            elif "hide" == ctx.triggered_id:
                self.on_active_change(False)
            self.check_rect_available()

    def start(self):
        self.app.run(port=8050, host="0.0.0.0", debug=True, use_reloader=False)


class Overlay:
    """
    Always on top, transparent overlay for showing some text.
    """

    def __init__(self, text, alpha=1, width=400, height=200):
        self.lbl_pad = 10
        self.make_app(alpha, width, height)
        self.set_text(text)

    def make_app(self, alpha, width, height):
        self.root = tk.Tk()
        self.root.geometry(f'{width}x{height}')  # Set initial window size
        #self.root.overrideredirect(True)  # Remove window decorations (title bar, etc.)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", alpha)

        self.label = tk.Label(self.root, text="Placeholder", font=("Arial", 18), bg='black', fg='white', wraplength=width-2*self.lbl_pad)
        self.label.pack(fill='both', expand=True, padx=self.lbl_pad, pady=self.lbl_pad)

        self.root.bind("<Escape>", self.close)
        self.root.bind("<Button-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<Configure>", self.on_resize)

    def on_press(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def on_drag(self, event):
        x = self.root.winfo_x() + event.x - self._offset_x
        y = self.root.winfo_y() + event.y - self._offset_y
        self.root.geometry(f'+{x}+{y}')

    def on_resize(self, event):
        new_width = event.width
        self.label.config(wraplength=new_width - 20)  # Adjust wraplength to window width with padding

    def set_text(self, text):
        self.label.config(text=text)

    def close(self, event):
        self.root.destroy()

    def start(self, step_func, step_ms=100):
        self.step_func = step_func
        def step():
            self.step_func()
            self.root.after(step_ms, step)
        step()
        self.root.mainloop()


class ChildProcessOverlay:
    def __init__(self):
        self.active = False

    def start(self):
        if self.active: return
        self.active = True
        self.parent_conn, self.child_conn = Pipe()
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        overlay = Overlay("Empty placeholder")
        def step():
            if self.parent_conn.poll():
                text = self.parent_conn.recv()
                overlay.set_text(text)
        overlay.start(step)

    def set_text(self, text):
        if not self.active: return
        self.child_conn.send(text)

    def stop(self):
        if not self.active: return
        self.active = False
        self.process.terminate()


if __name__ == '__main__':
    overlay = ChildProcessOverlay()

    if not SIMULATE:
        client = OpenAI(api_key=OPENAI_API_KEY)
    else:
        client = None

    def on_select(topleft, bottomright):
        x1, y1 = topleft
        x2, y2 = bottomright
        print("Got selection: ", (x1, y1), (x2, y2))
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        print("Got screenshot")
        if not np.any(np.array(screenshot)):
            print("Empty screenshot, script and window must be on the same screen")
            return
        text = pytesseract.image_to_string(screenshot)
        print("Got OCR: ", text.replace("\n", " ").strip())
        response = ask_llm(text, client)
        print("Got response: ", response.replace("\n", " ").strip())
        overlay.set_text(response)

    def on_active(active):
        if active:
            overlay.start()
        else:
            overlay.stop()

    selector = RemoteRectSelector(on_select, on_active)
    selector.start()
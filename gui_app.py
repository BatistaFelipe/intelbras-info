#!/usr/bin/env python3

import tkinter as tk

from gui_controller import GuiController
from gui_view import GuiView


def main() -> None:
    root = tk.Tk()
    view = GuiView(root)
    GuiController(view)
    root.mainloop()


if __name__ == "__main__":
    main()

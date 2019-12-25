"""
Stephen Montague
CPSC-61200 Software Architecture
Fall 2019 - Term 2
Week 3 - Lab 3

A school-provided implementation of a calculator
using the Model-View-Controller design pattern.

Updated by student to handle multiple expressions,
added a new backspace key, added a decimal key,
added the ability to handle keyboard input,
and added UI format tweaks to the original.

"""
import tkinter as tk


# noinspection PyBroadException
class Model:
    """Model class, abstracts the core data of the MVC pattern,
    Model maintains updates data based on events/calls it receives
    from Controller. Dependency should be one-way, Controller to Model,
    in other words, Model functions should NOT actively call methods of
    Controller or View
    """
    # Class re-written by student to handle multiple expressions
    continues_expression = True
    operators = {'+', '-', '*', '/'}

    def __init__(self):
        self.expr = ''

    def event(self, x):
        if Model.continues_expression or x in Model.operators:
            self.expr += x
        else:
            self.expr = x
        Model.continues_expression = True

    def calculate(self):
        Model.continues_expression = False
        try:
            self.expr = str(eval(self.expr))
        except:
            self.expr = ''

    def clear(self):
        self.expr = ''

    def backspace(self):
        self.expr = self.expr[:-1]

    @property
    def value(self):
        return 0 if self.expr == '' else self.expr


class View:
    """View in the MVC pattern assumes role of rendering user
    interface to the user, and maintaining an up to date view as
    it handles user interaction it receives from Controller.
    """

    def _add_numbers_keypad(self, frame):
        # calculator display
        self.display = tk.Label(frame, text=0, width=12, height=1, anchor=tk.NE)
        self.display.grid(row=0, column=0, columnspan=10, pady=5)

        # calculator numbers pad
        self.one = tk.Button(frame, text="1")
        self.one.grid(row=1, column=0)

        self.two = tk.Button(frame, text="2")
        self.two.grid(row=1, column=1)

        self.three = tk.Button(frame, text="3")
        self.three.grid(row=1, column=2)

        self.four = tk.Button(frame, text="4")
        self.four.grid(row=2, column=0)

        self.five = tk.Button(frame, text="5")
        self.five.grid(row=2, column=1)

        self.six = tk.Button(frame, text="6")
        self.six.grid(row=2, column=2)

        self.seven = tk.Button(frame, text="7")
        self.seven.grid(row=3, column=0)

        self.eight = tk.Button(frame, text="8")
        self.eight.grid(row=3, column=1)

        self.nine = tk.Button(frame, text="9")
        self.nine.grid(row=3, column=2)

        self.zero = tk.Button(frame, text="0")
        self.zero.grid(row=4, column=1)

        self.decimal = tk.Button(frame, text=".")  # New "Decimal" button
        self.decimal.grid(row=4, column=5)

        self.backspace = tk.Button(frame, text="Back")  # New "Backspace" button
        self.backspace.grid(row=1, column=4, columnspan=20)

    def _add_operations_keypad(self, frame):
        # operations pad
        self.clear = tk.Button(frame, text="C")
        self.clear.grid(row=4, column=0)

        self.equal = tk.Button(frame, text="=")
        self.equal.grid(row=4, column=2)

        self.add = tk.Button(frame, text="+")
        self.add.grid(row=2, column=5)

        self.sub = tk.Button(frame, text="-")
        self.sub.grid(row=3, column=5)

        self.mul = tk.Button(frame, text="*")
        self.mul.grid(row=2, column=6)

        self.div = tk.Button(frame, text="/")
        self.div.grid(row=3, column=6)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MVC example: Calculator")

        self._frame = tk.Frame(self.root)
        self._frame.pack(pady=10)
        self._add_numbers_keypad(self._frame)
        self._add_operations_keypad(self._frame)

    def refresh(self, value):
        self.display.config(text=value)

    def attach_keyboard(self, callback):
        self.root.bind("<Key>", callback)

    def start(self):
        self.root.mainloop()


class Controller:
    """Controller is the primary coordinator in the MVC patter, it collects
    user input, initiates necessary changes to model (data), and refreshes
    view to reflect any changes that might have happened."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.one.bind("<Button>", lambda event, n=1: self.num_callback(n))
        self.view.two.bind("<Button>", lambda event, n=2: self.num_callback(n))
        self.view.three.bind("<Button>", lambda event, n=3: self.num_callback(n))
        self.view.four.bind("<Button>", lambda event, n=4: self.num_callback(n))
        self.view.five.bind("<Button>", lambda event, n=5: self.num_callback(n))
        self.view.six.bind("<Button>", lambda event, n=6: self.num_callback(n))
        self.view.seven.bind("<Button>", lambda event, n=7: self.num_callback(n))
        self.view.eight.bind("<Button>", lambda event, n=8: self.num_callback(n))
        self.view.nine.bind("<Button>", lambda event, n=9: self.num_callback(n))
        self.view.zero.bind("<Button>", lambda event, n=0: self.num_callback(n))
        self.view.decimal.bind("<Button>", lambda event, n='.': self.num_callback(n))  # New "Decimal" binding
        self.view.add.bind("<Button>", lambda event, op='+': self.operation_callback(op))
        self.view.sub.bind("<Button>", lambda event, op='-': self.operation_callback(op))
        self.view.mul.bind("<Button>", lambda event, op='*': self.operation_callback(op))
        self.view.div.bind("<Button>", lambda event, op='/': self.operation_callback(op))
        self.view.equal.bind("<Button>", self.equal)
        self.view.clear.bind("<Button>", self.clear)
        self.view.backspace.bind("<Button>", self.backspace)  # New "Backspace" binding
        self.view.attach_keyboard(self.keystroke_callback)

    def keystroke_callback(self, event):
        """This is where you handle keystroke events from user,
        controller should invoke necessary methods on view and
        refresh view"""
        if event.keysym == 'Return':
            self.model.calculate()
        elif event.keysym == 'BackSpace':
            self.model.backspace()
        elif event.keysym == 'Escape':
            self.model.clear()
        else:
            self.model.event(event.char)
        self.view.refresh(self.model.value)
        print('keystroke: {}'.format(event.keysym))

    def num_callback(self, num):
        self.model.event(str(num))
        self.view.refresh(self.model.value)
        print('number {} is clicked'.format(num))

    def operation_callback(self, operation):
        self.model.event(operation)
        self.view.refresh(self.model.value)
        print('operation: {}'.format(operation))

    def equal(self, event):
        self.model.calculate()
        self.view.refresh(self.model.value)
        print('equal pressed')

    def clear(self, event):
        self.model.clear()
        self.view.refresh(self.model.value)

    def backspace(self, event):
        self.model.backspace()
        self.view.refresh(self.model.value)

    def run(self):
        self.view.start()


if __name__ == '__main__':
    ''' Main function, instantiate instances of Model, View and a Controller'''
    model = Model()
    view = View()
    controller = Controller(model=model, view=view)
    controller.run()

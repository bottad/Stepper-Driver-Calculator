import tkinter as tk
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
scalingFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

# Setting window size according to screen size and placing the window centered horizontally and slightly raised vertically
windowsize = str(str(int(screensize[0]*scalingFactor*1/4))+'x'+str(int(screensize[1]*scalingFactor*1/3))+'+'+str(int(screensize[0]*scalingFactor*1/8))+'+'+str(int(screensize[1]*scalingFactor*1/12)))

padding = int(10*scalingFactor)

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class App(tk.Tk):
    def __init__(self): #constructor
        super().__init__()

        # main setup
        self.config(bg='#272829')
        self.title("Stepper-Driver Current Calculator")
        self.iconbitmap("") #"./icon.ico" does not work as a onefile executable
        self.geometry(windowsize)
        self.minsize(640, 480)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.turned_on = True
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # widgets
        self.mainMenu = MainMenu(self)
        self.mainMenu.grid(row=0, column=0, sticky="nsew")

        #run
        while(self.turned_on):
            self.update()

    def on_close(self):
        self.turned_on  = False
        self.destroy()
        assert('terminated successfully!')

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#272829')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=30)

        label = tk.Label(self, text="Stepper Driver Type:", font=('Arial', 18), bg='#0F4C75')
        label.grid(row=0, column=0, sticky="nsew", pady=padding, padx=padding)

        # Stepper Driver Type Options (Dropdown Menu)
        self.driver_types = tk.StringVar()
        self.driver_types.set("Select Type")
        types_options = ["A4899", "DRV8825", "TMC2208", "TMC2209"]
        dropdown_type = tk.OptionMenu(self, self.driver_types, *types_options, command=self.change_frame)
        dropdown_type.config(bg='#0F4C75', fg='white', font=('Arial', 12))
        dropdown_type.grid(row=1, column=0, sticky="nsew", padx=padding)
        self.driver_types.set(types_options[0])

        # Frames for different drivers
        self.frame_A4988 = A4988Frame(self)
        self.frame_DRV8825 = DRV8825Frame(self)
        self.frame_TMC2208 = TMC2208Frame(self)
        self.frame_TMC2209 = TMC2209Frame(self)

        # initialize with A4899
        self.frame_A4988.grid(row=2, column=0, sticky="nsew", pady=padding, padx=padding)
        self.frame_DRV8825.grid(row=2, column=0, sticky="nsew", pady=padding, padx=padding)
        self.frame_TMC2208.grid(row=2, column=0, sticky="nsew", pady=padding, padx=padding)
        self.frame_TMC2209.grid(row=2, column=0, sticky="nsew", pady=padding, padx=padding)
        self.frame_DRV8825.grid_remove()
        self.frame_TMC2208.grid_remove()
        self.frame_TMC2209.grid_remove()

    def change_frame(self, *args):
        selected_type = self.driver_types.get()

        # Hide all frames
        self.frame_A4988.grid_remove()
        self.frame_DRV8825.grid_remove()
        self.frame_TMC2208.grid_remove()
        self.frame_TMC2209.grid_remove()

        # Show selected frame
        if selected_type == "A4899":
            self.frame_A4988.grid()
        elif selected_type == "DRV8825":
            self.frame_DRV8825.grid()
        elif selected_type == "TMC2208":
            self.frame_TMC2208.grid()
        elif selected_type == "TMC2209":
            self.frame_TMC2209.grid()

class A4988Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#454545')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(3, weight=1)

        # Labels for input boxes
        label_current = tk.Label(self, text="Max Current per Phase:", font=('Arial', 12), bg='#454545', fg='white')
        label_margin = tk.Label(self, text="Safety Margin:", font=('Arial', 12), bg='#454545', fg='white')
        label_resistor = tk.Label(self, text="Resistor Value:", font=('Arial', 12), bg='#454545', fg='white')

        self.scale_current = tk.Scale(self, from_=0, to=2000, resolution=100, orient="horizontal", font=('Arial', 10), label="mA", showvalue=False, command=self.update_slider_labels)
        self.scale_margin = tk.Scale(self, from_=0, to=50, resolution=1, orient="horizontal", font=('Arial', 10), label="%", showvalue=False, command=self.update_slider_labels)
        self.resistor_options = ["0.05 Ω", "0.1 Ω", "0.068 Ω"]
        self.resistor_value = tk.StringVar()
        self.resistor_value.set(self.resistor_options[0])
        self.dropdown_resistor = tk.OptionMenu(self, self.resistor_value, *self.resistor_options, command=self.calculate_reference_voltage)
        self.scale_current.set(1000)
        self.scale_margin.set(20)

        # Output of calculation result
        self.result_frame = tk.Frame(self, bg='white', bd=2, relief=tk.GROOVE)
        self.result_frame.columnconfigure(0, weight=8)
        self.result_frame.columnconfigure(1, weight=4)
        self.result_frame.columnconfigure(2, weight=2)
        self.result_frame.rowconfigure(0, weight=1)
        self.result_frame.rowconfigure(1, weight=3)
        self.result_frame.rowconfigure(2, weight=1)
        empty_label1 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label2 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label3 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label1.grid(row=0, column=0, columnspan=3, sticky="ew")
        empty_label2.grid(row=2, column=0, columnspan=3, sticky="ew")
        empty_label3.grid(row=1, column=2, sticky="nsew")
        self.label_result = tk.Label(self.result_frame, text="Reference Voltage:", font=('Arial', 12), bg='#454545', fg='white', padx=padding*2, pady=padding, anchor="w")
        self.calculation_result = tk.Label(self.result_frame, text="", font=('Arial', 12), bg='white', fg='black', anchor="center")
        self.label_result.grid(row=1, column=0, sticky="ew")
        self.calculation_result.grid(row=1, column=1, sticky="ew")

        # Grid placement
        label_current.grid(row=0, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_current.grid(row=0, column=1, padx=padding, pady=padding, sticky="ew")
        label_margin.grid(row=1, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_margin.grid(row=1, column=1, padx=padding, pady=padding, sticky="ew")
        label_resistor.grid(row=2, column=0, padx=padding, pady=padding, sticky="w")
        self.dropdown_resistor.grid(row=2, column=1, padx=padding, pady=padding, sticky="ew")
        self.result_frame.grid(row=3, column=0, columnspan=2, padx=padding, pady=padding, sticky="sew")

        self.update_slider_labels()

        # Bind events to recalculate reference voltage
        self.scale_current.bind(func=self.calculate_reference_voltage())
        self.scale_margin.bind(func=self.calculate_reference_voltage())

    def update_slider_labels(self, value=None):
        # Append units to slider labels
        current_value = self.scale_current.get()
        self.scale_current.configure(label=f"{current_value} mA")

        margin_value = self.scale_margin.get()
        self.scale_margin.configure(label=f"{margin_value} %")

        self.calculate_reference_voltage()

    def calculate_reference_voltage(self, value=None):
        max_current_mA = float(self.scale_current.get())
        safety_margin = float(self.scale_margin.get())
        resistor_value_str = self.resistor_value.get()
        resistor_value_str = resistor_value_str.replace(" Ω", "")  # Strip the unit (Ω)
        resistor_value = float(resistor_value_str)
        max_current_A = max_current_mA / 1000 * (1 - safety_margin/100)  # Convert current from mA to A
        # Calculation
        reference_voltage = max_current_A * 8 * resistor_value
        self.calculation_result.config(text=f"{reference_voltage:.2f} V")


class DRV8825Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#454545')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(3, weight=1)

        # Labels for input boxes
        label_current = tk.Label(self, text="Max Current per Phase:", font=('Arial', 12), bg='#454545', fg='white')
        label_margin = tk.Label(self, text="Safety Margin:", font=('Arial', 12), bg='#454545', fg='white')
        empty_label = tk.Label(self, text="", font=('Arial', 12), bg='#454545')

        self.scale_current = tk.Scale(self, from_=0, to=2500, resolution=100, orient="horizontal", font=('Arial', 10), label="mA", showvalue=False, command=self.update_slider_labels)
        self.scale_margin = tk.Scale(self, from_=0, to=50, resolution=1, orient="horizontal", font=('Arial', 10), label="%", showvalue=False, command=self.update_slider_labels)
        self.scale_current.set(1000)
        self.scale_margin.set(20)

        # Output of calculation result
        self.result_frame = tk.Frame(self, bg='white', bd=2, relief=tk.GROOVE)
        self.result_frame.columnconfigure(0, weight=8)
        self.result_frame.columnconfigure(1, weight=4)
        self.result_frame.columnconfigure(2, weight=2)
        self.result_frame.rowconfigure(0, weight=1)
        self.result_frame.rowconfigure(1, weight=3)
        self.result_frame.rowconfigure(2, weight=1)
        empty_label1 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label2 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label3 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label1.grid(row=0, column=0, columnspan=3, sticky="ew")
        empty_label2.grid(row=2, column=0, columnspan=3, sticky="ew")
        empty_label3.grid(row=1, column=2, sticky="nsew")
        self.label_result = tk.Label(self.result_frame, text="Reference Voltage:", font=('Arial', 12), bg='#454545', fg='white', padx=padding*2, pady=padding, anchor="w")
        self.calculation_result = tk.Label(self.result_frame, text="", font=('Arial', 12), bg='white', fg='black', anchor="center")
        self.label_result.grid(row=1, column=0, sticky="ew")
        self.calculation_result.grid(row=1, column=1, sticky="ew")

        # Grid placement
        label_current.grid(row=0, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_current.grid(row=0, column=1, padx=padding, pady=padding, sticky="ew")
        label_margin.grid(row=1, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_margin.grid(row=1, column=1, padx=padding, pady=padding, sticky="ew")
        empty_label.grid(row=2, column=0, padx=padding, pady=padding, columnspan=2)
        self.result_frame.grid(row=3, column=0, columnspan=2, padx=padding, pady=padding, sticky="sew")

        self.update_slider_labels()

        # Bind events to recalculate reference voltage
        self.scale_current.bind(func=self.calculate_reference_voltage())
        self.scale_margin.bind(func=self.calculate_reference_voltage())

    def update_slider_labels(self, value=None):
        # Append units to slider labels
        current_value = self.scale_current.get()
        self.scale_current.configure(label=f"{current_value} mA")

        margin_value = self.scale_margin.get()
        self.scale_margin.configure(label=f"{margin_value} %")

        self.calculate_reference_voltage()

    def calculate_reference_voltage(self):
        max_current_mA = float(self.scale_current.get())
        safety_margin = float(self.scale_margin.get())
        max_current_A = max_current_mA / 1000 * (1 - safety_margin/100)  # Convert current from mA to A
        # Calculation
        reference_voltage = max_current_A / 2
        self.calculation_result.config(text=f"{reference_voltage:.2f} V")


class TMC2208Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#454545')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(3, weight=1)

        # Labels for input boxes
        label_current = tk.Label(self, text="Max Current per Phase:", font=('Arial', 12), bg='#454545', fg='white')
        label_margin = tk.Label(self, text="Safety Margin:", font=('Arial', 12), bg='#454545', fg='white')
        empty_label = tk.Label(self, text="", font=('Arial', 12), bg='#454545')

        self.scale_current = tk.Scale(self, from_=0, to=1200, resolution=100, orient="horizontal", font=('Arial', 10), label="mA", showvalue=False, command=self.update_slider_labels)
        self.scale_margin = tk.Scale(self, from_=0, to=50, resolution=1, orient="horizontal", font=('Arial', 10), label="%", showvalue=False, command=self.update_slider_labels)
        self.scale_current.set(1000)
        self.scale_margin.set(20)

        # Output of calculation result
        self.result_frame = tk.Frame(self, bg='white', bd=2, relief=tk.GROOVE)
        self.result_frame.columnconfigure(0, weight=8)
        self.result_frame.columnconfigure(1, weight=4)
        self.result_frame.columnconfigure(2, weight=2)
        self.result_frame.rowconfigure(0, weight=1)
        self.result_frame.rowconfigure(1, weight=3)
        self.result_frame.rowconfigure(2, weight=1)
        empty_label1 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label2 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label3 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label1.grid(row=0, column=0, columnspan=3, sticky="ew")
        empty_label2.grid(row=2, column=0, columnspan=3, sticky="ew")
        empty_label3.grid(row=1, column=2, sticky="nsew")
        self.label_result = tk.Label(self.result_frame, text="Reference Voltage:", font=('Arial', 12), bg='#454545', fg='white', padx=padding*2, pady=padding, anchor="w")
        self.calculation_result = tk.Label(self.result_frame, text="", font=('Arial', 12), bg='white', fg='black', anchor="center")
        self.label_result.grid(row=1, column=0, sticky="ew")
        self.calculation_result.grid(row=1, column=1, sticky="ew")

        # Grid placement
        label_current.grid(row=0, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_current.grid(row=0, column=1, padx=padding, pady=padding, sticky="ew")
        label_margin.grid(row=1, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_margin.grid(row=1, column=1, padx=padding, pady=padding, sticky="ew")
        empty_label.grid(row=2, column=0, padx=padding, pady=padding, columnspan=2)
        self.result_frame.grid(row=3, column=0, columnspan=2, padx=padding, pady=padding, sticky="sew")

        self.update_slider_labels()

        # Bind events to recalculate reference voltage
        self.scale_current.bind(func=self.calculate_reference_voltage())
        self.scale_margin.bind(func=self.calculate_reference_voltage())

    def update_slider_labels(self, value=None):
        # Append units to slider labels
        current_value = self.scale_current.get()
        self.scale_current.configure(label=f"{current_value} mA")

        margin_value = self.scale_margin.get()
        self.scale_margin.configure(label=f"{margin_value} %")

        self.calculate_reference_voltage()

    def calculate_reference_voltage(self):
        max_current_mA = float(self.scale_current.get())
        safety_margin = float(self.scale_margin.get())
        max_current_A = max_current_mA / 1000 * (1 - safety_margin/100) # Convert current from mA to A and include safety margin
        # Calculation
        reference_voltage = max_current_A * 1.41
        self.calculation_result.config(text=f"Reference Voltage: {reference_voltage:.2f} V")


class TMC2209Frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg='#454545')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(3, weight=1)

        # Labels for input boxes
        label_current = tk.Label(self, text="Max Current per Phase:", font=('Arial', 12), bg='#454545', fg='white')
        label_margin = tk.Label(self, text="Safety Margin:", font=('Arial', 12), bg='#454545', fg='white')
        empty_label = tk.Label(self, text="", font=('Arial', 12), bg='#454545')

        self.scale_current = tk.Scale(self, from_=0, to=2000, resolution=100, orient="horizontal", font=('Arial', 10), label="mA", showvalue=False, command=self.update_slider_labels)
        self.scale_margin = tk.Scale(self, from_=0, to=50, resolution=1, orient="horizontal", font=('Arial', 10), label="%", showvalue=False, command=self.update_slider_labels)
        self.scale_current.set(1000)
        self.scale_margin.set(20)

        # Output of calculation result
        self.result_frame = tk.Frame(self, bg='white', bd=2, relief=tk.GROOVE)
        self.result_frame.columnconfigure(0, weight=8)
        self.result_frame.columnconfigure(1, weight=4)
        self.result_frame.columnconfigure(2, weight=2)
        self.result_frame.rowconfigure(0, weight=1)
        self.result_frame.rowconfigure(1, weight=3)
        self.result_frame.rowconfigure(2, weight=1)
        empty_label1 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label2 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label3 = tk.Label(self.result_frame, text="", bg='#454545')
        empty_label1.grid(row=0, column=0, columnspan=3, sticky="ew")
        empty_label2.grid(row=2, column=0, columnspan=3, sticky="ew")
        empty_label3.grid(row=1, column=2, sticky="nsew")
        self.label_result = tk.Label(self.result_frame, text="Reference Voltage:", font=('Arial', 12), bg='#454545', fg='white', padx=padding*2, pady=padding, anchor="w")
        self.calculation_result = tk.Label(self.result_frame, text="", font=('Arial', 12), bg='white', fg='black', anchor="center")
        self.label_result.grid(row=1, column=0, sticky="ew")
        self.calculation_result.grid(row=1, column=1, sticky="ew")

        # Grid placement
        label_current.grid(row=0, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_current.grid(row=0, column=1, padx=padding, pady=padding, sticky="ew")
        label_margin.grid(row=1, column=0, padx=padding, pady=padding, sticky="w")
        self.scale_margin.grid(row=1, column=1, padx=padding, pady=padding, sticky="ew")
        empty_label.grid(row=2, column=0, padx=padding, pady=padding, columnspan=2)
        self.result_frame.grid(row=3, column=0, columnspan=2, padx=padding, pady=padding, sticky="sew")

        self.update_slider_labels()

        # Bind events to recalculate reference voltage
        self.scale_current.bind(func=self.calculate_reference_voltage())
        self.scale_margin.bind(func=self.calculate_reference_voltage())

    def update_slider_labels(self, value=None):
        # Append units to slider labels
        current_value = self.scale_current.get()
        self.scale_current.configure(label=f"{current_value} mA")

        margin_value = self.scale_margin.get()
        self.scale_margin.configure(label=f"{margin_value} %")

        self.calculate_reference_voltage()

    def calculate_reference_voltage(self):
        max_current_mA = float(self.scale_current.get())
        safety_margin = float(self.scale_margin.get())
        max_current_A = max_current_mA / 1000 * (1 - safety_margin/100) # Convert current from mA to A and include safety margin
        # Calculation
        reference_voltage = max_current_A * 1.41
        self.calculation_result.config(text=f"Reference Voltage: {reference_voltage:.2f} V")

######################## Main code: ########################

app = App()
app.mainloop()

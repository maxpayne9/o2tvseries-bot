#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from o2tvseries import *

#start coding here
class LabelInput(tk.Frame):
   """A widget containing a label and input together"""

   def __init__(self, parent, label='', input_class=ttk.Entry, input_var=None, input_args=None, label_args=None, **kwargs):
      super().__init__(parent, **kwargs)
      input_args = input_args or {}
      label_args = label_args or {}
      self.variable = input_var
   
      if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
         input_args["text"] = label
         input_args["variable"] = input_var
      else:
         self.label = ttk.Label(self, text=label, **label_args)
         self.label.grid(row=0, column=0, sticky=(tk.W+tk.E))
         input_args["textvariable"] = input_var
      
      self.input = input_class(self, **input_args)
      self.input.grid(row=1, column=0, sticky=(tk.W+tk.E))

      self.columnconfigure(0, weight=1)

   def grid(self, sticky=(tk.E+tk.W), **kwargs):
      super().grid(sticky=sticky, **kwargs)

   def get(self):
      try:
         if self.variable:
            return self.variable.get()
         elif type(self.input) == tk.Text:
            return self.input.get('1.0', tk.End)
         else:
            return self.input.get()
      except (TypeError, tk.TclError):
         #Happens when numeric fields are empty.
         return ''
   def set(self, value, *args, **kwargs):
      if type(self.variable) == tk.BooleanVar:
         self.variable.set(bool(value))
      elif self.variable:
         self.variable.set(value, *args, **kwargs)
      elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
         if value:
            self.input.select()
         else:
            self.input.deselect()
      elif type(self.input) == tk.Text:
         self.input.delete('1.0', END)
         self.input.insert('1.0', value)
      else: #input must be an entr-typr widget with no variable
         self.input.delete(0, tk.END)
         self.input.insert(0, value)

class DataRecordForm(tk.Frame):
   """The input form for our widgets"""

   def __init__(self, parent,*args, **kwargs):
      super().__init__(parent, *args, **kwargs)

      # a dict to keep tract of input widgets
      self.inputs = {}

      recordinfo = tk.LabelFrame(self, text='Record Information')

      self.inputs['Date'] = LabelInput(recordinfo, "Date", input_var=tk.StringVar())
      self.inputs['Date'].grid(row=0, column=0)

      self.inputs['Time'] = LabelInput(recordinfo, "Time", input_class=ttk.Combobox, input_var=tk.StringVar(), input_args={"values": ["8.00", "12.00", "16.00", "20.00"]})
      self.inputs['Time'].grid(row=0, column=1)

      self.inputs['Technician'] = LabelInput(recordinfo, "Technician" input_var=tk.StringVar())
      self.inputs['Technician'].grid(row=0, column=2)

class Application(tk.Tk):
   """Application root windows"""


if __name__ == '__main__':
   app=Application()
   app.mainloop()
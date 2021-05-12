#!/usr/bin/python3

from tkinter import *
from o2tvseries import *

class Home:
   const_dict = {}
   def __init__(self, master, *args, **kwargs):
      self.master = master
      self.heading = Label(master, text="Series Downloader", font=('arial 20 bold'))
      self.heading.place(x=200)

      self.search_bar = Entry(master, width=25, font=('arial 18 bold'))
      self.search_bar.place(x=50, y=50)
      self.search_bar.focus()

      self.search_btn = Button(master, text='Search', width=18, height=2, command=lambda: self.on_search())
      self.search_btn.place(x=430, y=50)

      self.results_lst = StringVar()
      self.results = Listbox(master, width=100, height=30, listvariable=self.results_lst)
      self.results.bind('<<ListboxSelect>>', self.item_selected)
      self.results.bind('<<ListboxSelect>>', self.mult_select, add='+')
      self.results.bind('<<ListboxSelect>>', self.list_refresh, add='+') #replaces previous handler
      self.results.place(x=20, y=100)

      self.downl_btn = Button(master, text='Download', command=None, width=20, height=2)
      self.downl_btn.place(x=20, y=600)

      self.save_to_frame= LabelFrame(master, text='Saving to...', width=400, height=50)
      self.save_to_frame.place(x=220, y=590)
      Label(self.save_to_frame, text='path/to/save').place(x=10, y=0)

   def on_search(self):
      self.search_q = self.search_bar.get()
      self.const_dict.update(search(self.search_q))
      self.results_ = [ i for i in self.const_dict.keys()] # search() returns a dictionary
      self.results_lst.set(tuple(self.results_))
      return     

   def item_selected(self, event):
      self.selected_i = self.results.curselection() # index of selection
      self.selection = self.results.get(self.selected_i)
      print(self.selection)
      
      self.link = get_link(self.selection, self.const_dict)
      self.tags = link_parser(self.link)
      self.const_dict.clear()
      populate(self.tags, self.const_dict)

      #clearing listbox
      self.results.delete(0,'end')
      return
      
   def list_refresh(self, event):
      #repopulating listbox
      self.results_ = [ i for i in self.const_dict.keys()]
      
      if 'TV' not in list(self.const_dict.keys())[0]:
         self.results_lst.set(tuple(self.results_)) # trick to show end of iteration
      return

   def mult_select(self, event):
      if 'Episode' in list(self.const_dict.keys())[0]:
         self.results.config(selectmode = MULTIPLE)
      else:
         self.results.config(selectmode = SINGLE)
      






application = Tk()
b=Home(application)
application.title("o2tvseries-bot")
application.geometry("720x650+0+0")
application.mainloop()
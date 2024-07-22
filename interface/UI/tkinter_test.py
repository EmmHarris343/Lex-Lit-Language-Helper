# interface/UI/tkinter_test.py

# This is an attempt of building a very basic UI in Tkinter that. DOES NOT Directly control Python
# The goal of this is everything will be handled through API calls. 

# THis is more so a stop gap to help build the different API calls
# So later, tkinter can be replaced with an entirely different UI (IE, Electron, Web Interface etc)

import tkinter as tk

class TK_UI:

    def __init__(self):

        self.window = tk.Tk()
        self.start_layout()
        



    
    def start_layout(self):
        window = self.window


        # Output Window/ Results
        output_label = tk.Label(window, text='Word outputs:')
        output_label.pack()

        output_msg = tk.Message(window)
        output_msg.pack()


        # Word search Types
        # Frequency
        freq_chckbx = tk.Checkbutton(window, text='Use Frequency Word Search')
        freq_chckbx.pack()

        input_label = tk.Label(window, text='Type a number 0.01 - 300, for word Frequency')
        input_label.pack()

        input_field = tk.Entry(window)
        input_field.pack()


        # Word Search / Infini Search
        radio_word_search = tk.Radiobutton(window, text='Normal word Search')
        radio_inifi_search = tk.Radiobutton(window, text='Infinitif word Search')
        
        radio_word_search.pack()
        radio_inifi_search.pack()


        # Word search input
        input_label = tk.Label(window, text='Type word for search')
        input_label.pack()

        input_field = tk.Entry(window)
        input_field.pack()

        search_label = tk.Label(window, text='When Ready - Click the search button')
        search_label.pack()

        sub_search_btn = tk.Button(window, text='Search')
        sub_search_btn.pack()


        window.mainloop()
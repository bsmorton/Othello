import tkinter

DEFAULT_FONT = ('Helvetica', 14)

###################################################
############GAME OPTIONS CLASS#####################
###################################################

class GameOptions:
    def __init__(self):
        '''
        initialises GameOptions
        '''
        self._dialog_window = tkinter.Tk()
        

        title_label = tkinter.Label(
            master = self._dialog_window, text = 'OTHELLO',
            font = DEFAULT_FONT)

        title_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.N)

        row_label = tkinter.Label(
            master = self._dialog_window, text = 'Number Of Rows:',
            font = DEFAULT_FONT)

        row_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._row_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._row_entry.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        col_label = tkinter.Label(
            master = self._dialog_window, text = 'Number Of Columns:',
            font = DEFAULT_FONT)

        col_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._col_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._col_entry.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        
        player1_label = tkinter.Label(
            master = self._dialog_window, text = 'Who Goes First?(B/W):',
            font = DEFAULT_FONT)

        player1_label.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._player1_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._player1_entry.grid(
            row = 3, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        topleft_label = tkinter.Label(
            master = self._dialog_window, text = 'Top Left Player?(B/W):',
            font = DEFAULT_FONT)

        topleft_label.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._topleft_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._topleft_entry.grid(
            row = 4, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        moreless_label = tkinter.Label(
            master = self._dialog_window, text = 'More Wins Or Less Wins?(>/<):',
            font = DEFAULT_FONT)

        moreless_label.grid(
            row = 5, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._moreless_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._moreless_entry.grid(
            row = 5, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)


        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(
            row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)

        ok_button = tkinter.Button(
            master = button_frame, text = 'OK', font = DEFAULT_FONT,
            command = self._on_ok_button)

        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._on_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self._dialog_window.rowconfigure(6, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)


        self._ok_clicked = False
        self._row = ''
        self._col = ''
        self._topleft = ''
        self._player1 = ''
        self._moreless = ''
        self.show()


###################################################
##############PUBLIC METHODS#######################
###################################################

    def show(self):
        '''
        shows the window
        '''
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def was_ok_clicked(self):
        '''
        returns true if the ok button was clicked
        '''
        return self._ok_clicked

    def get_row(self):
        '''
        returns the row that was inputed by the user
        '''
        return self._row

    def get_col(self):
        '''
        returns the collumn that was inputed by the user
        '''
        return self._col

    def get_player1(self):
        '''
        returns the starting player that was inputed by the user
        '''
        return self._player1

    def get_topleft(self):
        '''
        returns the top left player that was inputed by the user
        '''
        return self._topleft

    def get_moreless(self):
        '''
        returns the winning rule that was inputed by the user
        '''
        return self._moreless

###################################################
##############PRIVATE METHODS######################
###################################################
    def _on_ok_button(self):
        '''
        carries out action if ok button was clicked
        '''
        self._ok_clicked = True
        self._row = self._row_entry.get()
        self._col = self._col_entry.get()
        self._player1 = self._player1_entry.get()
        self._topleft = self._topleft_entry.get()
        self._moreless = self._moreless_entry.get()
        
        self._dialog_window.destroy()


    def _on_cancel_button(self):
        '''
        carries out action if cancel button was clicked
        '''
        self._dialog_window.destroy()

    




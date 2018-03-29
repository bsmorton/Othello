import tkinter
import point
import math
from collections import namedtuple
import othello_opps
import othello_prompt

cell=namedtuple('cell','x1 y1 x2 y2 row col value')
chip=namedtuple('chip','x1 y1 x2 y2 value')


DEFAULT_FONT = ('Helvetica', 14)

###################################################
##############OTHELLO GUI CLASS#####################
###################################################

class othello_gui:
    def __init__(self):
        '''
        initialization of othello_gui class
        '''
        self.r_list=[]
        self.center_list=[]
        self.chips=[]
        self.num_black=2
        self.num_white=2
        options = othello_prompt.GameOptions()
        self.ROW=int(options.get_row())
        self.COL=int(options.get_col())
        self.turn=options.get_player1()
        self.topleft=options.get_topleft()
        self.moreless=options.get_moreless()
        self.winner=''

        self.no_move_ticker=0
        self.game=othello_opps.GameState(self.turn,self.ROW,self.COL,self.topleft,self.moreless,self.no_move_ticker)
        self.game.new_game()

        if self.game.turn=='B':
            
            self.player='TURN: BLACK'
        else:
            self.player='TURN: WHITE'
        
        
        self._root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(
        master = self._root_window,
        width = 300, height = 300,
        background = 'green')

        i=0
        j=0

        for row in range(self.ROW):
            j=0
            for col in range(self.COL):
                temp_cell=cell(j,i,j+1/self.COL,i+1/self.ROW, row, col, 'empty')
                self.r_list.append(temp_cell)
                j=j+1/self.COL
            i=i+1/self.ROW

        
        self.x_dis=(self.r_list[0].x2-self.r_list[0].x1)/2
        self.y_dis=(self.r_list[0].y2-self.r_list[0].y1)/2

               
        self.title_label = tkinter.Label(
            master = self._root_window, text = 'OTHELLO (FULL)     '+'BLACK: '+str(self.num_black)+'     '+'WHITE: '+str(self.num_white),
            font = DEFAULT_FONT)

        self.title_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.N)

        self.bottom_label = tkinter.Label(
            master = self._root_window, text = self.player+self.winner,
            font = DEFAULT_FONT)

        self.bottom_label.grid(
            row = 2, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.N)

        self._canvas.grid(row = 1, column = 0, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.rowconfigure(2, weight = 0)
        self._root_window.columnconfigure(0, weight = 1)


        self._draw_board()
    


###################################################
##############PUBLIC METHODS#######################
###################################################

    def start(self):
        '''
        starts the gui
        '''
        
        self._root_window.mainloop()



###################################################
##############PRIVATE METHODS######################
###################################################



    def _play(self, click_point):
        '''
        function that carries out a turn in Othello
        '''
        self.game.valid_moves()

        x_clk,y_clk=click_point.frac()
        
        for val in range(len(self.r_list)):
            x1,y1,x2,y2=self.r_list[val].x1,self.r_list[val].y1,self.r_list[val].x2,self.r_list[val].y2
            if x_clk>x1 and x_clk<x2 and y_clk>y1 and y_clk<y2:
                self.move= self.r_list[val].row,self.r_list[val].col

        

        if not self.game.no_move_check():
                try:
                    if self.game.is_valid(self.move[0],self.move[1]):
                        self.game.clean_board()
                        self.game.player_move(self.move[0],self.move[1])
                        temp_cell=self._find_cell(self.move[0],self.move[1])
                        if self.game.turn=='B':
                            self._add_chip(temp_cell.x1,temp_cell.y1,temp_cell.x2,temp_cell.y2,'black')
                        else:
                            self._add_chip(temp_cell.x1,temp_cell.y1,temp_cell.x2,temp_cell.y2,'white')
                        self.game.next_turn()
                        self.chips=[]
                        self._draw_board()

                    self.game.valid_moves()   
                    if self.game.no_move_check():
                        if self.game.handle_no_move_ticker():
                            self.player=''
                            self._game_over_text(self.game.game_over())
                    self.game.clean_board()

                                
                except(othello_opps.InvalidRowCol):
                    self.game.clean_board()
                  
                except(othello_opps.InvalidMove):
                    self.game.clean_board()
                 
    
        self.num_black,self.num_white=self.game.count()
        self._update_text()
        self.game.clean_board()       
        self._canvas.delete(tkinter.ALL)        
        self._draw_rects()
        self._draw_chips()

    def _update_text(self):
        '''
        updates the text fields at the top and the bottom of the screen
        '''
        if self.player!='':
            if self.game.turn=='B':
                
                self.player='TURN: BLACK'
            else:
                self.player='TURN: WHITE'

        self.title_label = tkinter.Label(
            master = self._root_window, text = 'OTHELLO (FULL)     '+'BLACK: '+str(self.num_black)+'     '+'WHITE: '+str(self.num_white),
            font = DEFAULT_FONT)

        self.title_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.N)

        self.bottom_label = tkinter.Label(
            master = self._root_window,text=self.player+self.winner,
            font = DEFAULT_FONT)

        self.bottom_label.grid(
            row = 2, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.N)
    

    def _game_over_text(self, winner):
        '''
        sets the text for the winner
        '''
        if winner=='B':
            self.winner='WINNER: BLACK'
        elif winner=='W':
            self.winner='WINNER: WHITE'
        else:
            self.winner='WINNER: NONE'
        
    def _draw_board(self):
        '''
        draws the current game board
        '''
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.game.board[row][col]==self.game.WHITE:
                    temp_cell=self._find_cell(row,col)
                    self._add_chip(temp_cell.x1,temp_cell.y1,temp_cell.x2,temp_cell.y2,'white')
                elif self.game.board[row][col]==self.game.BLACK:
                    temp_cell=self._find_cell(row,col)
                    self._add_chip(temp_cell.x1,temp_cell.y1,temp_cell.x2,temp_cell.y2,'black')
                

    def _on_canvas_resized(self, event):
        '''
        resizes rectangs and chips
        '''
        self._canvas.delete(tkinter.ALL)
        self._draw_rects()
        self._draw_chips()


    def _on_canvas_clicked(self, event):
        '''
        manages click events
        '''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        click_point = point.from_pixel(
            event.x, event.y, width, height)

        self._play(click_point)

        

    
    def _draw_rects(self):
        '''
        draws all rectangles
        '''
        
        for cell in self.r_list:
            frac_x1, frac_y1, frac_x2, frac_y2=cell.x1,cell.y1,cell.x2,cell.y2
            self._draw_rect(frac_x1, frac_y1, frac_x2, frac_y2)


    def _draw_rect(self, frac_x1, frac_y1, frac_x2, frac_y2):
        '''
        draws a rectangle
        '''
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        self._canvas.create_rectangle(
            canvas_width * frac_x1, canvas_height * frac_y1,
            canvas_width * frac_x2, canvas_height * frac_y2,
            outline = 'black')

    def _add_chip(self, x1, y1, x2, y2, value):
        '''
        adds a chip to the list
        '''
        temp_chip=chip(x1+.002,y1+.002,x2-.002,y2-.002, value)
        self.chips.append(temp_chip)

    def _find_cell(self, row, col):
        '''
        takes in a row and collumn and returns a cell
        '''
        for item in self.r_list:
            if item.row == row and item.col == col:
                return item

    def _draw_chips(self):
        '''
        draws all chips on the board
        '''
        for frac_x1, frac_y1, frac_x2, frac_y2, color in self.chips:
            self._draw_chip(frac_x1, frac_y1, frac_x2, frac_y2, color)
        
    def _draw_chip(self,frac_x1, frac_y1, frac_x2,
                   frac_y2, turn):
        '''
        draws a single chip
        '''
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        
        self._canvas.create_oval(
                frac_x1*canvas_width, frac_y1*canvas_height,
                frac_x2*canvas_width, frac_y2*canvas_height,
                fill = turn)

if __name__ == '__main__':    
    app=othello_gui()
    app.start()



    


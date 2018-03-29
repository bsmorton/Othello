###################################################
##############EXCEPTION CLASSES####################
###################################################

class InvalidRowCol(Exception):
    '''
    Raised whenever an column or row choice is made
    '''
    pass

class InvalidMove(Exception):
    '''
    Raised whenever an invalid choice is made
    '''
    pass

class GameOverMove(Exception):
    '''
    Raised whenever choice is made after the game is over
    '''
    pass

###################################################
##############GAME STATE CLASS#####################
###################################################

class GameState:
    def __init__(self, turn, row, col, top_left, end_game, no_move_ticker):
        self.board=[]
        self.turn=turn
        self.ROW=row
        self.COL=col
        self.top_left=top_left
        self.NONE=0
        self.WHITE=1
        self.BLACK=2
        self.VALID=3
        self.end_game=end_game
        self.no_move_ticker=no_move_ticker
        
###################################################
##############PUBLIC METHODS#######################
###################################################
        
    def new_game(self):
        '''
        determines whether or not the top left is black or white, then returns the board accordingly
        '''
        if self.top_left=='W':
            return self._new_game_board_white()
        else:
            return self._new_game_board_black()

    def valid_moves(self):
        '''
        returns a board with the valid moves checked
        '''
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.turn=='W':
                    if self.board[row][col]==self.WHITE:
                        self.board=self._move_check_hor(row,col)
                        self.board=self._move_check_ver(row,col)
                        self.board=self._move_check_dia(row,col)
                        
                else:
                    if self.board[row][col]==self.BLACK:
                        self.board=self._move_check_hor(row,col)
                        self.board=self._move_check_dia(row,col)
                        self.board=self._move_check_ver(row,col)

        return self.board

    def clean_board(self):
        '''
        returns a board with the x's removed
        '''
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.board[row][col]==self.VALID:
                    self.board[row][col]=self.NONE
        return self.board

    def player_move(self, row, col):
        '''
        carrys out the players move. returns the updated board
        '''
        self.board=self._flip_color_hor(row,col)
        self.board=self._flip_color_ver(row,col)
        self.board=self._flip_color_dia(row,col)
        if self.turn=='W':
            self.board[row][col]=self.WHITE
        else:
            self.board[row][col]=self.BLACK
        return self.board

   

    def next_turn(self):
        '''
        change turn to next player
        '''
        if self.turn=='W':
            self.turn='B'
        else:
            self.turn='W'

    def is_valid(self,row:int,col:int):
        '''
        return true if move is valid
        '''
        try:
            if self.board[row][col]==self.VALID:
                return True
            else:
                raise InvalidMove
        except(InvalidMove):
            raise InvalidMove
        except:
            raise InvalidRowCol

    def no_move_check(self):
        '''
        return true if there are no availible moves
        '''
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.board[row][col]==self.VALID:
                    return False
        return True

    def handle_no_move_ticker(self):
        '''
        handles the ticker to determine whether or no both players cannot move
        '''
        while True:
            if self.no_move_ticker!=1:
                self.no_move_ticker+=1
                self.next_turn()
                self.clean_board()
                self.valid_moves()
                if not self.no_move_check():
                    self.no_move_ticker=0
                    self.clean_board()
                    return False
                
            else:
                return True

    def game_over(self):
        '''
        determins the winner of the game. returns a string
        '''
        black_tot, white_tot=self._end_count()
        if self.end_game=='>':
            if black_tot > white_tot:
                return 'B'
            elif black_tot < white_tot:
                return 'W'
            else:
                return 'NONE'
            
        elif self.end_game=='<':
            if black_tot > white_tot:
                return 'W'
            elif black_tot < white_tot:
                return 'B'
            else:
                return 'NONE'


    def count(self):
        '''
        counts the numbe of blacks and whites on the board
        '''
        black=0
        white=0
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.board[row][col]==self.BLACK:
                    black+=1
                elif self.board[row][col]==self.WHITE:
                    white+=1
        return black,white
                    
###################################################
##############PRIVATE METHODS######################
###################################################

    def _new_game_board_white(self):
        '''
        private function. sets up white gameboard, and returns board
        '''
        for row in range(self.ROW):
            self.board.append([])
            for col in range(self.COL):
                if row==self.ROW/2-1:
                    if col==self.COL/2-1:
                        self.board[row].append(self.WHITE)
                    elif col==self.COL/2:
                        self.board[row].append(self.BLACK)
                    else:
                        self.board[row].append(self.NONE)
                elif row==self.ROW/2:
                    if col==self.COL/2-1:
                        self.board[row].append(self.BLACK)
                    elif col==self.COL/2:
                        self.board[row].append(self.WHITE)
                    else:
                        self.board[row].append(self.NONE)
                else:
                    self.board[row].append(self.NONE)

        return self.board

    def _new_game_board_black(self):
        '''
        private function. sets up black gameboard, and returns board
        '''
        for row in range(self.ROW):
            self.board.append([])
            for col in range(self.COL):
                if row==self.ROW/2-1:
                    if col==self.COL/2-1:
                        self.board[row].append(self.BLACK)
                    elif col==self.COL/2:
                        self.board[row].append(self.WHITE)
                    else:
                        self.board[row].append(self.NONE)
                elif row==self.ROW/2:
                    if col==self.COL/2-1:
                        self.board[row].append(self.WHITE)
                    elif col==self.COL/2:
                        self.board[row].append(self.BLACK)
                    else:
                        self.board[row].append(self.NONE)
                else:
                    self.board[row].append(self.NONE)

        return self.board


    def _move_check_ver(self, row, col):
        '''
        private function. Checks moves vertically, and marks valid moves with an x. returns board
        '''
        run=False
        break_chk=False
        for row_temp in range(row+1,self.ROW):
            self.board,run,break_chk=self._mark_valid(row_temp ,col, run, break_chk)
            if break_chk==True:
                break

        run=False
        break_chk=False
        for row_temp in range(1,row+1):
            self.board,run,break_chk=self._mark_valid(row-row_temp ,col, run, break_chk)
            if break_chk==True:
                break

        
        return self.board

    def _move_check_hor(self, row, col):
        '''
        private function. Checks moves horizontally, and marks valid moves with an x. returns board
        '''
        run=False
        break_chk=False
        for col_temp in range(col+1,self.COL):
            self.board,run,break_chk=self._mark_valid(row ,col_temp, run, break_chk)
            if break_chk==True:
                break
            
        run=False
        break_chk=False
        for col_temp in range(1,col+1):
            self.board,run,break_chk=self._mark_valid(row ,col-col_temp, run, break_chk)
            if break_chk==True:
                break
            
        return self.board 


    
    def _move_check_dia(self, row: int, col: int):
        '''
        private function. Checks moves diagonally. returns board
        '''
        run=False
        break_chk=False
        for col_temp in range(1,self.COL):
            if row+col_temp<self.ROW and col+col_temp<self.COL:

                self.board,run,break_chk=self._mark_valid(row+col_temp ,col+col_temp, run, break_chk)
                if break_chk==True:
                    break
                
        run=False
        break_chk=False
        for col_temp in range(1,self.COL):
            if row-col_temp>=0 and col-col_temp>=0:

                self.board,run,break_chk=self._mark_valid(row-col_temp ,col-col_temp, run, break_chk)
                if break_chk==True:
                    break
                

        run=False
        break_chk=False
        for col_temp in range(1,self.COL):
            if row-col_temp>=0 and col+col_temp<self.COL:
                
                self.board,run,break_chk=self._mark_valid(row-col_temp ,col+col_temp, run, break_chk)
                if break_chk==True:
                    break
                
                
        run=False
        break_chk=False
        for col_temp in range(1,self.COL):
            if row+col_temp<self.ROW and col-col_temp>=0:

                self.board,run,break_chk=self._mark_valid(row+col_temp ,col-col_temp, run, break_chk)
                if break_chk==True:
                    break
                

                
        return self.board   

    

    def _mark_valid(self, row ,col, run, break_chk):
        '''
        private function. marks valid moves with an x, returns a tuple
        '''
        if self.board[row][col]==self.NONE:
            if run==True:
                    
                    self.board[row][col]=self.VALID
                    break_chk=True
            else:
                    break_chk=True
                    
        elif self.board[row][col]==self.VALID:
            break_chk=True

        elif self.turn=='W':
            if self.board[row][col]==self.WHITE: 
                break_chk=True
            elif self.board[row][col]==self.BLACK:
                run=True

        elif self.turn=='B':
            if self.board[row][col]==self.BLACK: 
                break_chk=True
            elif self.board[row][col]==self.WHITE:
                run=True
        
        return self.board,run,break_chk

    def _flip_color_ver(self, row, col):
        '''
        private method. fips the colors vertically, returns board
        '''
        run=False
        break_chk=False
        temp_flip=[]
        for row_temp in range(row+1,self.ROW):
            GS,run,break_chk,temp_flip=self._flip_color(row_temp ,col, run, break_chk,temp_flip)
            if break_chk==True:
                break

        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK

        run=False
        break_chk=False
        temp_flip=[]
        for row_temp in range(1,row+1):
            GS,run,break_chk,temp_flip=self._flip_color(row-row_temp ,col, run, break_chk,temp_flip)
            if break_chk==True:
                break

        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK

            
        return self.board   


    def _flip_color_hor(self, row, col):
        '''
        private method. fips the colors horizontally, returns board
        '''
        run=False
        break_chk=False
        temp_flip=[]
        for col_temp in range(col+1,self.COL):
            self.board,run,break_chk,temp_flip=self._flip_color(row ,col_temp, run, break_chk,temp_flip)
            if break_chk==True:
                break

        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK

            
        run=False
        break_chk=False
        temp_flip=[]
        for col_temp in range(1,col+1):
            self.board,run,break_chk,temp_flip=self._flip_color(row ,col-col_temp, run, break_chk,temp_flip)
            if break_chk==True:
                break

        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK

            
        return self.board


    def _flip_color_dia(self, row, col):
        '''
        private method. fips the colors diagonally, returns board
        '''
        run=False
        break_chk=False
        temp_flip=[]
        for col_temp in range(1,self.COL):
            if row+col_temp<self.ROW and col+col_temp<self.COL:

                self.board,run,break_chk,temp_flip=self._flip_color(row+col_temp ,col+col_temp, run, break_chk,temp_flip)
                if break_chk==True:
                    break
        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK
                
        run=False
        break_chk=False
        temp_flip=[]
        for col_temp in range(1,self.COL):
            if row-col_temp>=0 and col-col_temp>=0:

                self.board,run,break_chk,temp_flip=self._flip_color(row-col_temp ,col-col_temp, run, break_chk,temp_flip)
                if break_chk==True:
                    break

        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK
                
        run=False
        break_chk=False
        temp_flip=[]
        for col_temp in range(1,self.COL):
            if row-col_temp>=0 and col+col_temp<self.COL:
                
                self.board,run,break_chk,temp_flip=self._flip_color(row-col_temp ,col+col_temp, run, break_chk,temp_flip)
                if break_chk==True:
                    break
                
        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK       
        run=False
        break_chk=False
        temp_flip=[]
        for col_temp in range(1,self.COL):
            if row+col_temp<self.ROW and col-col_temp>=0:

                self.board,run,break_chk,temp_flip=self._flip_color(row+col_temp ,col-col_temp, run, break_chk, temp_flip)
                if break_chk==True:
                    break
                
        if run==False:
            for item in temp_flip:
                if self.turn=='W':
                    self.board[item[0]][item[1]]=self.WHITE
                else:
                    self.board[item[0]][item[1]]=self.BLACK
        return self.board

    
    def _flip_color(self, row ,col, run, break_chk, temp_flip=list):
        '''
        private method. fips the color, returns tuple
        '''
        if self.board[row][col]==self.NONE:
                temp_flip=[]
                break_chk=True
        elif self.turn=='W':
            if self.board[row][col]==self.WHITE:
                break_chk=True
                run=False
            else:
                temp_flip.append((row,col))
                run=True
        elif self.turn=='B':
            if self.board[row][col]==self.BLACK:
                break_chk=True
                run=False
            else:
                temp_flip.append((row,col))
                run=True
        
        return self.board,run,break_chk,temp_flip


    def _end_count(self):
        '''
        returns final count
        '''
        black_tot=0
        white_tot=0
        for row in range(self.ROW):
            for col in range(self.COL):
                if self.board[row][col]==self.BLACK:
                    black_tot+=1
                elif self.board[row][col]==self.WHITE:
                    white_tot+=1
        return black_tot, white_tot

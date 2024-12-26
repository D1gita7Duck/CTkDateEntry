import customtkinter as ctk
from tkinter import END, NORMAL, Event

def _is_leap(year):
    """Returns 1 if year is leap year, else 0"""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

class DateTextEntry(ctk.CTkEntry):
    
    def __init__(self, 
                 master,
                 width = 140,
                 height = 40,
                 corner_radius = None,
                 border_width = None,
                 bg_color = "transparent", 
                 fg_color = None, 
                 border_color = None, 
                 text_color = None, 
                 placeholder_text_color = None, 
                 textvariable = None, 
                 placeholder_text : str = None,
                 date_format : int = 0,
                 delimiter : str = "/",
                 font = None, 
                 state = NORMAL, 
                 invalid_date_cmd = None, **kwargs):
        """
        Spawns a CtkEntry to take date string.\n
        date_format takes 0, 1, 2, 3, 4
        corresponding to DD/MM/YY, DD/MM/YYYY, MM/DD/YY, MM/DD/YYYY, YYYY/MM/DD\n
        custom delimiter can be given using delimiter = <?>. Placeholder text is automatically altered on passing delimiter.\n
        ValueError is raised on giving invalid date. Error can be caught by passing suitable function to invalid_date_cmd.\n
        String Values are passed to invalid_date_cmd in the format "Error {int} -> ..." with int corresponding to
        Incomplete date = -1, Bad date input = 1, Bad month input = 2, Bad February Date = 3
        """
        if (date_format not in range(0, 5)):
            raise ValueError(f'Format : {self._placeholder_text} ' + "Bad input for date_format. Must be one of the integers 0, 1, 2, 3, 4")
        if (placeholder_text is None):
            if (date_format == 0):
                placeholder_text = "DD/MM/YY".replace('/', delimiter)
            elif (date_format == 1):
                placeholder_text = "DD/MM/YYYY".replace('/', delimiter)
            elif (date_format == 2):
                placeholder_text = "MM/DD/YY".replace('/', delimiter)
            elif (date_format == 3):
                placeholder_text = "MM/DD/YYYY".replace('/', delimiter)
            elif (date_format == 4):
                placeholder_text = "YYYY/MM/DD".replace('/', delimiter)

        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, text_color, placeholder_text_color, textvariable, placeholder_text, font, state, **kwargs)
        self._placeholder_text = placeholder_text
        self._date_format = date_format
        self._delimiter = delimiter
        self._invalid_date_cmd = invalid_date_cmd
        self._digit_count = 0
        self.date_str = ""
        self.input_str = ""
        self.full = False
        self._30_days = (4, 6, 9, 11)
        self._31_days = (1, 3, 5, 7, 8, 10, 12)

        if (date_format == 0 or date_format == 2):
            self.bind("<KeyRelease>", self.control_entry02)
        elif (date_format == 1 or date_format == 3):
            self.bind("<KeyRelease>", self.control_entry13)
        else:
            self.bind("<KeyRelease>", self.control_entry4)
    

    def control_entry02(self, event : Event):
        """
        Date format is DD/MM/YY or MM/DD/YY
        """
        print(event, event.char, self.full)
        
        if (event.keysym == "BackSpace"):
            if (self.date_str != "" and self.date_str[-1].isdigit()):
                self.date_str = self.date_str[0:-1]
                self.input_str = self.input_str[0:-1]
            elif (self.date_str != "" and self.date_str[-1] == self._delimiter):
                self.date_str = self.date_str[0:-2]
                self.input_str = self.input_str[0:-2]
                self.delete(0, END)
                self.insert(0, self.date_str)
            self._digit_count -= 1
            self.full = False
            return

        if (self._digit_count == 6):
            self.full = True
            self.delete(0, END)
            self.insert(0, self.date_str)
            return
        elif (event.char.isdigit()):
            self._digit_count += 1
            self.date_str += event.char
            self.input_str += event.char
            if (self._digit_count == 6):
                self.full = True
                self.validate_entry()
        else:
            self.delete(0, END)
            self.insert(0, self.input_str)
            return
        
        if (self._digit_count == 2 or self._digit_count == 4):
            self.date_str += self._delimiter
            self.input_str += self._delimiter
            self.insert(END, self._delimiter)
        
    def control_entry13(self, event : Event):
        """
        Date Format is DD/MM/YYYY or MM/DD/YYYY
        """
        print(event, event.char, self.full)
        
        if (event.keysym == "BackSpace"):
            if (self.date_str != "" and self.date_str[-1].isdigit()):
                self.date_str = self.date_str[0:-1]
                self.input_str = self.input_str[0:-1]
            elif (self.date_str != "" and self.date_str[-1] == self._delimiter):
                self.date_str = self.date_str[0:-2]
                self.input_str = self.input_str[0:-2]
                self.delete(0, END)
                self.insert(0, self.date_str)
            self._digit_count -= 1
            self.full = False
            return

        if (self._digit_count == 8):
            self.full = True
            self.delete(0, END)
            self.insert(0, self.date_str)
            return
        elif (event.char.isdigit()):
            self._digit_count += 1
            self.date_str += event.char
            self.input_str += event.char
            if (self._digit_count == 8):
                self.full = True
                self.validate_entry()
        else:
            self.delete(0, END)
            self.insert(0, self.input_str)
            return
        
        if (self._digit_count == 2 or self._digit_count == 4):
            self.date_str += self._delimiter
            self.input_str += self._delimiter
            self.insert(END, self._delimiter)
    
    def control_entry4(self, event : Event):
        """
        Date Format is YYYY/MM/DD
        """
        print(event, event.char, self.full)
        
        if (event.keysym == "BackSpace"):
            if (self.date_str != "" and self.date_str[-1].isdigit()):
                self.date_str = self.date_str[0:-1]
                self.input_str = self.input_str[0:-1]
            elif (self.date_str != "" and self.date_str[-1] == self._delimiter):
                self.date_str = self.date_str[0:-2]
                self.input_str = self.input_str[0:-2]
                self.delete(0, END)
                self.insert(0, self.date_str)
            self._digit_count -= 1
            self.full = False
            return

        if (self._digit_count == 8):
            self.full = True
            self.delete(0, END)
            self.insert(0, self.date_str)
            return
        elif (event.char.isdigit()):
            self._digit_count += 1
            self.date_str += event.char
            self.input_str += event.char
            if (self._digit_count == 8):
                self.full = True
                self.validate_entry()
        else:
            self.delete(0, END)
            self.insert(0, self.input_str)
            return
        
        if (self._digit_count == 4 or self._digit_count == 6):
            self.date_str += self._delimiter
            self.input_str += self._delimiter
            self.insert(END, self._delimiter)

    def validate_entry(self):
        """
        Checks if given input is valid for a given date format.\n
        If it is invalid, ValueError is raised with appropriate message.
        """
        try:
            if (self.full == False):
                raise ValueError(f'Error -1 -> Format : {self._placeholder_text} ' + "Given Date is incomplete")
            date = self.get_int()
            if (self._date_format == 0 or self._date_format == 1):
                # check month
                if (date[1] > 12 or date[1] < 1):
                    raise ValueError(f'Error 2 -> Format : {self._placeholder_text} ' + "Bad input for month")
                # check date for corresponding month
                if (date[1] in self._30_days):
                    if (date[0] > 30 or date[0] < 1):
                        raise ValueError(f'Error 2 -> Format : {self._placeholder_text} ' + "Bad input for date")
                elif (date[1] in self._31_days):
                    if (date[0] > 31 or date[0] < 1):
                        raise ValueError(f'Error 1 -> Format : {self._placeholder_text} ' + "Bad input for date")
                elif (_is_leap(date[2]) and date[1] == 2):
                    if (date[0] > 29 or date[0] < 1):
                        raise ValueError(f'Error 3 -> Format : {self._placeholder_text} ' + "Bad input for February date")
                elif (date[1] == 2):
                    if (date[0] > 28 or date[0] < 1):
                        raise ValueError(f'Error 3 -> Format : {self._placeholder_text} ' + "Bad input for February date")
            
            elif (self._date_format == 2 or self._date_format == 3):
                # check month
                if (date[0] > 12 or date[0] < 1):
                    raise ValueError(f'Error 2 -> Format : {self._placeholder_text} ' + "Bad input for month")
                # check date for corresponding month
                if (date[0] in self._30_days):
                    if (date[1] > 30 or date[1] < 1):
                        raise ValueError(f'Error 1 -> Format : {self._placeholder_text} ' + "Bad input for date")
                elif (date[0] in self._31_days):
                    if (date[1] > 31 or date[1] < 1):
                        raise ValueError(f'Error 1 -> Format : {self._placeholder_text} ' + "Bad input for date")
                elif (_is_leap(date[2]) and date[0] == 2):
                    if (date[1] > 29 or date[1] < 1):
                        raise ValueError(f'Error 3 -> Format : {self._placeholder_text} ' + "Bad input for February date")
                elif (date[0] == 2):
                    if (date[1] > 28 or date[1] < 1):
                        raise ValueError(f'Error 3 -> Format : {self._placeholder_text} ' + "Bad input for February date")
            else:
                print(date, date[0]%4, date[0]%400, date[0]%100, date[1] == 2)
                # check month
                if (date[1] > 12 or date[1] < 1):
                    raise ValueError(f'Error 2 -> Format : {self._placeholder_text} ' + "Bad input for month")
                # check date for corresponding month
                if (date[1] in self._30_days):
                    if (date[2] > 30 or date[2] < 1):
                        raise ValueError(f'Error 1 -> Format : {self._placeholder_text} ' + "Bad input for date")
                elif (date[1] in self._31_days):
                    if (date[2] > 31 or date[2] < 1):
                        raise ValueError(f'Error 1 -> Format : {self._placeholder_text} ' + "Bad input for date")
                elif (_is_leap(date[0]) and date[1] == 2):
                    if (date[2] > 29 or date[2] < 1):
                        raise ValueError(f'Error 3 -> Format : {self._placeholder_text} ' + "Bad input for February date")
                elif (date[1] == 2):
                    if (date[2] > 28 or date[2] < 1):
                        raise ValueError(f'Error 3 -> Format : {self._placeholder_text} ' + "Bad input for February date")
        except ValueError as msg:
            if self._invalid_date_cmd is not None:
                self._invalid_date_cmd(msg)
            else:
                raise ValueError(msg)

    def get_int(self) -> tuple[int, int, int]:
        """
        Returns tuple of three integers in given date format
        """
        if (self.full == False):
            raise ValueError(f'Format : {self._placeholder_text} ' + "Given Date is incomplete")
        date = self.date_str.split(self._delimiter)
        date = tuple(int(x) for x in date)
        return date
    
    def get_str(self) -> str:
        if (self.full == False):
            raise ValueError(f'Format : {self._placeholder_text} ' + "Given Date is incomplete")
        return self.date_str

    def reset(self):
        """
        Clears the Entry. Resets date_str to ""
        """
        self.delete(0, END)
        self.date_str = ""
        self.input_str = ""
        self.full = False
        self._digit_count = 0
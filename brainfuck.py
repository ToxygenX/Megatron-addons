# Made by : @Hackintush || github.com/ToxygenX
# Made For : https://github.com/TeamUltroid/UltroidAddons

"""
✘ Commands Available

• `{i}bf`
    Text to Brainfuck String Generator with text or reply.

• `{i}rbf`
    Brainfuck Interpreter with string or reply.

• `{i}morse`
    Morse code Generator and Interpretor
"""

from bidict import bidict 

from . import *

def evaluate(commands):
    interpreter = BrainfuckInterpreter(commands)
    while interpreter.available():
        interpreter.step()

    return interpreter.output.read()

__all__ = (
    'BrainfuckInterpreter'
)

class IOStream:
    def __init__(self, data=None):
        self._buffer = data or ''

    def __len__(self):
        return len(self._buffer)

    def read(self, length=None):
        if not length:
            data = self._buffer
            self._buffer = ''
        else:
            data = self._buffer[:length]
            self._buffer = self._buffer[length:]

        return data

    def write(self, data):
        self._buffer += data


class IncrementalByteCellArray:
    def __init__(self):
        self.byte_cells = [0]
        self.data_pointer = 0

    def __getitem__(self, item):
        cell_amount = len(self.byte_cells)
        if item > cell_amount - 1:
            self.extend(item - cell_amount + 1)

        return self.byte_cells[item]

    def __setitem__(self, key: int, value: int):
        cell_amount = len(self.byte_cells)
        if key > cell_amount - 1:
            self.extend(key - cell_amount + 1)

        self.byte_cells[key] = value

    def __len__(self):
        return len(self.byte_cells)

    def __repr__(self):
        return self.byte_cells.__repr__()

    def extend(self, size: int):
        self.byte_cells += [0] * size

    def increment(self):
        new_val = (self.get() + 1) % 256
        self.set(new_val)

    def decrement(self):
        new_val = self.get() - 1
        if new_val < 0:
            new_val = 255

        self.set(new_val)

    def set(self, value: int):
        self.__setitem__(self.data_pointer, value)

    def get(self):
        return self.__getitem__(self.data_pointer)


class BrainfuckInterpreter:
    def __init__(self, commands: str):
        self._commands = commands

        self.input = IOStream()
        self.output = IOStream()

        self.instruction_pointer = 0
        self.cells = IncrementalByteCellArray()

        self._opening_bracket_indexes = []

    def _look_forward(self):
        remaining_commands = self._commands[self.instruction_pointer:]
        loop_counter = 0
        index = self.instruction_pointer

        for command in remaining_commands:
            if command == '[':
                loop_counter += 1
            elif command == ']':
                loop_counter -= 1

            if loop_counter == 0:
                return index

            index += 1

    def _interpret(self):
        instruction = self._commands[self.instruction_pointer]

        if instruction == '>':
            self.cells.data_pointer += 1
        elif instruction == '<':
            self.cells.data_pointer -= 1
        elif instruction == '+':
            self.cells.increment()
        elif instruction == '-':
            self.cells.decrement()
        elif instruction == '.':
            self.output.write(chr(self.cells.get()))
        elif instruction == ',':
            self.cells.set(self.input.read(1))
        elif instruction == '[':
            if self.cells.get() == 0:
                loop_end = self._look_forward()
                self.instruction_pointer = loop_end
            else:
                self._opening_bracket_indexes.append(self.instruction_pointer)
        elif instruction == ']':
            if self.cells.get() != 0:
                opening_bracket_index = self._opening_bracket_indexes.pop(-1)

                self.instruction_pointer = opening_bracket_index - 1
            else:
                self._opening_bracket_indexes.pop(-1)

    def step(self) -> None:
        self._interpret()
        self.instruction_pointer += 1

    def available(self) -> bool:
        return not self.instruction_pointer >= len(self._commands)

    def command(self):
        return self._commands[self.instruction_pointer]


def bf(text):
  items = []
  for c in text:
     items.append('[-]>[-]<' + ('+' * (ord(c) // 10)) + '[>++++++++++<-]>' + ('+' * (ord(c) % 10)) + '.<')
  return ''.join(items)


@ultroid_cmd(
    pattern="bf",
)
async def _(event):        
    input_ = event.text[4:]
    if not input_:
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            input_ = previous_message.message
        else:
            return await eod(event, "Give me some text lol", time=5)
    await eor(event, f"{bf(input_)}")
    

@ultroid_cmd(
    pattern="rbf",
)
async def _(event):
    input_ = event.text[5:]
    if not input_:
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            input_ = previous_message.message
        else:
            return await eod(event, "Give me some text lol", time=5)
    await eor(event, f"{evaluate(input_)}")


morse_dict = bidict({'A' : '.-',
                     'B' : '-...',
                     'C' : '-.-.',
                     'D' : '-..',
                     'E' : '.',
                     'F' : '..-.',
                     'G' : '--.',
                     'H' : '....',
                     'I' : '..',
                     'J' : '.---',
                     'K' : '-.-',
                     'L' : '.-..',
                     'M' : '--',
                     'N' : '-.',
                     'O' : '---',
                     'P' : '.--.',
                     'Q' : '--.-',
                     'R' : '.-.',
                     'S' : '...',
                     'T' : '-',
                     'U' : '..-',
                     'V' : '...-',
                     'W' : '.--',
                     'X' : '-..-',
                     'Y' : '-.--',
                     'Z' : '--..',
                     'Ö' : '---.',
                     'ß' : '...--..',
                     'Ü' : '..--',
                     'Ä' : '.-.-',
                     'CH': '----',
                     '.' : '.-.-.-',
                     ':' : '---...',
                     ',' : '--..--',
                     ';' : '-.-.-.',
                     '?' : '..--..',
                     '!' : '-.-.--',
                     '-' : '-....-',
                     '_' : '..--.-',
                     '(' : '-.--.',
                     ')' : '-.--.-',
                     '=' : '-...-',
                     '+' : '.-.-.',
                     '/' : '-..-.',
                     '@' : '.--.-.',
                     ' ' : ' /',
                     '1' : '.----',
                     '2' : '..---',
                     '3' : '...--',
                     '4' : '....-',
                     '5' : '.....',
                     '6' : '-....',
                     '7' : '--...',
                     '8' : '---..',
                     '9' : '----.',
                     '0' : '-----',
                     'SOS' : '...---...',
                     })


def toMorse(text):
    for x in text:
        if(x != '-' and x != '.' and x != ' ' and x != '/'):
            return True 
    return False 


def decrypt(text):
    text = text.split()
    tilak = ""
    for x in text:
        if(x == '/'):
            tilak += ' '
        elif(x in morse_dict.inverse):
            tilak += morse_dict.inverse[x]
        else:
            tilak += 'UNKOWN' + '0'
    return tilak


def encrypt(text):
    tilak = ""
    for x in text:
        if(x in morse_dict):
            tilak += morse_dict[x] + ' '
        else:
            tilak += 'UNKNOWN' + ' '
    return tilak


@ultroid_cmd(
    pattern=".morse", 
)
async def morsey(event):
    input_ = event.text[4:]
    if not input_:
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            input_ = previous_message.message
        else:
            return await eod(event, "Give me some text lol", time=5)
    tilak = ""
    if(toMorse(input_.upper())):
        tilak =  encrypt(input_.upper())
    else:
        tilak = decrypt(input_.upper())
    await eor(event, tilak)
  

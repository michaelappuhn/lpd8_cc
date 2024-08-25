import mido

def main():
    controller = LPD8Controller()

class LPD8Controller():
    is_connected = False

    def __init__(self):
        # Connect to the port or message failure
        self.port = self.connect()

        if (self.port != False):
            self.is_connected = True
            self.give_instructions()
            self.get_pad_press()
        else:
            self.message_connection_failure()


    def give_instructions(self):
        print("Twist a knob or hit a pad on the LPD8.")

    def connect(self):
        ins = mido.get_input_names()
        if ('LPD8' in ins):
            print("LPD8 connected")
            port = mido.open_input('LPD8')
            return port
        else:
            return False

    def message_failure(self):
        print("LPD8 port not connected.") 
        print("Using keyboard instead of external controller.") 

    def check_is_connected(self):
        if (self.is_connected != False):
            return True
        else: return False

    def get_pad_press(self):
        for msg in self.port:
            mp = MessageProcessor(msg)
            #mp.print_response()

    def process_note(self):
        pass

    def process_cc(self):
        pass

class MessageProcessor():
    msg_type = False

    def __init__(self, msg):
        self.process_message(msg)
        self.print_response()

    def process_message(self, msg):
        self.__select_type(msg)

    def __select_type(self, msg):
        if msg.type == 'note_on':
            self.message = NoteMessage(msg)
            self.msg_type = 'note'
        elif msg.type == 'control_change':
            self.message = CCMessage(msg)
            self.msg_type = 'cc'
        elif msg.type == 'program_change':
            self.message = ProgramChangeMessage(msg)
            self.msg_type = 'program'

    def print_response(self):
        if (self.msg_type != False):
            self.message.print_output()

class Message():
    def __init__(self, msg):
        self.msg = msg
        self.channel = msg.channel
        
    def print_output(self):
        pass

    def __debug_output(self):
        print(self.msg)


class CCMessage(Message):
    def __init__(self, msg):
        super().__init__(msg)

    def print_output(self):
        self.__debug_output()

    def __debug_output(self):
        print("CC", ": ", "cc#:", self.msg.control, "value:", self.msg.value, "channel", self.channel)
 
class NoteMessage(Message):
    def __init__(self, msg):
        super().__init__(msg)
        self.note = self.msg.note
        self.map_note()

    def print_output(self):
        self.__debug_output()
        
    def __debug_output(self):
        print("channel:", self.channel, "pad:", self.pad)
        #print(self.msg)
        #print(self.msg.dict())

    def map_note(self):

        note_map = { 
            0: {
                36: 1,
                37: 2,
                38: 3,
                39: 4,
                40: 5,
                41: 6,
                42: 7,
                43: 8
            },
            1: {
                35: 1,
                36: 2,
                42: 3,
                39: 4,
                37: 5,
                38: 6,
                46: 7,
                44: 8
            },
            2: {
                60: 1,
                62: 2,
                64: 3,
                65: 4,
                67: 5,
                69: 6,
                71: 7,
                72: 8
            },
            3: {
                36: 1,
                38: 2,
                40: 3,
                41: 4,
                43: 5,
                45: 6,
                47: 7,
                48: 8
            }
        }

        try: 
            self.pad = note_map[self.channel][self.note]
        except:
            print("some kind of pad error")
            self.__debug_output()


class ProgramChangeMessage(Message):
    def print_output(self):
        self.__debug_output()
        
    def __debug_output(self):
        print(self.msg)


main() 

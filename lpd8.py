import mido

def main():
    x = LPD8Controller()

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
        print("Instructions go here")

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
            mp.print_response()
            #print(msg)
            #print("channel", msg.channel)

            # Turning the LPD8 into a voting system?
            if (msg.type == 'note_on'):
                #print("note:", msg.note)
                if msg.note == 36:
                    pad=1
                if msg.note == 37:
                    pad=2
                if msg.note == 38:
                    pad=3
                if msg.note == 39:
                    pad=4
                if msg.note == 40:
                    pad=5
                if msg.note == 41:
                    pad=6
                if msg.note == 42:
                    pad=7
                if msg.note == 43:
                    pad=8
                elif (msg.note < 36 or msg.note > 43):
                    print("Your LPD8 should be on Prog1!")
                    pad = False
                return(pad)

    def process_note(self):
        pass

    def process_cc(self):
        pass

class MessageProcessor():
    msg_type = False

    def __init__(self, msg):
        self.choose_type(msg)
        self.print_response()

    def choose_type(self, msg):
        if msg.type == 'note_on':
            self.message = NoteMessage(msg)
            self.msg_type = 'note'
        elif msg.is_cc:
            self.message = CCMessage(msg)
            self.msg_type = 'cc'

    def print_response(self):
        if (self.msg_type != False):
            self.message.print_output()

class Message():
    def __init__(self, msg):
        self.msg = msg
        
    def print_output(self):
        pass

    def __debug_output(self):
        print(self.msg)


class CCMessage(Message):
    def print_output(self):
        self.__debug_output()

    def __debug_output(self):
        print(self.msg)
        print(self.msg.type, ": ", self.msg.control, self.msg.value, self.msg.time)
 
class NoteMessage(Message):
    def print_output(self):
        self.__debug_output()
        
    def __debug_output(self):
        print(self.msg)

main() 

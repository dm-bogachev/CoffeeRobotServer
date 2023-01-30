from datetime import datetime

def push(msg=''):
        msg_ = ''
        if type(msg) == type([]):
            msg_ = [str(datetime.now()), ': '] + msg
        if type(msg) == type(''):
            msg_ = [str(datetime.now()), ': ']
            msg_.append(msg)
        print(''.join(msg_))
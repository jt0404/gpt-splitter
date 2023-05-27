# This tool can help ChatGPT read big texts
# by splitting them into chunks of certain size. 
# For example GPT3.5 can read around 4000 characters in a single message. 


import sys
import pyperclip
import argparse


def parse_flags():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--save', 
                        help='save all the messages to <path/filename_chunked.txt>', 
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        type=bool)
    parser.add_argument('--display', 
                        help='display messages while iterating through them', 
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        type=bool)
    parser.add_argument('--path', 
                        help='path to the file', 
                        default='',
                        type=str)
    parser.add_argument('--action', 
                        help='action for ChatGPT to perform after sending all messages', 
                        default='summarize all text',
                        type=str)
    parser.add_argument('--size', 
                        help='size of a single message', 
                        default=4000,
                        type=int)

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def open_file(path):
    f = None
    try:
        f = open(flags.path, 'r')
    except Exception as e:
        print(e)
        sys.exit(2)
    return f


def msg_prefix(last_msg, msg_idx):
    if last_msg:
        return f'==================== MESSAGE {msg_idx} -> LAST ====================\n'
    return f'==================== MESSAGE {msg_idx} ====================\n'


def write_file(path, content):
    with open(path, 'a') as f:
        f.write(content)


if __name__ == '__main__':
    flags = parse_flags()
    path = flags.path
    action = flags.action
    msg_size = flags.size
    display = flags.display 
    save = flags.save
    save_path = path.split('.')[0] + '_chunked.txt'
    f = open_file(path)
    msg_idx = 0
    msg_iter = iter(lambda: f.read(msg_size) , '')
    msg = (
        '==================== MESSAGE 0 ====================\n'
        + 'Hi I will give you a text to read splitted into multiple messages in the form of\n'
        + '==================== MESSAGE n ====================\n'
        + '\'message\'\n'
        + '\nDONT RESPOND TO THIS MESSAGE YET\n'
        + 'last message is going to have a form of\n'
        + '==================== MESSAGE n -> LAST ====================\n'
        + '\'message\'\n'
        + '\nRESPOND TO THIS MESSAGE NOW\n'
        + 'which will tell you what to do, are you ready?\n'
    )
    last_msg = False
         
    while True:
        if display:
            print(msg)
            print()

        print(f'Press \'c\' to copy MESSAGE {msg_idx} to clipboard and go to the next message')
        print('Press \'q\' to exit')

        key = input()

        if key == 'c':
            pyperclip.copy(msg)
            print(f'\nMessage {msg_idx} copied to clipboard')

            if save:
                print(f'Message {msg_idx} appended to a file: {save_path}')

                if msg_idx == 1:
                    msg = '\n' + msg
                elif msg_idx > 1:
                    msg = '\n\n' + msg

                write_file(save_path, msg)

            if last_msg:
                break

            msg_idx += 1

            try:
                msg = (
                        msg_prefix(last_msg, msg_idx)
                        + '...' 
                        +  next(msg_iter) 
                        + '...'
                        + '\n\nDONT RESPOND TO THIS MESSAGE YET'
                      )
            except:
                last_msg = True
                msg = (
                        msg_prefix(last_msg, msg_idx)
                        + f'Ok that was the last message, now can you {action}?'
                        + '\n\nRESPOND TO THIS MESSAGE NOW'
                      )
        elif key == 'q':
            print('\nExiting')
            break
        else:
            print('\nUnrecognized key')

        print()

    f.close()



import sys
import pyperclip
import argparse
import os


def prepare_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input',
                        help='decide where to take input from',
                        choices=['stdin', 'file'],
                        default='stdin',
                        type=str)
    parser.add_argument('--save_path',
                        help='if specified saves all messages to a given path',
                        default='',
                        type=str)
    parser.add_argument('--input_path', 
                        help='path to the file, required if --input=file or --chunked', 
                        default='',
                        type=str)
    parser.add_argument('--display', 
                        help='display messages while iterating through them', 
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        type=bool)
    parser.add_argument('--action', 
                        help='action for ChatGPT to perform after sending all messages', 
                        default='summarize all text',
                        type=str)
    parser.add_argument('--size', 
                        help='size of a single message', 
                        default=4000,
                        type=int)
    parser.add_argument('--chunked',
                        help='if specified copies all messages prepared by this program from --input_path',
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        type=bool)

    return parser


def read_input_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(e)
        sys.exit(4)


def open_output_file(save, save_path):
    if save:
        return open(save_path, 'a')
    return None


def msg_prefix(last_msg, msg_idx):
    if last_msg:
        return f'==================== MESSAGE {msg_idx} -> LAST ====================\n'
    return f'==================== MESSAGE {msg_idx} ====================\n'


def write_file(f, msg, msg_idx, save, save_path):
    if not save:
        return

    if msg_idx > 0:
        msg = '\n' + msg

    f.write(msg)    
    print(f'Message {msg_idx} appended to a file: {save_path}\n')


def first_message():
    return (
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


def format_msg(msg, msg_idx, action, last_msg):
    if last_msg:
        return (
            f'==================== MESSAGE {msg_idx} -> LAST ====================\n'
            + f'Okay that was the last message, now can you {action}?\n'
            + 'RESPOND TO THIS MESSAGE NOW\n'
        )
    return (
        f'==================== MESSAGE {msg_idx} ====================\n' 
        + f'...{msg}...\n'
        + 'DONT RESPOND TO THIS MESSAGE YET\n'
    )


def copy_to_clipboard(msg, msg_idx):
    pyperclip.copy(msg)
    print(f'\nMessage {msg_idx} copied to clipboard')


def wait_for_key(msg_idx):
    print(f'Press \'c\' to copy MESSAGE {msg_idx} to clipboard and go to the next message')
    print('Press \'n\' go to the next message')
    print('Press \'q\' to exit')
    return input('Your key: ')


def display_msg(display, msg):
    if display:
        print(msg)
        print()


def process_text(text, action, size, display, save_path):
    save = save_path != ''
    f = open_output_file(save, save_path)
    msg_idx = 0
    msg = first_message()
    last_msg = False
         
    print('\n\n')

    while True:
        display_msg(display, msg)

        key = wait_for_key(msg_idx)

        if key in ['c', 'n']:
            if key == 'c':
                copy_to_clipboard(msg, msg_idx)

            write_file(f, msg, msg_idx, save, save_path)

            if last_msg:
                break

            if len(text) == 0:
                last_msg = True 

            msg_idx += 1
            msg = format_msg(text[:size], msg_idx, action, last_msg)
            text = text[size:]
        elif key == 'q':
            print('\nExiting')
            break
        else:
            print('\nUnrecognized key')

        print()

    if save:
        f.close()


def chunked_search(text, i, j, msg_idx):
    s = text.find(f'==================== MESSAGE {msg_idx} ====================\n', i, j)
    e = text.find(f'==================== MESSAGE {msg_idx + 1} ====================\n', i, j)

    if s == -1:
        s = text.find(f'==================== MESSAGE {msg_idx} -> LAST ====================\n', i, j)
        e = len(text) 
    elif e == -1:
        e = text.find(f'==================== MESSAGE {msg_idx + 1} -> LAST ====================\n', i, j)

    return s, e


def chunked(text, display):
    msg_idx = 0
    s, e = chunked_search(text, 0, len(text), 0)
    msg = text[s:e]

    while True:
        display_msg(display, msg)

        key = wait_for_key(msg_idx)

        if key in ['c', 'n']:
            if key == 'c':
                copy_to_clipboard(msg, msg_idx)

            if e == len(text):
                break

            msg_idx += 1
            s, e = chunked_search(text, e, len(text), msg_idx)
            msg = text[s:e]
        elif key == 'q':
            print('\nExiting')
            break
        else:
            print('\nUnrecognized key')


if __name__ == '__main__':
    parser = prepare_parser()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    if args.input == 'stdin':
        print('Please enter your input followed by Ctrl+Z or Ctrl+D:\n')
        process_text(sys.stdin.read(), args.action, args.size, args.display, args.save_path)
    elif args.input == 'file':
        if args.input_path == '':
            print('ERROR: Input path not provided\n')
            parser.print_help()
            sys.exit(2)
        if args.chunked:
            chunked(read_input_file(args.input_path), args.display)
        else:
            process_text(read_input_file(args.input_path), args.action, args.size, args.display, args.save_path)
    else:
        print('ERROR: Unrecognized argument\n')
        parser.print_help()
        sys.exit(3)



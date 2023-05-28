# gpt-reader

This tool can help ChatGPT read big texts
by splitting them into chunks of certain size. 
For example GPT3.5 can read around 4000 characters in a single message. 

## Example

![Alt text](example.gif)

## Usage

```console
$ pip install -r requirements.txt
```

```console
$ python gpt_reader.py 

usage: gpt_reader.py [-h] [--save | --no-save] [--display | --no-display] [--path PATH] [--action ACTION] [--size SIZE]

options:
  -h, --help            show this help message and exit
  --save, --no-save     save all the messages to <filename.gptr> (default: False)
  --display, --no-display
                        display messages while iterating through them (default: False)
  --path PATH           path to the file (default: )
  --action ACTION       action for ChatGPT to perform after sending all messages (default: summarize all text)
  --size SIZE           size of a single message (default: 4000)
```


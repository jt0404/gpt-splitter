# gpt-reader

This tool can help ChatGPT read big texts
by splitting them into chunks of certain size. 
For example GPT3.5 can read around 4000 characters in a single message. 

## Usage

```console
$ pip install -r requirements.txt
```

```console
$ python main.py --help

usage: main.py [-h] [--display | --no-display] [--path PATH] [--action ACTION] [--size SIZE]

options:
  -h, --help            show this help message and exit
  --display, --no-display
                        display messages while iterating through them (default: False)
  --path PATH           path to the file (default: )
  --action ACTION       action for ChatGPT to perform after sending all messages (default: summarize all text)
  --size SIZE           size of a single message (default: 4000)
```

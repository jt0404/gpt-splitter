# gpt-splitter

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
$ python gpt_splitter.py 

usage: gpt_splitter.py [-h] [--input {stdin,file}] [--save_path SAVE_PATH] [--input_path INPUT_PATH] [--display | --no-display]
                       [--action ACTION] [--size SIZE] [--splitted | --no-splitted]

options:
  -h, --help            show this help message and exit
  --input {stdin,file}  decide where to take input from (default: stdin)
  --save_path SAVE_PATH
                        if specified saves all messages to a given path (default: )
  --input_path INPUT_PATH
                        path to the file, required if --input=file or --splitted (default: )
  --display, --no-display
                        display messages while iterating through them (default: False)
  --action ACTION       action for ChatGPT to perform after sending all messages (default: summarize all text)
  --size SIZE           size of a single message (default: 4000)
  --splitted, --no-splitted
                        if specified copies all messages prepared by this program from --input_path (default: False)
```


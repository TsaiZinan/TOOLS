# TOOLS
Some tools

## ConvertMarkdownImageLinks2imgur
### Convert every image link in your Markdown file to Imgur links.

1. Fill your Imgur API client_id and client_secret in code below.
```
client_id = 'Your Client ID'
client_secret = 'Your Client Secret'
```
2. Rename your Markdown file to new_markdown_file.md
3. Install imgurpython
```
pip install imgurpython
```
4. Run the program
```
python MarkdownImageLinkConvert2imgur.py
```

Due to the speed limit of Imgur, only 50 uploads per IP per hour. You need to change your IP when you see the warning message.

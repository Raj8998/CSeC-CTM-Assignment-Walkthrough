> Raj Pastagiya | 06/05/2023

## Solution-1
#### Step-1
- After loading and running the image, the first thing I did was to inspect the image and running container using
```bash
docker inspect [image-name | container-name]
```
- It didn't give anything unusual, so next step is to start searching within the running container.

#### Step-2
- Start a shell prompt inside container with privileged permissions using:
```bash
docker exec -it --privileged conatiner-name bash
```
- Now the first thing I looked is if there exists any users in the container, so I looked into **/etc/passwd** file where I found my first flag...
```FLAG
/etc/passwd: CSeC{4nd_n0w_y0u_d0n7}
```

#### Step-3
- We now know the format of the flag, so we can search for other flags using grep command like below:
```bash
grep -ie "CSeC.*" -R <folder>
```
- Here the folder I used were /home, /var, /root.. and in /root folder I found other two flags:
```FLAG
/root/.bashrc:export CTM="CSeC{n0w_y0u_s33_m3}"
/root/.bash_history:echo CSeC{qu1t3_4n_3y3_y0u_g07_7h3r3}
```

# OR
## Solution-2
- Below commands should give all necessary flags:
```bash
# flag 1
env

# flag 2
cat /etc/passwd

# flag 3
history
```


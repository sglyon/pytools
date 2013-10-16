# Setting up a public notebook server

Much of the material here is adapted from the [Running a notebook server](http://ipython.org/ipython-doc/dev/interactive/public_server.html) page of the ipython documentation.

Steps:

1. Inside IPython, run the following (obviously replacing the string `ENTERpasswordHERE`)

```python
from IPython.lib import passwd
print(passwd('ENTERpasswordHERE'))
```
2. Copy the text printed out, you will use it later.
3. Create a new ipython profile. I wanted to name the profile nbssl and I used the command `ipython profile create nbssl`.
4. Within the new profile directory, edit the file `ipython_notebook_config.py`. For me this file was in `~/.ipython/profile_nbssl/ipython_notebook_config.py`. Search for and update/un-comment the following line (keep the file open, as we will be changing more of it as we go):

```python
c.NotebookApp.password = u'LONGhashFROMstep2'
```
5. Create a self-signed ssl certificate (this will produce a warning, but getting an officially signed one is a non-trivial endeavor). To do this `cd` to the ipython profile directory from above and run the following

```sh
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.crt
```
6. Update the `ipython_notebook_config.py` file again to specify the location of the certification and the key file. For me this meant updating the following lines to look like this:

```python
# The full path to an SSL/TLS certificate file.
c.NotebookApp.certfile = u'/Users/sglyon/.ipython/profile_nbssl/mycert.crt'

# The full path to a private key file for usage with SSL/TLS.
c.NotebookApp.keyfile = u'/Users/sglyon/.ipython/profile_nbssl/mycert.key'
```
7. Make the notebook public by telling the server to listen on all ip addresses by editing the following line in the `ipython_notebook_config.py` file:

```python
c.NotebookApp.ip = '*'
```
8. (OPTIONAL) Give the notebook a static, specified port to run on. I changed the following line in the `ipython_notebook_config.py` file:

```python
c.NotebookApp.port = 9999
```
9. (OPTIONAL) Have the notebook server start without pulling up the browser by changing the following line:

```python
c.NotebookApp.open_browser = False
```

10. (OPTIONAL) If you would like to access this notebook server from outside your local network you need to do the following two steps. Configure your computer's internal network settings so it has a static local IP address. I chose `10.0.1.222` for my server.
11. (OPTIONAL) Configure your router to forward the port from step 8 (mine was `9999`) to the static IP from step 10 (mine was `10.0.1.222`). This will ensure that you can access the server remotely, from behind the router.
12. (OPTIONAL) Specify a custom directory for the server notebooks to be stored by editing the following line of `ipython_notebook_config.py` (note that I have included the example directory I chose: `/Users/sglyon/serverNotebooks`):

```python
# The directory to use for notebooks.
c.NotebookManager.notebook_dir = u'/Users/sglyon/serverNotebooks'
```

After all that setup, you simply need to run the following to start the server:

```sh
ipython notebook --profile=nbssl
```


## Accessing from a remote computer

If you would like to access from a remote computer (one not on your same wifi network or the equivalent), you need to have opened up the ports in steps 8 and 11 *and* you need to know the public IP address for your network (this is different from the local IP address assigned to your computer in step 10). You can do this using a website like [whatsmyip.org](http://www.whatsmyip.org/), or using the following python script.

```python
import urllib
import re


def fetch_ext_ip():
    "Fetches and returns external IP address"
    request = urllib.urlopen("http://checkip.dyndns.org").read()

    return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)[0]

print("your IP Address is: %s" %  fetch_ext_ip())
```

Once you know your external IP address and the port number for the server, you can access it remotely by making an https request. For example, if my remote IP address was `1.1.1.1` and I was specified port `2222` in step 8, I would access this server from any computer using the url `https://1.1.1.1:2222`. This would direct me to the ipython notebook login screen where I would enter the password from step 1 and be up and running inside the ipython notebook.

## Automatic external IP updates

```python
import smtplib
import os
from net_utils import fetch_ext_ip  # function from previous snippet


def send_email(msg, to, username, password, provider='gmail'):
    """
    Send an email

    Parameters
    ==========
    msg : str
        The actual message you would like to send

    to : str
        The recipient's email address as a string

    username : str
        The username for the sender as a string

    password : str
        The password for the sender's email account

    provider : str
        The email provider to be used. Right now this function only works for
        gmail, but could be easily extended for other email providers. (I only
        use gmail so I didn't feel like looking up other providers info)

    Returns
    =======
    None, just sends an email
    """
    if provider == 'gmail':
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(username, password)
    smtpserver.sendmail(username, to, msg)
    smtpserver.close()

home = os.path.expanduser("~")
ip_fn = home + os.path.sep + ".ext_ip.txt"  # file name where ip is stored

if os.path.exists(ip_fn):
    former_ip = open(ip_fn, 'r').read().strip()

    new_ip = fetch_ext_ip().strip()
    if former_ip != new_ip:
        changed = True
        with open(ip_fn, 'w') as f:
            f.write(new_ip)
    else:
        changed = False
else:
    changed = True
    new_ip = fetch_ext_ip()
    with open(ip_fn, 'w') as f:
        f.write(new_ip)

if changed is True:  # only send email if there is a change
    info = open(home + os.path.sep + '.email_settings').readlines()
    parsed = map(lambda x: x.split()[1].strip(), info)
    msg = "To:{to}\nFrom:{sender}\nSubject: IPynb External IP changed\n\n"
    msg += "The new IP address is {ip}"
    send_email(msg.format(to=parsed[0], sender=parsed[1], ip=new_ip), *parsed)

```

The above creates a file in your home directory named `.ext_ip.txt`. It is simply a text file containing the external IP address of the network where this file was last executed. It also assumes that there is a file at `~/.email_settings` that has 4 lines in the following structure:

```
to: YOURemailHERE
from: YOURemailHERE
password: emailPASSWORDhere
provider: EMAILproviderHERE
```

It would then be up to you to use a service like `cron` to run this file on a schedule from the computer hosting the notebook server.

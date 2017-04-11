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

    
        

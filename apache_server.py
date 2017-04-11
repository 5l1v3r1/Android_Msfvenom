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
            






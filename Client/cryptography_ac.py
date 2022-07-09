import Cryptodome
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from cryptography.fernet import Fernet
from ffd import Dirs_and_files, Delet_files 
import base64
import hashlib
import shutil
import os
import sys
import subprocess
from getpass import getpass
import colorama
from colorama import Fore
import time


class Crypt_ac(object):
    
    
    class Asymmetric_encryption(object):
            
        def generet_rsa_keys(self,bytes_length):
            key=RSA.generate(bytes_length)
            public=key.public_key()
            return [key.export_key('PEM'),public.export_key('PEM')]

        def import_rsa_private_key(self,private_pem):
            return RSA.import_key(private_pem)

        def import_rsa_public_key(self,public_pem):
            return RSA.import_key(public_pem).public_key()

        def rsa_encryt(self,public,data):
            if type(public)!=Cryptodome.PublicKey.RSA.RsaKey:
                public=self.import_rsa_private_key(public)
            cipher=PKCS1_OAEP.new(public)
            return base64.b64encode(cipher.encrypt(data))

        def rsa_decrypt(self,private,data):
            if type(private)!=Cryptodome.PublicKey.RSA.RsaKey:
                private=self.import_rsa_private_key(private)
            cipher=PKCS1_OAEP.new(private)
            return cipher.decrypt(base64.b64decode(data))


    
    
    class Symmetric_encryption(object):

        def __init__(self,key,iv=b'0'*16):
            if type(key)!=bytes:
                key=key.encode()
            if type(iv)!=bytes:
                iv=iv.encode()
            self.key=key
            try:
                self.cipher=AES.new(key, AES.MODE_CBC, iv)
            except:
                pass
            try:
                self.cipher2=AES.new(key, AES.MODE_GCM, iv)
            except Exception as e:
                #print(e)
                pass

        def pad_data(self,data):
            if len(data)%16!= 0:
                while len(data)%16!= 0:
                    data+=b' '
                return data

        def encrypt_data_aes(self,data):
            data=self.pad_data(data)
            return base64.b64encode(self.cipher.encrypt(data))

        def decrypt_data_aes(self,data):
            data=base64.b64decode(data)
            return self.cipher.decrypt(data[AES.block_size:])

        def encrypt_aes_gcm(self,data):
            return self.cipher2.encrypt(data)

        def decrypt_aes_gcm(self,data):
            return self.cipher2.decrypt(data)


        def fer_encrypt(self,data):
            if type(data)!= bytes:
                data=data.encode()
            key=base64.b64encode(hashlib.sha256(self.key).digest())
            fer=Fernet(key)
            return fer.encrypt(data)

        def fer_decrypt(self,data):
            if type (data)!= bytes:
                data=data.encode()
            key=base64.b64encode(hashlib.sha256(self.key).digest())
            fer=Fernet(key)
            return fer.decrypt(data)


        def _cp_file(self,path,name_cp):
            srs=(path)
            if name_cp=='backup':
                dest=os.environ['AppData']+os.sep+'Cryptography'+os.sep+name_cp+os.path.splitext(path)[1]
            else: 
                dest=os.environ['AppData']+os.sep+'Cryptography'+os.sep+'Cipher'+os.sep+name_cp+os.path.splitext(path)[1]
            try:
                shutil.copyfile(srs,dest)
            except Exception as e:
                 if os.system('copy '+srs+' '+dest)!=0:
                    raise Exception (str(e))
            return[srs,dest]


        def encrypt_file(self,path):
            pathSize=int(os.path.getsize(path))
            if pathSize>=1073741824:
                pathes=self._cp_file(path,'encp')
                cp_file=pathes[-1]
                with open(cp_file,'rb') as srs:
                    with open(pathes[0],'wb') as dest:
                        try:
                            dest.write(self.cipher.encrypt(pad(srs.read(),AES.block_size)))
                            dest.close()
                            srs.close()
                            Delet_files().delet_one_file(cp_file)
                            return 'Successfully encrypted!'
                        except Exception as e:
                            self._restore_data(cp_file,pathes[0])
                            raise Exception (str(e))
            elif pathSize>20971520:
                with open(path,'rb') as file:
                    data=file.read()
                with open(path,'wb')as file:
                    try:
                        file.write(self.cipher.encrypt(pad(data,AES.block_size)))
                        data=''
                        return 'Successfully encrypted'
                    except Exception as e:
                        file.write(data)
                        data=''
                        raise Exception (str(e))
            else:
                with open(path,'rb') as file:
                    data=file.read()
                with open(path,'wb')as file:
                    try:
                        file.write(self.fer_encrypt(data))
                        data=''
                        return 'Successfully encrypted'
                    except Exception as e:
                        file.write(data)
                        raise Exception (str(e))



        def decrypt_file(self,path):
            pathSize=int(os.path.getsize(path))
            if pathSize>=1073741824:
                pathes=self._cp_file(path,'decp')
                cp_file=pathes[-1]
                with open(cp_file,'rb') as srs:
                    with open(pathes[0],'wb') as dest:
                        try:
                            dest.write(unpad(self.cipher.decrypt(srs.read()),AES.block_size))
                            dest.close()
                            srs.close()
                            Delet_files().delet_one_file(cp_file)
                            return 'Successfully decrypted'
                        except  Exception as e:
                            self._restore_data(cp_file,pathes[0])
                            raise Exception (str(e))
            elif pathSize>27962124:
                with open(path,'rb')as file:
                    data=file.read()
                with open(path,'wb')as file:
                    try:
                        file.write(unpad(self.cipher.decrypt(data),AES.block_size))
                        data=''
                        return 'Successfully decrypted'
                    except Exception as e:
                        file.write(data)
                        data=''
                        raise Exception (str(e))
            else:
                with open(path,'rb')as file:
                    data=file.read()
                with open(path,'wb')as file:
                    try:
                        file.write(self.fer_decrypt(data))
                        return 'Successfully decrypted'
                    except Exception as e:
                        file.write(data)
                        data=''
                        raise Exception (str(e))




        def recursive_encrypt_files(self,path):
            paths_dir=Dirs_and_files(path).get_all_files()
            print('Processing...') 
            for i in paths_dir:
                try:
                    self.encrypt_file(i)
                except:
                    pass
            print('end.')


        def sync_recursive_encrypt_files(self,path):
            sec=''
            faild=''
            print('Processing...')
            paths_dir=Dirs_and_files(path).get_all_files()
            for i in paths_dir:
                try:
                    self.encrypt_file(i)
                    sec+=f"{i.strip():<70}{' sec':>10}"+'\n'
                except:
                    faild+=f"{i.strip():<70}{' failde':>10}"+'\n'
                    pass
            print('end.')
            return sec+faild

        def recursive_decrypt_files(self,path):
            paths_dir=Dirs_and_files(path).get_all_files()
            print('Processing...') 
            for i in paths_dir:
                try:
                    self.decrypt_file(i)
                except Exception as e:
                    print(e)
            print('end.')

        def _restore_data(self,srs,dest):
            try:
                with open(srs,'rb') as s:
                    with open(dest,'wb')as d:
                        d.write(s.read)
                    d.close()
                    s.close()
            except:
                p=subprocess.Popen('copy "'+srs+'" "'+dest+'" /y', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        
def get_hash_key_and_iv(passwd):
    key=hashlib.md5(passwd.encode()).digest()
    iv=hashlib.md5(key[::2]).digest()
    return [key,iv]
    
    
        
def compar_passwd(path,passwd):
    if type(passwd)!=bytes:
        passwd=passwd.encode()
    with open(path,'rb') as file:
        key_compar=file.read()
        file.close()
    if passwd==key_compar:
        return True
    return False

    
def main():
    try:
        os.mkdir(os.environ['AppData']+os.sep+'Cryptography')
        os.mkdir(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'Cipher')
        print("First Setup...")
        time.sleep(0.5)
        password=getpass('please choose password to encrypt and decrypt using this program: ')
        key=hashlib.md5(password.encode()).hexdigest()
        with open(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'key.key','wb') as file:
            file.write(key.encode())
    except Exception as e:
        #print(e)
        key=getpass('please enter your password: ')
        key=hashlib.md5(key.encode()).hexdigest()
        print('Processing...')
        time.sleep(1)
        if compar_passwd(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'key.key',key):
            print('Correct password!')
        else:
            count=1
            for i in range(1,7):
                key=getpass("Incorrect password Please try again ("+str(count)+' - 6)')
                key=hashlib.md5(key.encode()).hexdigest()
                print('Processing...')
                time.sleep(1)
                if compar_passwd(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'key.key',key):
                    print('Correct password!')
                    break
                if i == 5:
                    print('\nLast try!', end='. ')
                    time.sleep(2)
                elif i == 6:
                    sys.exit(-1)
                count+=1
    key=bytes.fromhex(key)
    iv=hashlib.md5(key[::2]).digest()
    cr=Crypt_ac().Symmetric_encryption(key,iv)
    cr._cp_file(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'key.key','backup')
    time.sleep(1)
    help_='\n'
    help_+=('======= Encrypt & Decrypt ========')+'\n'
    help_+=(f"|{'  To change password.     (1)':<32}|")+'\n'
    help_+=(f"|{'  To backup the password. (2)':<32}|")+'\n'
    help_+=(f"|{'  To encrypt text.        (3)':<32}|")+'\n'
    help_+=(f"|{'  To decrypt text.        (4)':<32}|")+'\n'
    help_+=(f"|{'  To encrypt file.        (5)':<32}|")+'\n'
    help_+=(f"|{'  To decrypt file.        (6)':<32}|")+'\n'
    help_+=(f"|{'  To encrypt directory.   (7)':<32}|")+'\n'
    help_+=(f"|{'  To decrypt directory.   (8)':<32}|")+'\n'
    help_+=('-'*34)+'\n'
    
    print(help_)
    while True:
        cr=Crypt_ac().Symmetric_encryption(key,iv)
        time.sleep(0.5)
        t=input('Select one option: ')
        
        if t=='help':
            print(help_)

        elif t=='1':
            real_password=getpass('please enter your current password: ')
            real_password=hashlib.md5(real_password.encode()).hexdigest()
            print('Processing...')
            time.sleep(1)
            if compar_passwd(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'key.key',real_password):
                new_pass=getpass('Please enter new password: ')
                pass_comp=getpass('Please confirm your password: ')
                if new_pass==pass_comp:
                    with open(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'key.key','wb') as file:
                        file.write(hashlib.md5(new_pass.encode()).hexdigest().encode())
                        file.close()
                    key=hashlib.md5(new_pass.encode()).digest()
                    iv=hashlib.md5(new_pass[::2].encode()).digest()
                    print('This password will be the permanent key to encrypt and decrypt using this program.')
                else:
                    print('Worng password.')
            else:
                print('Worng password')
            
            
            
        elif t=='2':
            cr._cp_file(os.environ['AppData']+os.sep+'Cryptography'+os.sep+'key.key','backup.key')
            print('The password was successfully retrieved!')
            
            
        elif t=='3':
            text = input('Please enter text to encrypt: ').encode()
            if len(text)<400:
                print('encrypt data = '+str(cr.fer_encrypt(text).decode()))
            elif len(text)<=16381:
                with open('Encrypt Text.txt','wb')as file:
                    file.write(cr.fer_encrypt(text))
                    file.close()
                time.sleep(1)
                os.startfile('Encrypt Text.txt')
                print('resault file was open! 🢃')
            else:
                print('The length of the string is too long,\nplease enter the string in a text file and \nselect the option 5 to encrypt a file.')
            text=''
                
                
        elif t=='4':
            psw = input('To decrypt with same password enter 1\nto decrypt with other password enter 2\n> ')
            if psw =='1':
                text=input('Please enter encypt text to decrypt: ').encode()
                dec_text=b''
                try:
                    dec_text=cr.fer_decrypt(text)
                except:
                    print('\n\nThis cipher could not be decrypted with your key',end='')
                if len(dec_text)<=450 and len(dec_text)>0:
                    print('Decrypt text = '+str(dec_text.decode()))
                elif len(dec_text)>0:
                    with open('Decrypt Text.txt','wb') as file:
                        file.write(cr.fer_encrypt(text))
                        file.close()
                    time.sleep(1)
                    os.startfile('Decrypt Text.txt')
                    print('resault file was open! 🢃')
                dec_text=b''
            elif psw =='2':
                dec_text=b''
                psw=getpass('Please enter password: ')
                text=input('Please enter encypt text to decrypt: ')
                psw=hashlib.md5(psw.encode()).digest()
                iv2=hashlib.md5(psw[::2]).digest()
                try:
                    dec_text=Crypt_ac().Symmetric_encryption(psw,iv2).fer_decrypt(text)
                except:
                    print('Worng password.',end='')
                if len(dec_text)<=450 and len(dec_text)>0:
                    print('Decrypt text = '+dec_text.decode())
                elif len(dec_text)>0:
                    file=open('Decrypt Text.txt','wb')
                    file.write(cr.fer_decrypt(text))
                    os.startfile('Decrypt Text.txt')
                    print('resault file was open! 🢃')
                dec_text=b''
                

                
        elif t=='5':
            path=input('Please enter path: ')
            print(cr.encrypt_file(path))
                
        elif t=='6':
            psw = input('To decrypt with same password enter 1\nto decrypt with other password enter 2\n> ')
            if psw =='1':
                path=input('Please enter path: ')
                print(cr.decrypt_file(path))
            elif psw == '2':
                psw=getpass('Please enter password\n> ').encode()
                path=input('Please enter path: ')
                print(Crypt_ac().Symmetric_encryption(get_hash_key_and_iv(psw)[0],get_hash_key_and_iv(psw)[-1]).decrypt_file(path))
            
        elif t=='7':
            print(Fore.LIGHTRED_EX)
            print("="*61)
            print(f"| {'WARNING!':^51}{'|':>8}\n|",end='')
            print(f"{'|':>60}")
            print(f"|{'  the path encryption is done recursively,':<59}|\n|{'  for each file and folder in the selected path!':<59}|")
            print(f"|{'  do not to encrypt sensitive files such as system':<59}|\n|{'  essential files, an entire drive(!C:) or users':<59}|")
            print(f"|{'  directory!':<59}|")
            print('-'*61)
            print(Fore.RESET,end='')
            w=input('continue (y/n): ')
            if w=='y':
                path=input('to encrypt folder please enter full path (ex: C:\\Users\\foder): ')
                with open("Encrypt Folder.txt",'wb')as file:
                    file.write(cr.sync_recursive_encrypt_files(path).encode('utf8',errors="replace"))
                os.startfile("Encrypt Folder.txt")
                print('resault file was open! 🢃')
                
                
        elif t=='8':
            psw = input('To decrypt with same password enter 1\nto decrypt with other password enter 2\n> ')
            if psw =='1':
                path=input('Please enter path: ')
                cr.recursive_decrypt_files(path)
            elif psw == '2':
                psw=getpass('Please enter password\n> ')
                path=input('Please enter path: ')
                Crypt_ac().Symmetric_encryption(get_hash_key_and_iv(psw)[0],get_hash_key_and_iv(psw)[-1]).recursive_decrypt_files(path)
                
                

                
if __name__=='__main__':                     
    main()  
    
   
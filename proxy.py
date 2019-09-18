import requests
import time
import os
import shutil

# =============================================================================
# with open("newproxy.txt",'r') as p:
#     proxiess = p.read().split()
# 
# =============================================================================
def random_proxy(): 
    r = requests.get("http://34.213.20.241/?Key=PROFEZA").text.split('\\')[1][1:]  #newline
    proxy = {'https':'https://' + r }      #random.choice(proxiess)}
    return proxy

def get_url(url, retries=3, steam = False):
    if retries>0:
        try:
            return requests.get(url,proxies=random_proxy(), stream=steam) #proxies=random_proxy(),
        except Exception as e:
            print(e)
            print("Retrying remain %s" %(retries))
            retries -= 1
            time.sleep(1)
            return get_url(url, retries)
    else:
        print("not found")
        
def download_pdf(link,j):
    directory = "pyf"+str(j)
    os.mkdir(directory)
    #folder_name = Directory.make_directory(j)
    flag = 0
    try:
        l = get_url(url=link, retries=4, steam=True)
        with open(directory+'/pyf'+str(j)+'.pdf','wb') as pdf:
            for chunk in l.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
                print("downloading")
            print("downloaded")
            flag = 1
            return flag
    except Exception as e:
        print(e)
        print("download failed, so deleting the directory")
        shutil.rmtree(directory)
        #Directory.remove_directory(j)
        print("deleted")
        return flag
    

    
            

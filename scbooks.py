from bs4 import BeautifulSoup
from proxy import get_url
from proxy import download_pdf





def libgen(doi,j):
    flag=0
    url = "http://booksdescr.org/scimag/ads.php?doi="+doi
    try:
        r=get_url(url)
        soup = BeautifulSoup(r.content, 'lxml')
        link=soup.find("tr").a['href']
        if link:
            flag = download_pdf(link)
            return flag
    except: 
        return sc_books(doi,j)
    

def api_unpaywall(doi,j):
    flag = 0
    url="http://api.unpaywall.org/v2/"+doi+"?email=chaturvedivanchhit@gmail.com"
    try:
        response = get_url(url)
        data = response.json()
        try:
            link = data['best_oa_location']['url_for_pdf']
            #doi = data['doi']
            if link == None:
                print("link is None")
                return libgen(doi,j)
            else:
                flag = download_pdf(link,j)
                return flag
        except:
            print("not found")
            return libgen(doi,j)
    except:
        return libgen(doi,j)
    


def sc_books(doi,j):
    flag = 0
    return flag 
# =============================================================================
# 
#     url='http://booksc.org/s/?q=' + doi + '&t=0'
#     try:
#         req =get_url(url)
#         if req:
#             manual_response = re.findall("On your request nothing has been found",req.text)
#             if not manual_response:
#                 first_link = re.findall('["]\/book\/.+\/.+["]\s',req.text)[0].replace('"','')
#                 first_link = "https://booksc.xyz"+first_link
#                 
#                 ##request on new link
#                 req1 = get_url(first_link)
#                 soup =BeautifulSoup(req1.text,'lxml')
#                 download_link = soup.find('a',{'class':'btn btn-primary dlButton'})
#                 link = "https://booksc.xyz/" + download_link['href']
#                 flag = download_pdf(link)
#                 return flag
#         else: 
#             return flag
#     except:
#         return flag        
#     
# =============================================================================
# =============================================================================
# soup = bs(req.text,'lxml')   
# url = soup.find('div',{'id':'searchResultBox'}).find('div',{'class':'resItemBox resItemBoxArticles resItemFuzzyMatch'}).div
#     link = re.findall('["]\/book\/.+\/.+["]\s',str(url))
# =============================================================================
    
   
#a material section cleaner script                      
import spacy 
# Load English tokenizer, tagger,  
# parser, NER and word vectors 
nlp = spacy.load("en_core_web_sm")
import re
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from string import punctuation
ps = PorterStemmer()

f=open('stemmeshfinal.txt','r',encoding='utf8')
contents = f.read().lower()
f.close()
contents = contents.split()    
stop_words = stopwords.words('english') + list(punctuation) + list(contents) + ['','C','','’','•','¢','F.','T.','root','stem','®','™','Dancers','Infusion','Sporulation','B.','Greenland','Centrifuge','Resuspend','procured','.A','P.','/m','Gujarat','Co.','E.','St.','Dr.','Ltd.','Inc','U.S.A.','','°C','S.','M.','Prof.','-20°C','C.','U.S.A','·','-3','±','L.','A.','‘','-2','N-','J.','K.','Co.Usa','Diagnostics','Sequencing','Sterilized','Signaling','','~g/ml','O.D','D.','J.l','O.lM','Staining','Upstate','B.']
remwords=['','»','’','O.lM','/mg','â€Ÿs','•','/mg-','/ml','-up','Concentrated','dilution','conjugate','lmmunoresearch','assays','\'7gre','\'la.ter','-70°C','¢','F.','T.','','root',':250','°/o','stem','®','™','-1','lmM','i.e','U.K','electrodes','electrode','digestion','ice-cold','lOOml','we~e','centrifugation','dye','ng/ml','g/L','slants','routinely','w.r.t','stimulation','commercially','promoter','digestion','labeling','amplification','transfection','kindly','freshly','doses','absorbance','freshly','Prof','quantitation','in-house','Dancers','Infusion','Sporulation','B.','Greenland','Centrifuge','Resuspend','.A','P.','/m','Gujarat','Co.','Corp.','E.','St.','Dr.','Ltd.','Inc','U.S.A.','','°C','S.','M.','Prof.','-20°C','C.','U.S.A','·','-3','±','L.','A.','‘','-2','N-','J.','K.','Co.Usa','Diagnostics','Sequencing','Sterilized','Signaling','','~g/ml','O.D','D.','J.l','O.lM','Staining','Upstate','B.']    
                      
#a material section string is given
def tokenise(material):
    wospl = material.split('. ')
    wojoi = ','.join(wospl)
    wospl = wojoi.split(',')
    wojoi=' '.join(wospl)
    token = nltk.word_tokenize(wojoi)
    return token

def regsub_clean(lisli):
    li=[]
    for word in lisli:
        word=re.sub('^[¢»®™•°/’!"#$%&\€Ÿ\'()*+,-./:;<=>?@[\]^_`{|}~\“\”]+','',word)
        word=re.sub('[¢»®™•°/’!"#$%&\€Ÿ\'()*+,-./:;<=>?@[\]^_`{|}~\“\”]+$','',word)
        #word=re.sub('^[¢»®™•°/’!"#$%&\\'()*+,-./:;<=>?@[\]^_`{|}~\“\”]{1,6}[0-9]+$','',word)
        word=re.sub('^[¢»®™•°/’!"#$%&\\'()*+,-./:;<=>?@[\]^_`{|}~\“\”0-9]+$','',word)
        word=re.sub('^[0-9]{4,8}?.+','',word) 
        if re.search('^[0-9]+$',word):
            continue 
        elif word == '':
        	continue
        elif re.search('m[mlin]{0,3}/[cmlin]+',word):
            continue
        elif re.search('^[μ]',word):
            continue              
        elif (len(word)<=2):
            continue
        elif (len(word)>45):
            continue
        li.append(word)        
    lis = [ word for word in li if not word in remwords]
    return lis



def lemm(lisli):
    words = [word for word in lisli if not ps.stem(word.lower()) in stop_words]
    return words

#removes word with the help of spacy library and gives final result
def spac(listli): 
    if listli is None:
        return listli
    new=[]
    for item in listli:
        doc = nlp(item)
        tok = [token.text for token in doc if not token.pos_ == "VERB"]
        tok = ''.join(tok)
        new.append(tok)
    return new
    

def rem_af_spac(lisli): #lemm function is present in 
    li=[]
    for word in lisli:
        word=re.sub('^[¢»®™•°/’!"#$%&\€Ÿ\'()*+,-./:;<=>?@[\]^_`{|}~\“\”]+','',word)
        word=re.sub('[¢»®™•°/’!"#$%&\€Ÿ\'()*+,-./:;<=>?@[\]^_`{|}~\“\”]+$','',word)
        word=re.sub('^[¢»®™•°/’!"#$%&\\'()*+,-./:;<=>?@[\]^_`{|}~\“\”0-9]+$','',word)
        word=re.sub('^[0-9]{4,8}?.+','',word) 
        if re.search('^[0-9]+$',word):
            continue 
        elif word == '':
        	continue
        elif re.search('m[mlin]{0,3}/[cmlin]+',word):
            continue
        elif re.search('^[μ]',word):
            continue              
        elif (len(word)<=2):
            continue
        elif (len(word)>45):
            continue
        li.append(word) 
    words = lemm(li)
    wojoi = ' '.join(words)
    return wojoi
                      

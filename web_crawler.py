#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#theme 
get_ipython().system('pip install jupyterthemes')
get_ipython().system('pip install --upgrade jupyterthemes')
get_ipython().system('jt -t grade3')
get_ipython().system('jt -t grade3 -T')
#https://towardsdatascience.com/customize-your-jupyter-notebook-theme-in-2-lines-of-code-fc726cea1513


# In[29]:


get_ipython().system('pip install requests')
get_ipython().system('pip install beautifulsoup4 ')
get_ipython().getoutput('pip install nltk')
get_ipython().system('pip install pandas ')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[147]:


import re
import requests
import urllib.request
from bs4 import BeautifulSoup, Comment
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
#import matplotlib.pyplot as plt
from operator import itemgetter
#import string
import collections
import operator 
import pandas as pd
# We used also other basic libraries like pandas to show the data in nice forms, re for matching 
#a spesific set of strings, 
#, collection and string.
class Web_Crawler():
    def __init__(self, url , depth, re_specialD):
        self.url=url #website address
        self.depth=depth
        self.re_specialD=re_specialD
        self.source_code= self.read_htmlFile(url)
        self.lemmas_with_freq={}
        
    def read_htmlFile(self, url): 
        req=requests.get(url) #make a http-request for a given url
        doc=BeautifulSoup(req.content, 'html.parser') #get source code ..convert to string
        return doc

   
    #extracting links of subpages from the main page of the given website
    def extract_links(self):
       
        li_tags=self.source_code.find_all("li") #source code of the main website adress
        
        #list of lists .. every list has on element  .. <a> </<a>
        a_tags= [li.find_all("a", href=True) for li in li_tags]
        #extract links from li-elements
        links=[ a_tags[i][0]['href'] for i in range(len(a_tags)) if len(a_tags[i]) !=0 ]
        #check if the subpages has full adress link
        full_links=[]

        for link in links:
            # if a link not full link like   /studier then add the full extension
            if re.search("^/.*", link): #Check if the string starts not full url adress
                full_link=self.url+link
                full_links.append(full_link)
            else:
                 full_links.append(link)

        return full_links
       
    
    #extracting the source code of subpages
    def extract_subpages(self):
        
        subpages=[]
        
        links=self.extract_links()
        
        if self.depth>len(links):
            raise Exception("Depth cannot be bigger than the total nr. subpages!")
            
        else:     
            return [self.read_htmlFile(link) for link in links[:self.depth]]
        
    
    #extract the textual and numeric content of  html-file- observe numbers and special data are included
    def extract_content(self): 
       
        #source code of all_pages, included the main page
        soups=self.extract_subpages()
        soups.append(self.source_code) #add the source code of main page to the subpages' source code
        
        texts=[]
        for soup in soups:
            tag = soup.body
            
            for string in tag.strings:
                #st=string.rstrip()
                if len(string)>1:

                    st=string.strip()
                    #tolowercase
                    #remove nrs 
                    texts.append(st)
                #print(st) 
                #remove digits
        return texts
    
    
    def wild_re(self):
        matches=[]
        links=self.extract_links()
        links.append(self.url)
        for i in range(self.depth+1):
            html_file=urllib.request.urlopen(links[i])
            bytes_file=html_file.read()  #Bytes class
            text_file = bytes_file.decode('utf-8') # to string class
            result=re.findall(self.re_specialD, text_file )
            if len(result)!=0:   
                matches.append(result)
        return matches
        """ another way to do the same
        main=self.source_code
        #print(main)
        x= main.find_all(re.compile(self.re_specialD))
        #re.findall(, main)
        return  x  
        """       
       
    
    def extract_comments(self):
       
        links=self.extract_links()[:self.depth]
       
        dic={}
        pages=self.extract_subpages()
        pages.append(self.source_code)
        
        for i in range(len(pages)):
            
            comments = pages[i].find_all(string=lambda text: isinstance(text, Comment))
            if i <len(links):
                dic[links[i]]=comments
            else:
                dic[self.url]=comments
       
        return dic
    
   
        #testing with prices
        #https://www.komplett.no/category/11156/pc-nettbrett/pc-baerbar/laptop/alle-baerbare-pc-er
    
    def extract_emails(self):
        
        emails=[]
        
        #gather the source code of all pages, included the one of the main page
        pages=self.extract_subpages()
        pages.append(self.source_code)
        
        for source_code in pages:
            #a_tags which represent e-mails as following: <a hrf="mailto: xx@xxxx.xxx"> ... </a>
            emails_asLinks= source_code.find_all('a', attrs={"href" : re.compile("^mailto")})
            emails_str=[emails_asLinks[i].string for i in range( len(emails_asLinks))]
            emails.extend(emails_str)
            
       #search inside all the texts for  all pages (the main page and  subpages)
        content=self.extract_content()
        for string in content:
             #match email which starts with any word, pluss @ pluss any word pluss any domain name.
            x= re.findall(r"\w+@\w+\.\w+",string)
            if len(x)!=0: #if there is a match, add it to the list
                emails.append(x[0])
        return  emails
    

    
    def extract_tlfnrs(self):
        tlfnumbers=[]
        content=self.extract_content()
        regex="(^0047|\+47|47( |-|.)?)?(\d\d){1}( |-|.)?(\d\d){1}( |-|.)?(\d\d){1}( |-|.)?(\d\d){1}"
        for txt in content:

            match=re.findall(regex,txt)
            #print(match)

            if match is not None:
                for tlfnr in match: #one or more tlfnr.(s) found in a text
                    string="".join(tlfnr)
                    tlfnumbers.append(string)

        return tlfnumbers
    
    
    
    def cleaned_data(self):
        #self.series= [line.strip() for line in f.readlines()] 
        
        special_chars=r"!#$%&\"()*+,-./:;<=>?@[\]^_`{|}~"
        nrs=["0","1","2","3","4","5","6","7","8","9"]
        cleaned_strings=[]
        content=self.extract_content()
        
        if len(content)==0:
             raise Exception("No data to clean!")
         
        #removing empty strings
        no_emptyStrings =[string for string in content if string!="" ]
            
        for string in no_emptyStrings:
            temp= [char for char in string if char not in special_chars and char not in nrs]  #and char not in str(nrs) 
            cleanen_string="".join(temp) 
            cleaned_strings.append( (cleanen_string.lower()).strip() )
                
        return cleaned_strings
    
      # It translates BT tages into WordNet-tags   #this simple method borrowed  from stackoverflow:     #https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
    def __to_wordnet_tag(self, treebank_tag):
       
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'): # or treebank_tag.startswith('S')
            return wordnet.ADV
        return ''

    
    def tagging(self): #return a matrix where every list represent a sent. [ [(word,its tag), (..,..), ],[..]]
        taggedStrs_Treebank=[]
        taggedStrs_WordNet=[]
        cleaned_data=self.cleaned_data()
        if len(cleaned_data)==0:
             raise Exception("No data to tag! Call clean_data() first! ")
        
        for string in cleaned_data:
            if len(string)!=0:
                taggedWords_tb=nltk.pos_tag(string.split())
                taggedStrs_Treebank.append(taggedWords_tb)           
                to_wornetPosTags=[ (pair[0], self.__to_wordnet_tag(pair[1]))  for pair in taggedWords_tb ]
                taggedStrs_WordNet.append(to_wornetPosTags)
        return  taggedStrs_WordNet
    
    
    def lemmatizing_and_freq(self):
        lemmatizer=WordNetLemmatizer()
       
        stop_words = stopwords.words('english')  #179words  ..  pronouns (I me yours), propositions, wh-questions,common verbs (do have be), auxulary verbs, common adverbs
        #adding some unwanted words which I found in the series and they are not in the stop words list
        newStopWords = ["they're","i'm","i'll","that's","we're",'not',"that's","i've","he'll","he's","mr","expandmore","o'","can't","there's"]
        stop_words.extend(newStopWords)
        """  """
        lemmatized_strs=[]    
        
        for tagged_str in self.tagging():
            
            lemmatized_str=[]
    
            for pair in tagged_str:
                to_lower=pair[0].lower()
                if pair[1]!='' and to_lower not in stop_words:
                    lemmatized_str.append( lemmatizer.lemmatize(to_lower, pos=pair[1]))
            if len(lemmatized_str)!=0:
                lemmatized_strs.append(lemmatized_str)

            for word in lemmatized_str:

                if word in self.lemmas_with_freq:
                        self.lemmas_with_freq[word]+=1
                else:

                        self.lemmas_with_freq[word]=1
        #We need to sort the lemmas base on their frequency and  return them as a dic. But no, direct way to do.
        #But we can use Operator to sorted them as list of tuples-Every tuple has to elements (word, its freq).
        sorted_lemmas_asList= sorted(self.lemmas_with_freq.items(), key=operator.itemgetter(1), reverse=True)
        
        #then empty the dic- no need for the usorted values. 
        sorted_lemmas_asDic={}
        
        #At the end we convert the list of tuples into a dic, and add them to our empty dic (=self.lemmas) 
        #we  This is why we need convert the list of tuples to dic
        for i in range(len(sorted_lemmas_asList)):
            sorted_lemmas_asDic[sorted_lemmas_asList[i][0]] = sorted_lemmas_asList[i][1]
        return sorted_lemmas_asDic
    
    
    def get_WNtags_freq(self): 
        # return a sorted dic highest to lowest vals {tag:freq,...} 
        
        tags_and_freq={}
        
        for sent in self.tagging():#sent for sentence or string
            for i in range(len(sent)):
                
                if  sent[i][1] not in tags_and_freq:
                    tags_and_freq[sent[i][1]]=1
                else:
                    tags_and_freq[sent[i][1]]+=1  
        
        sorted_tags= sorted(tags_and_freq.items(), key=operator.itemgetter(1), reverse=True)
        
        tags_and_freq={}
        
        for i in range(len(sorted_tags)):
            tags_and_freq[sorted_tags[i][0]] = sorted_tags[i][1]
                        
        return tags_and_freq
    
    
    def statistics_on_data(self): 
            #return matrix (one column, 6 rows )     
            #statistics on frequency of:   lemmas  vs. phV-es 
            statistics=[]

            lemmas=[list(self.lemmas_with_freq.values()) ]
            mean, median, mode, rng, variance, std=[],[],[],[],[],[]
            for part in lemmas:
                stats_model=""
                #an object of Class statistical_model
                stats_model=statistical_model(part)
                mean.append(stats_model.mean())
                mode.append(stats_model.mode())
                median.append(stats_model.median())
                rng.append(stats_model.rng())
                variance.append(stats_model.variance())
                std.append(stats_model.std())

            statistics=[mean, median, mode, rng, variance, std]    
            return statistics
        
        
    def visualize_lemmas_freq(self): 
   
        plt.title(" lemmas frequency of the chosen series ")
        plt.xlabel("index of lemmas", color="red")
        plt.ylabel("frequency",color="red")
        index_words=[i for i in range(0, len(self.lemmas_with_freq.keys()))]     
        plt.scatter(index_words, list(self.lemmas_with_freq.values()), c='green',marker='.'  )
        
        plt.show()
        
      
#....................test area.........................    

def main():
    wc=Web_Crawler("https://schibsted.com/", 3,  ".*master.*" )
    #Obs. to test a part of the code just uncomment it! 
    
    #print(wc.extract_links())
    #print(wc.extract_subpages())
    #print(wc.extract_content())
    
    """
    wc=Web_Crawler("https://www.oslomet.no/om/kontakt", 3,  ".*master.*" )
    print(wc.extract_emails())
    """
    
    """
    wc=Web_Crawler("https://oslomet.no/", 3,  ".*master.*" )
    print(wc.extract_tlfnrs()) 
    """

    #print(wc.extract_comments())
    #print( wc.cleaned_data())
    #print(wc.tagging())
    #print(wc.lemmatizing_and_freq())
    
    """
    Obs. Please, don't forget to run the class Statstical_model!
    
    wc=Web_Crawler("https://schibsted.com/", 10,  ".*master.*" )
    WNtagsFreq_table=pd.DataFrame(index=["tag", "frequency"],columns=["other tags","nouns","verbs", "adverbs","adjectives"],
                              data=[(wc.get_WNtags_freq()).keys(), (wc.get_WNtags_freq()).values()] )
    display(WNtagsFreq_table) #a table shows TB-tags and their frequency
    """
    
    """
    
    wc=Web_Crawler("https://schibsted.com/", 10,  ".*master.*" )
    wc.lemmatizing_and_freq()
    st_data= wc.statistics_on_data()
    stats=pd.DataFrame( index=["mean", "median", "mode", "range", "variance", "std"],
                            columns=["statstics on the lemmas "] ,
                            data=[st_data[0],st_data[1],st_data[2],st_data[3],st_data[4],st_data[5]] )
    display(stats) #statistics on the previous tables
    """
    
    """
    wc.lemmatizing_and_freq()
    vis=wc.visualize_lemmas_freq()
    display(vis)
    """
    
 
if __name__ == "__main__":
   main()




   


# In[ ]:


"""
new tasks: 
-make a class diagram
-move some sentence from implimentation to evaluation
-visualse first 15 words .... stop words
-extract key words

"""


# In[122]:


#a supporting class

class statistical_model():
   
    def __init__(self, data):  
        
        self.data = data  #av type list
        
        if len(self.data)==0:
            raise Exception("Your array is empty. You need to call lemmatizing_and_freq() first!!")
        if type(self.data) != list:
            raise Exception("Your data  must be of type 'list'! ")
                         
    def max(self):   
        max_v=self.data[0]       
        for obs in self.data:
            if obs > max_v:
                max_v=obs
        return max_v
    
    def min(self):
        min_v=self.data[0]
        for obs in self.data:
            if obs < min_v:
                min_v=obs
        return min_v
       
    
    def rng(self):
        return self.max()-self.min()
        
    def mode(self):
        """
        fre_dic{obsrvation: frequency, ....}
        return an integer, the most frequent observation
        """
        freq_dic={} 
        
        for obs in self.data:
            if obs in freq_dic:
                freq_dic[obs] +=1
            else:
                 freq_dic[obs] =1
               
        keys = list(freq_dic.keys())
        vals = list(freq_dic.values()) 
                 
        pos=vals.index(max(vals))  #index of the most freq. val
        
        return keys[pos] 
    
    
    def median(self):
        """
        #if case the length og data is even number, we take the average of the two middle values
        """
        sorted_data= sorted(self.data)
        
        if (len(sorted_data)%2)==1: #check if n is odd nr.
            return sorted_data[int(len(sorted_data)/2)]
            
        else:
            
            return( sorted_data[int(len(sorted_data)/2 )-1 ] + sorted_data[int(len(sorted_data)/2)]  ) / 2
              
            
    def mean(self): 
        count=0
        for obs in self.data:
            count+=obs
            
        return count/len(self.data)        
              
        
    def variance(self):
        mn=self.mean()
        
        sub_from_mean=[i-mn for i in self.data]
        
        squred_vals=[i*i for i in sub_from_mean]   #squre the values
       
        count=0
        for  value in squred_vals:
            count+=value 
           
        return count/(len(squred_vals)-1)
    
    
    def std(self):
        return (self.variance())** 0.5   #The square root
     
    
    def quartiles(self):
        sorted_data= sorted(self.data)
       
        obj1=statistical_model(sorted_data[0:int(len(sorted_data)/2)]) #  a new data set, from pos.0-median to find Q1
        obj2=statistical_model(sorted_data[int(len(sorted_data)/2)+1:]) #  a new data set, from pos.median to -1  to find Q1
        
        #find quertiles
        Q1=obj1.median() 
        Q2=self.median()
        Q3=obj2.median()

        #find inter-quertile
        interQ= Q3-Q1
        return Q1,Q2,Q3, interQ
    
    def z_scores(self):        
        return [(obs-self.mean())/self.standard_diviation() for obs in self.data]

    
    def detect_outliers(self):
        """parms:
        dataset: type list 
        Q1 and Q3 stands for quertile 1, quertile 3. type float
        interQ stands for interquertile.
        return: 
        list of outliers if any exits, otherwise it return empty array
        """    
        Q1, Q3, interQ= self.quartiles()[0], self.quartiles()[2], self.quartiles()[3]
        outliers=[]
        for obs in self.data:
            if obs< Q1-(interQ*1.5) or obs>Q3+(interQ*1.5):
                outliers.append(obs)
        return outliers


# In[ ]:





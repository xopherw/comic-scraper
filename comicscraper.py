import requests, re, bs4, os, shutil

# get image contents from url
def urlgrab(issues_url):
    r = requests.get(issues_url)
    html_read = bs4.BeautifulSoup(r.text,features="html.parser").findAll('img')
    comic_urls = [requests.get(i.get('src')).content for i in html_read[1:]]
    return comic_urls

# download images
def imgDown(folder, title, content):
    for i,j in enumerate(content):
        f = open(f'{os.getcwd()}/{folder}/{title} page {i+1}.jpg','wb')
        f.write(j)
        f.close

# create folder
def mkdir(foldername):    
    os.mkdir(os.getcwd()+f'/{foldername}')

# get all the issues from the main comic era
def issues(url):
    return [i.get('href') for i in bs4.BeautifulSoup(requests.get(url).text,features="html.parser").findAll('a', {'class' : 'ch-name'})]

# only use this when issued numbers are specified
def collector(chaptername, url):
    for i,j in enumerate(sorted(issues(url)), 1):
        foldername = f"{chaptername} #Issue {i}"
        mkdir(foldername)
        imgDown(f'{foldername}', f'{chaptername} #{i}', urlgrab(f'{j}/full'))

# compress all folders to zip and change to cbr format, then delete folders
def cbrized():
    for k in os.listdir(os.getcwd()):   
        if(os.path.isdir(k)):   #find all the folders only
            os.rename(shutil.make_archive(k,'zip',k), k+'.cbr') # convert folder to zip and rename to foldername.cbr
            shutil.rmtree(f'{os.getcwd()}/{k}') # delete the folder

# regex pattern to detect if it's a url
pattern = r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
print()
print('Welcome to my comic downloader service!')
print('The ouput of each downloaded comic will be in .cbr file')
print('and the output given name will be for example: [comic_name #Issue X (where X is a number)')
print('This program only works on viewcomics.me\n')

while(True):
    url = input('Comic URL source (only from viewcomics.me): ')
    print()
    
    # ends program when entered 'quit' or q, case insensitive
    if(url.lower() == 'quit' or url.lower() == 'q'): 
        print("Program is finished, thanks for choosing this service!")
        break
    # check if is url
    if(not(re.match(pattern,url))):
        print('Please proved a proper url.\n')
        
    else:
        title = input('Title of the comic: ')
        print()
        try:
            print('Printing comics, please wait...\n')
            collector(title, url)
            cbrized()
            print("Done!\n")
            
        except Exception:    
            print('If you are using viewcomics website, please check the url again. If not, this program only work on viewcomics website.\n')
            continue




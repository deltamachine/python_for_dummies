import os
import re
import html
import urllib.request

def request (link):
    req = urllib.request.Request (link)
    with urllib.request.urlopen(req) as response: 
       html = response.read().decode('utf-8')
    return html

def create_a_link (link):
    link = 'http://www.evening-kazan.ru' + link
    return link

def next_and_last (html):
    not_the_first = []

    last_page = re.search ('<li class="pager-last last"><a href="(.*?page=)([0-9]*)" title', html)
    if last_page != None:
        j = last_page.group(2)

    i = 1 
    
    while i <= int(j):
        link = 'http://www.evening-kazan.ru' + last_page.group(1) + str(i)
        not_the_first.append (link)
        i += 1

    return not_the_first

def find_metadata (text):
    metadata = {}

    author = re.search ('<div class="author heading--meta">(.*?)<', text)
    if author != None and author != 'ВК':
        metadata['author'] = author.group(1)
    else:
        metadata['author'] = 'NoName'

    header = re.search ('<title>(.*?) \|.*?</title>', text)
    if header != None:
        metadata['header'] = header.group(1)

    created = re.search ('<div class="submitted heading--meta">([0-9]*?\.[0-9]*?\.([0-9]*?)) .*?', text)
    if created != None:
        metadata['created'] = created.group(1)
        metadata ['publ_year'] = '20' + created.group(2)
    else:
        metadata ['created'] = 'Unknown'
        metadata ['publ_year'] = 'Unknown'

    topic = re.search ('rel="tag" title="">(.*?)</a></li>', text)
    if topic != None:
        metadata['topic'] = topic.group(1)
    else:
        metadata['topic'] = ''
    
    return metadata

def clean_article (text):
    regTag = re.compile('<.*?>', flags=re.DOTALL)
    regScript = re.compile('<script>.*?</script>', flags=re.DOTALL)
    regComment = re.compile('<!--.*?-->', flags=re.DOTALL)
    regSpace = re.compile('\s{2,}', flags = re.DOTALL)

    m = re.search ('</head>(.*?)<aside id="sidebars-wrap">', text, flags=re.DOTALL)
    if m != None:
        text = m.group(1)

    clean_text = regTag.sub("", text)
    clean_text = regSpace.sub("\n", clean_text)
    clean_text = regScript.sub("", clean_text)
    clean_text = regComment.sub("", clean_text)
    
    regHeads = re.findall ('((?:[А-Я]|[0-9]).*?[^\.?!]\n)', clean_text)
    for head in regHeads:
        clean_text = re.sub(head, '', clean_text)

    clean_text = html.unescape(clean_text)

    clean_text = re.sub('View the discussion thread.', '', clean_text)
    
    return clean_text

def metadata_table(metadata):
    os.chdir ('C:/evening-kazan/')
    info = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tреспубликанская\t%s\tВечерняя Казань\t\t%s\tгазета\tРоссия\tТатарстан\tru\n'
    with open ('info.csv', 'a', encoding = 'utf-8') as file:
        file.writelines (info % (metadata['path'], metadata['author'], metadata['header'], metadata['created'], metadata['topic'], metadata['source'], metadata['publ_year']))    
        
def create_a_catalog():
    paths = ['C:/evening-kazan/plain/', 'C:/evening-kazan/mystem-xml/', 'C:/evening-kazan/mystem-plain/']

    for path in paths:
        os.makedirs(path + 'Unknown')
        for i in range (2010, 2017):
            for j in range (1, 13):
                if j<10:
                    newpath = path + str(i) + '/' + '0' + str(j)
                else:
                    newpath = path + str(i) + '/' + str(j)
                if not os.path.exists(newpath):
                    os.makedirs(newpath)

def create_file_name (path):
    inpt = os.listdir (path)
    number = len(inpt) + 1
    file_name = 'article' + str(number) + '.txt'
    return file_name

def create_paths (metadata):
    data = metadata['created']
    
    month = re.search ('\.([0-9][0-9])\.', data)
    month = month.group(1)

    paths = {}

    if data == 'Unknown':
        paths['path'] = 'C:/evening-kazan/plain/' + metadata['publ_year'] + '/'
        os.chdir (paths['path'])
        paths['file_name'] = create_file_name (paths['path'])
        paths['full_path'] = paths['path'] + paths['file_name']
        paths['mystem_xml_path'] = 'C:/evening-kazan/mystem-xml/' + metadata['publ_year'] + '/' + paths['file_name']
        paths['mystem_plain_path'] = 'C:/evening-kazan/mystem-plain/' + metadata['publ_year'] + '/' + paths['file_name']
    else:
        paths['path'] = 'C:/evening-kazan/plain/' + metadata['publ_year'] + '/' + month + '/'
        os.chdir (paths['path'])
        paths['file_name'] = create_file_name (paths['path'])
        paths['full_path'] = paths['path'] + paths['file_name']
        paths['mystem_xml_path'] = 'C:/evening-kazan/mystem-xml/' + metadata['publ_year'] + '/' + month + '/' + paths['file_name']
        paths['mystem_plain_path'] = 'C:/evening-kazan/mystem-plain/' + metadata['publ_year'] + '/' + month + '/' + paths['file_name']
    
    return paths

def mystem(paths):
    os.system ('C:/mystem.exe ' + paths['full_path'] + ' ' + paths['mystem_plain_path'] + ' -cnid --format text')
    os.system ('C:/mystem.exe ' + paths['full_path'] + ' ' + paths['mystem_xml_path'] + ' -cnid --format xml')

def crawler ():
    final_results = []

    main_link = 'http://www.evening-kazan.ru/categories/ekonomika.html'
    html = request (main_link)
    
    not_the_first = next_and_last (html)
    not_the_first.insert (0, main_link)

    for link in not_the_first:
        html = request (link)
        links_articles = re.findall ('/articles/.*?\.html', html)
        for link in links_articles:
            link = create_a_link (link)
            if link not in final_results:
                final_results.append (link)
    
    return final_results

def main():
    create_a_catalog()

    final_results = crawler()

    for link in final_results:
        try:
            text = request (link)

            metadata = find_metadata (text)

            paths = create_paths (metadata)

            metadata['path'] = paths['full_path']
            metadata['source'] = link

            clean_text = clean_article (text)

            with open (paths['file_name'], 'w', encoding = 'utf-8') as file:
                file.writelines (clean_text)

            mystem (paths)

            with open (paths['file_name'], 'r+', encoding = 'utf-8') as file:
                info = '@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n'
                data = file.readlines()
                file.seek(0)
                file.writelines (info % (metadata['author'], metadata['header'], metadata['created'], metadata['topic'], metadata['source']))
                file.writelines (data)

            info = metadata_table(metadata)

        except:
            print ('Error at page', link)

if __name__ == '__main__':
    main()

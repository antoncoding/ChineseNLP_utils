from bs4 import BeautifulSoup, Comment
from sys import argv
import requests

def process_text(text):
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def super_crawler_v1(url, verbose=False):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    raw = requests.get(url, headers=headers)
    html = raw.text
    soup = BeautifulSoup(html, 'html.parser')
    title = str(soup.title)
    if verbose:
        print('Original # of descendants: {}'.format(len(list(soup.descendants))))

    # Remove list of links
    for li in soup.find_all('li'):
        if li.find('a') != None:
            li.decompose()

    # Remove Table
    for table in soup.find_all('table'):
        table.decompose()

    if verbose:
        print('# of descendants after removing url lists: {}'.format(len(list(soup.descendants))))

    # Remove Header, Footers
    try:
        soup.header.decompose()
    except:
        pass
    try:
        soup.head.decompose()
    except:
        pass
    try:
        soup.footer.decompose()
    except:
        pass
    try:
        for element in soup.find_all(text=lambda text: isinstance(text, Comment)):
            element.extract()
    except:
        pass

    if verbose:
        print('# of descendants after removing headers and footers: {}'.format(len(list(soup.descendants))))

    # Delete Javascript
    for script in soup(["script", "style", "select"]):
        script.decompose()    # rip it out

    if verbose:
        print('# of descendants after removing Javascript: {}'.format(len(list(soup.descendants))))

    for e in soup.find_all('br'):
        e.decompose()

    for i in soup.find_all('img'):
        i.decompose()

    # Delete Links in nav bars...etc
    for a in soup.find_all('a'):
        try:
            if a.parent.name not in ['p','span']:
                a.decompose()
        except:
            pass

    if verbose:
        print('# of descendants after removing links: {}'.format(len(list(soup.descendants))))

    text = soup.get_text()
    text = process_text(text)

    return soup, text, title


def recursive_get_content(soup, pre=None, dic={}):
    '''
    recursive function to calculate the most important tag among all paths.
    '''
    generation_name = pre
    if pre==None:
        pre = '_'
    else:
        pre = pre + soup.name

    if soup.findChild() != None:
        child = soup.findChild()
        r_dic = recursive_get_content(child, pre=pre,dic=dic)
        dic = r_dic

    if soup.find_next_sibling() != None :
        sibling = soup.find_next_sibling()
        return_dic = recursive_get_content(sibling, pre=generation_name, dic=dic)
        dic = return_dic

    c = ''
    try:
        for content in soup.contents:
            if str(content)[0] != '<':
                c+=content.strip('\n')
    except Exception as e:
        pass

    if len(c)>3:
        dic[pre] = c + dic.get(pre,'')

    return dic


def get_main_content(soup, return_dic=False):
    '''
    input: (processed) bf object
    output: main text (string)
    '''
    content_mapping = recursive_get_content(soup,pre=None, dic={})
    length = 0
    longest = ''
    for k, c in content_mapping.items():
        if len(c.strip())>length and k!='_':
            length = len(c)
            longest = c
    if return_dic:
        return longest, content_mapping
    return longest


if __name__ == '__main__':
    url = argv[1]
    soup, text, title = super_crawler_v1(url)
    content, detail_dictionary = get_main_content(soup, True)
    print(title + ':' + content)

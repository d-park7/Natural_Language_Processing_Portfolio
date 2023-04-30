# Jonathan Ho and David Park
# CS 4395


import requests
import time
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
}


# Function to build the text files to insert into Dialogflow's Knowledge Base
def build_kb(r_list):
    
    for dict in r_list:
        for key, value in dict.items():
            kb_name = str(key) + ".txt"
            with open(kb_name, 'a', encoding='utf-8') as file:
                file.writelines(value)


# Function to remove any duplicate links
def remove_dupes():
    url_list = []

    with open('urls.txt', 'r') as f:
        urls = f.read().splitlines()
    for u in urls:
        url_list.append(u)

    # List comprehension to remove any duplicate links
    new_list = []
    [new_list.append(x) for x in url_list if x not in new_list]

    # Create new txt file with no dupes
    with open('unique_urls.txt', 'w') as nf:
        for link in new_list:
            nf.write(str(link) + '\n')


# Function to webcrawl given a link
def web_crawler(link):
    r = requests.get(link, headers=HEADERS)

    data = r.text
    soup = BeautifulSoup(data, features="lxml")

    # Writes URLs to recipes to a urls.txt file
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a', class_='bylink comments may-blank'):
            link_str = str(link.get('href'))
            if "mod_psa" not in link_str:
                f.write(link_str + '\n')

# Function to find the original poster's comment for ingredients and instructions
def find_op_comments_from_url(unique_links_to_crawl):
    with open(unique_links_to_crawl, 'r') as file:
        links = file.readlines()
        recipe_list = list()
        for link in links:
            reqs = requests.get(link, headers=HEADERS)
            data = reqs.text
            soup = BeautifulSoup(data, features='lxml')
            
            # Get relevant information of the op and the post
            main_post = soup.find('div', id='siteTable')
            op = main_post.find('a', attrs={'class': 'author'}).text
            title = main_post.find('a',attrs={'class':'title'}).text
            print(title) # Should be getting titles of each post and outputting in terminal
            comment_area = soup.find('div', attrs={'class':'commentarea'})
            comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})

            # Get all comments from the original poster and store into list
            extracted_comments = []
            for comment in comments: 
                if comment.find('form'):
                    commenter = comment.find('a',attrs={'class':'author'}).text
                    if op == commenter:
                        comment_text = comment.find('div',attrs={'class':'md'}).text
                        extracted_comments.append(comment_text)

            # Get the comment about the recipe
            recipe_comment = extracted_comments[0]

            # Find the longest comment from the op (implying the instructions and ingredients)
            for x in range(len(extracted_comments)):
                if len(recipe_comment) < len(extracted_comments[x]):
                    recipe_comment = extracted_comments[x]
            recipe_list.append({title:recipe_comment})

    return recipe_list


if __name__ == '__main__':
    link_to_crawl = 'https://old.reddit.com/r/recipes/'
    
    web_crawler(link_to_crawl)
    remove_dupes()

    time.sleep(3)
    recipe_list = find_op_comments_from_url('unique_urls.txt')

    # Creating the knowledge base
    build_kb(recipe_list)
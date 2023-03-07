import requests
from bs4 import BeautifulSoup

def crawler():
    starter_url = "https://www.youtube.com/"

    reqs = requests.get(starter_url)

    data = reqs.text
    soup = BeautifulSoup(data, features="lxml")

    counter = 0
    with open('urls.txt', 'w') as file:
        # find_all('a') finds all article tags
        for link in soup.find_all('a'):
            print(link.get('href'))
            file.write(str(link.get('href')) + '\n\n')
            if counter > 20:
                break
            counter += 1
    print('end of crawler')


if __name__ == "__main__":
    crawler()
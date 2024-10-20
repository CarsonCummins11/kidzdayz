from playwright.sync_api import sync_playwright, Page, ElementHandle
import re, os
import requests
from typing import Union, List

class Image:
    def __init__(self, remote_url:str, title:str):
        self.remote_url = remote_url
        self.title = title
        assert ' ' not in title
        self.local_url = self.download_image()
    def download_image(self) -> str:
        remote_name = self.remote_url.split('/')[-1]
        remote_type = remote_name.split('.')[-1]
        local_name = f'blog/img/{self.title}.{remote_type}'
        open(local_name, 'wb+').write(requests.get(self.remote_url).content)
        return local_name.replace('blog/', '')
    def render(self):
        self.download_image()
        return f'<div class="image_div"><img class="image" src="{self.local_url}"></div>'

class BlogPost:
    def __init__(self, title:str, date:str, content:List[Union[str,Image]]):
        self.title = title
        self.date = date
        self.content = content
        self.file_title = re.sub(r'\W+', '_', title)
    
    @staticmethod
    def extract_from_element(element: ElementHandle):
        title = element.query_selector('.post-title').inner_text()
        file_title = re.sub(r'\W+', '_', title)
        date = element.query_selector('.date-header').inner_text()
        img_count = 0
        content = []
        for block in element.query_selector('.post-body').query_selector_all('.separator'):
            if block.inner_html().strip().startswith('<a'):
                img_src = block.query_selector('a').query_selector('img').get_attribute('src')
                img_count += 1
                content.append(Image(img_src, f'{file_title}_{img_count}'))
            else:
                content.append(block.inner_text())

        return BlogPost(title, date, content)

    def export_to_file(self):
        post_content = f"""
<!DOCTYPE html>
<html>
<body>
<link rel="stylesheet" href="style.css">
<h1 class="post_title">{self.title}</h1>
<h2 class="post_date">{self.date}</h2>
<div class="post">
"""
        for block in self.content:
            if isinstance(block, Image):
                post_content += block.render()+"\n"
            else:
                post_content += f'<div class="post_text">{block}</div>\n'
        post_content += """</div></body></html>
        """
        #write to blog/year/month/title.html
        # Sunday, April 9, 2017
        year = self.date.split(", ")[2].strip()
        month = self.date.split(", ")[1].strip().split(" ")[0]
        # make the directories if they don't exist
        os.makedirs(f'blog/{year}/{month}', exist_ok=True)

        with open(f"blog/{year}/{month}/{self.file_title}.html", 'w+') as f:
            f.write(post_content)


def scrape_kidzdayz_page(page: Page):
    # get all divs with the class date-outer
    posts = page.query_selector_all('.date-outer')
    for post in posts:
        try:
            blog_post = BlogPost.extract_from_element(post)
            blog_post.export_to_file()
        except Exception as e:
            pass


def scrape_all_links(url = "https://kidzdayz.blogspot.com/"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        while True:
            #scrape and export the blog posts
            scrape_kidzdayz_page(page)
            
            #click on an a element with the text "Older Posts"
            page.click('text="Older Posts"', timeout=5000)
            #wait for the page to load
            page.wait_for_load_state('networkidle')
            print(page.url)

        
scrape_all_links("https://kidzdayz.blogspot.com/search?updated-max=2010-12-29T19:20:00-08:00&max-results=7&start=1478&by-date=false")
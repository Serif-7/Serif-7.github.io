#!/run/current-system/sw/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bs4",
#     "pypandoc",
#     "pyyaml",
# ]
# ///
import os
import sys
import shutil
from convert_post_to_html import convert_post_to_html as convert_post
from convert_post_to_html import extract_metadata
from datetime import datetime
import json
from bs4 import BeautifulSoup

date_format = "%B %d, %Y" # ex. October 4, 2024
recent_posts_limit = 5 # number of recent posts to show on home page

# copy all non-draft posts into /markdown
def copy_markdown_from_obsidian():
    posts_folder = os.environ['HOME'] + "/Notes/Writing/Posts"
    for file in os.listdir(posts_folder):
        metadata = extract_metadata(posts_folder + "/" + file)
        if not metadata['draft']:
            shutil.copy2(posts_folder + "/" + file, "./markdown")        

def create_pdf_list():
    html_list = "<ol>\n"
    for file in os.listdir("pdfs"):
        # formatted_date = datetime.strptime(date, date_format).strftime("%B %d, %Y")
        filename = "pdfs/" + file
        # can click link to download
        html_list += f"  <li><a href='{filename}' download>{file}</a><p>Insert File Description here</p></li>\n"
    html_list += "</ol>"

    list_soup = BeautifulSoup(html_list, features='html.parser')

    with open("pdfs.html", "r") as f:
        pdf_soup = BeautifulSoup(f, features='html.parser')

    pdf_list = pdf_soup.find('div', {'class': 'pdf-list'})
    pdf_list.clear()
    pdf_list.append(list_soup)
    with open("pdfs.html", "w") as f:
        f.write(str(pdf_soup.prettify()))
    
    
def generate_sorted_date_list(post_data):
    dates = []
    for post in post_data:
        dates.append((post['date'], post['filename'], post['title']))
    
    # Scan the directory for HTML files
    # for filename in os.listdir(directory):
    #     if filename.endswith('.html'):
    #         file_path = os.path.join(directory, filename)
            
    #         with open(file_path, 'r', encoding='utf-8') as file:
    #             soup = BeautifulSoup(file, 'html.parser')
                
    #             # Find the date div
    #             date_div = soup.find('div', {'class': 'date'})
                
    #             if date_div and date_div.string:
    #                 # Extract the date string and append to the list
    #                 date_str = date_div.string.strip()
    #                 if date_str.startswith("Date: "):
    #                     date_str = date_str[6:]  # Remove "Date: " prefix
    #                 dates.append((date_str, filename, soup.head.title.string))

    if not dates:
        print("ERROR: No posts in given data. Exiting.")
        sys.exit(1)
    
    # Sort the dates
    # date format: 
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x[0], date_format), reverse=True)
    
    # Generate the HTML ordered list
    html_list = "<ol>\n"
    # only get first 5 posts
    for date, filename, title in sorted_dates[0:recent_posts_limit]:
        # formatted_date = datetime.strptime(date, date_format).strftime("%B %d, %Y")
        html_list += f"  <li><a href='{filename}'>{title}: {date}</a></li>\n"
    html_list += "</ol>"
    
    return html_list

def populate_recent_posts(index_file, post_data):

    with open(index_file, 'r') as f:
        index_soup = BeautifulSoup(f, features='html.parser')

    date_list_html = generate_sorted_date_list(post_data)

    soup = BeautifulSoup(date_list_html, features='html.parser')

    recent_posts = index_soup.find('div', {'class': 'recent-posts'})
    assert(recent_posts is not None)
    recent_posts.clear()
    recent_posts.append(soup)

    # print(index_soup.prettify())
    # f.write(str(index_soup))
    with open(index_file, 'w') as f:
        f.write(str(index_soup.prettify()))

    print(f"Populated recent posts of {index_file}")
    
    return


def generate_site() -> None:

    copy_markdown_from_obsidian()
    
    metadata = []

    # convert all files in /markdown to html, extract metadata, and place in /posts
    for file in os.listdir('markdown'):
        if file == 'template.md':
            continue
        if file.endswith('.md'):
            
            metadata.append(convert_post('markdown/' + file, 'post_template.html'))

    # put metadata in search.html
    with open('search.html', 'r') as f:
        soup = BeautifulSoup(f, features='html.parser')

    posts = soup.head.find('meta', {'id': 'post-data'})
    assert(posts is not None)
    posts['data'] = json.dumps(metadata)

    # replace search.html with new version
    with open('search.html', 'w') as f:
        f.write(soup.prettify())
    
    populate_recent_posts('index.html', metadata)
    create_pdf_list()
    return

if __name__ == "__main__":
    if not os.listdir('markdown'):
        print("ERROR: No files in ./markdown. Exiting.")
        sys.exit(1)
    generate_site()
    print("Generated site.")

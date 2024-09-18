#!/run/current-system/sw/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bs4",
#     "pypandoc",
# ]
# ///
from populate_recent_posts import populate_recent_posts
from convert_post_to_html import convert_post_to_html as convert_post
import os
import json
from bs4 import BeautifulSoup

# def populate_search_results_and_buttons(metadata_list):
#     with open('search.html', 'r') as f:
#         soup = BeautifulSoup(f)

#     # get unique set of tags
#     tags = set()
#     for post in metadata_list:
#         for tag in post['tags']:
#             tags.add(tag)

#     # add tag buttons
#     for tag in tags:
#         new_button = soup.new_tag()
#         new_button.string = tag

def generate_site():

    metadata = []

    # convert all files in /markdown to html, extract metadata, and place in /posts
    for file in os.listdir('markdown'):
        if file == 'template.md':
            continue
        if file.endswith('.md'):
            postname = 'posts/' + file[0:-3] + '.html'
            
            metadata.append(convert_post('markdown/' + file, 'template.html', postname))

    # put post data in search.html
    with open('search.html', 'r') as f:
        soup = BeautifulSoup(f, features='html.parser')

    posts = soup.head.find('meta', {'id': 'post-data'})
    posts['data'] = json.dumps(metadata)
    with open('search.html', 'w') as f:
        f.write(soup.prettify())
    
    populate_recent_posts('index.html', metadata)
    return

if __name__ == "__main__":
    generate_site()
    print("Generated site.")

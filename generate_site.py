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

def generate_site():

    # convert all files in /markdown to html and place in /posts
    for file in os.listdir('markdown'):
        if file.endswith('.md'):
            postname = 'posts/' + file[0:-3] + '.html'
            
            convert_post('markdown/' + file, 'template.html', postname)

    populate_recent_posts('index.html', 'posts')
    return

if __name__ == "__main__":
    generate_site()
    print(f"Generated site.")

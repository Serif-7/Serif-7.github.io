#!/run/current-system/sw/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bs4",
#     "pypandoc",
# ]
# ///

import sys
import re
import pypandoc
from bs4 import BeautifulSoup

def convert_post_to_html(markdown_file, template_file, output_file):
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML using pandoc
    content_html = pypandoc.convert_text(markdown_content, 'html', format='md')
    # print(content_html)


    with open(template_file, 'r') as f:
        template_html = f.read()

    # create Soup objects
    md_soup = BeautifulSoup(content_html, features='html.parser')
    tsoup = BeautifulSoup(template_html, features='html.parser')
    
    ### Replace placeholders in the template

    # Extract first tag, the title, and then the date
    # this removes both tags from the soup object
    title = md_soup.find().extract().string
    date = md_soup.find().extract().string
    
    tsoup.head.title = title

    # replace site-title contents with title
    tsoup.find('div', {'class': 'site-title'}).contents[0].string = f'> {title}'

    # insert content

    # reinsert the date as an isolated tag for easy lookup later
    date_tag = md_soup.new_tag('div')
    date_tag['class'] = 'date'
    date_tag.string = date
    md_soup.insert(0, date_tag)
    
    # print(tsoup.find('div', {'class': 'content'}))
    tsoup.find('div', {'class': 'content'}).clear() # remove child tags
    tsoup.find('div', {'class': 'content'}).append(md_soup)

    # Write the final HTML to the output file
    with open(output_file, 'w') as f:
        f.write(str(tsoup))

    return


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <markdown_file> <template_file> <output_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    template_file = sys.argv[2]
    output_file = sys.argv[3]

    convert_post_to_html(markdown_file, template_file, output_file)
    print(f"Converted {markdown_file} to {output_file} using template {template_file}")
    return

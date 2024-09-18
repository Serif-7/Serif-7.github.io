#!/run/current-system/sw/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bs4",
#     "pypandoc",
# ]
# ///

import sys
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
    
    ### Extract Metadata

    # Extract first tag, the title, and then the date
    # this removes all three tags from the soup object
    title = md_soup.find().extract().string
    date = md_soup.find().extract().string
    date = date.split()[1:]
    date = date[0] + ' ' + date[1] + ' ' + date[2] +' ' + date[3]
    tags = md_soup.find().extract().string
    tags = tags.split()
    tags = list(map(lambda t: t[0:-1] if t[-1] == ',' else t, tags))

    # expected formats:
    # title is at top of document, ex '# Title'
    # Date is second, ex 'Date: Sep 14 2024'
    # Tags are third, ex 'Tags: film, photography'

    
    metadata = {
        "title": title,
        "filename": output_file,
        "date": date,
        "tags": tags[1:]
    }

    ### Insert content into template
    
    tsoup.head.title = title

    # replace site-title contents with title
    tsoup.find('div', {'class': 'site-title'}).contents[0].string = f'> {title}'

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

    print(metadata)
    return metadata


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <markdown_file> <template_file> <output_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    template_file = sys.argv[2]
    output_file = sys.argv[3]

    convert_post_to_html(markdown_file, template_file, output_file)
    print(f"Converted {markdown_file} to {output_file} using template {template_file}")

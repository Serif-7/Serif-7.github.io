#!/run/current-system/sw/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bs4",
#     "pypandoc",
#     "pyyaml",
# ]
# ///

import sys
import pypandoc
from bs4 import BeautifulSoup
import yaml

def extract_metadata(markdown):
        # Split the content to get the front matter
    front_matter = markdown.split('---', 2)
    if len(front_matter) < 3:
        print("YAML front matter not found. Exiting!")
        sys.exit(1)

    # Parse the front matter as YAML
    front_matter_data = yaml.safe_load(front_matter[1])
    # print(front_matter_data)

    metadata = {}
    # Extract the tags
    metadata['tags'] = front_matter_data.get('tags', [])
    metadata['date'] = front_matter_data.get('published', [])
    
    return metadata
    
    
# convert to html and place in posts
def convert_post_to_html(markdown_file, template_file):

    if markdown_file[:8] != "markdown":
        print("Script must be run from webroot. Exiting.")
        sys.exit(1)
    
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
    # title = md_soup.find().extract().string
    # date = md_soup.find().extract().string[6:] # strike off "Date: " from string
    # tags = md_soup.find().string
    # tags = tags.split()
    # tags = list(map(lambda t: t[0:-1] if t[-1] == ',' else t, tags))

    # expected formats:
    # title is at top of document, ex '# Title'
    # Date is second, ex 'Date: Sep 14 2024'
    # Tags are third, ex 'Tags: film, photography'
    metadata = extract_metadata(markdown_content)

    #convert post title to filename, ex. 'markdown/How My Blog Works'.md -> 'posts/how_my_blog_works.html'
    output_file = markdown_file[9:-3]
    output_file = output_file.lower()
    output_file = output_file.replace(' ', '_')
    output_file += ".html"
    output_file = "posts/" + output_file

    metadata["filename"] = output_file
    metadata["title"] = markdown_file[9:-3]

    ### Insert content into template
    
    tsoup.head.title = metadata["title"]

    # replace site-title contents with title
    tsoup.find('div', {'class': 'site-title'}).contents[0].string = f'> {metadata["title"]}'

    # reinsert the date as an isolated tag for easy lookup later
    date_tag = md_soup.new_tag('div')
    date_tag['class'] = 'date'
    date_tag.string = metadata["date"]
    md_soup.insert(0, date_tag)
    
    # print(tsoup.find('div', {'class': 'content'}))
    tsoup.find('div', {'class': 'content'}).clear() # remove child tags
    tsoup.find('div', {'class': 'content'}).append(md_soup)

    # Write the final HTML to the output file
    with open(output_file, 'w') as f:
        f.write(str(tsoup))

    print(f"convert_post_to_html: metadata for post: {metadata["title"]}")
    print(metadata)
    return metadata


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <markdown_file> <template_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    template_file = sys.argv[2]

    metadata = convert_post_to_html(markdown_file, template_file)
    print(f"Converted {markdown_file} to {metadata["filename"]} using template {template_file}")

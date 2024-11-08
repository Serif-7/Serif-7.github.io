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
import os
import pypandoc
from bs4 import BeautifulSoup
import yaml

def extract_metadata_from_folder(folder) -> list:
    metadata_list = []
    for file in os.listdir(folder):
        if file == 'template.md':
            continue
        if file.endswith('.md'):
            metadata_list.append(extract_metadata_from_post(folder + "/" + file))
    return metadata_list         
        

def extract_metadata_from_post(markdown_file):

    with open(markdown_file, 'r') as f:
        markdown = f.read()

    # Split the content to get the front matter
    front_matter = markdown.split('---', 2)
    if len(front_matter) < 3:
        print("YAML front matter not found. Exiting!")
        print("File text or filename:" + markdown_file)
        print("Front Matter: ")
        print(front_matter)
        sys.exit(1)

    # Parse the front matter as YAML
    # print("Loading YAML: filename: " + markdown_file)
    # print(front_matter)
    front_matter_data = yaml.safe_load(front_matter[1])
    # print(front_matter_data)
    metadata = {}

    filename = markdown_file.split('/')[-1].split('.md')[0]
    filename = filename.lower()
    filename = filename.replace(' ', '_')
    filename += ".html"
    metadata['filename'] = filename
    print("filename: " + filename)
    
    # Extract the tags
    metadata['tags'] = front_matter_data.get('tags', [])
    if 'published' in front_matter_data:
        metadata['date'] = front_matter_data.get('published', [])
    if 'date' in front_matter_data:
        metadata['date'] = front_matter_data.get('date', [])
    metadata['updated'] = front_matter_data.get('updated', [])
    metadata['draft'] = front_matter_data.get('draft', [])
    metadata['title'] = front_matter_data.get('title', [])
    return metadata
    
    
# convert to html and place in posts
def convert_post_to_html(markdown_file, template_file):

    # if markdown_file[:8] != "markdown":
    #     print("Script must be run from webroot. Exiting.")
    #     sys.exit(1)

    metadata = extract_metadata_from_post(markdown_file)

        
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
    # metadata = extract_metadata_from_post(markdown_content)

    #convert post title to filename, ex. 'markdown/How My Blog Works'.md -> 'posts/how_my_blog_works.html'
    output_file = metadata["filename"]
    # output_file = output_file.lower()
    # output_file = output_file.replace(' ', '_')
    # output_file += ".html"
    # output_file = "posts/" + output_file

    # metadata["filename"] = output_file

    ### Insert content into template
    
    tsoup.head.title = metadata["title"]

    # replace site-title contents with title
    tsoup.find('div', {'class': 'site-title'}).contents[0].string = f'> {metadata["title"]}'

    # insert 'updated' tag
    # TODO: make `updated` a tag in the html itself and just find it
    updated_tag = md_soup.new_tag('div')
    updated_tag['class'] = 'updated'
    updated_tag.string = "Updated: " + metadata["updated"]
    md_soup.insert(0, updated_tag)

    # insert tags
    if metadata['tags']:
        string = "Tags: " + metadata['tags'][0]
        for tag in metadata['tags'][1:]:
            string = string + ", " + tag
        tag_tag = md_soup.new_tag('div')
        tag_tag['class'] = 'post-tags'
        tag_tag.string = string
        md_soup.insert(0, tag_tag)
    
    # reinsert the date as an isolated tag for easy lookup later
    # TODO: metadata is handled better now so do the same as for `updated`
    date_tag = md_soup.new_tag('div')
    date_tag['class'] = 'date'
    date_tag.string = metadata["date"]
    md_soup.insert(0, date_tag)
    
    # print(tsoup.find('div', {'class': 'content'}))
    tsoup.find('div', {'class': 'content'}).clear() # remove child tags
    tsoup.find('div', {'class': 'content'}).append(md_soup)

    # print(f"convert_post_to_html: metadata for post: {metadata["title"]}")
    # print(metadata)

    # return str(tsoup)

    # Write the final HTML to the output file
    with open(output_file, 'w') as f:
        f.write(str(tsoup))

    print(f"convert_post_to_html: metadata for post: {metadata["title"]}")
    print(metadata)
    return metadata

def convert_posts_in_folder_to_html(src_folder, template_file):
    for file in os.listdir(src_folder):
        convert_post_to_html(src_folder + "/" + file, template_file)
                


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <markdown_file> <template_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    template_file = sys.argv[2]

    metadata = convert_post_to_html(markdown_file, template_file)
    # print(f"Converted {markdown_file} to {metadata["filename"]} using template {template_file}")

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
from datetime import datetime
import json
from bs4 import BeautifulSoup
import pypandoc
import yaml

date_format = "%B %d, %Y" # ex. October 4, 2024
recent_posts_limit = 5 # number of recent posts to show on home page
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

    # Write the final HTML to the output file
    with open(output_file, 'w') as f:
        f.write(str(tsoup))

    print(f"convert_post_to_html: metadata for post: {metadata["title"]}")
    print(metadata)
    return metadata

def extract_metadata(markdown_file) -> dict:

    # check if argument is file
    if os.path.isfile(markdown_file):
        with open(markdown_file, 'r') as f:
            markdown = f.read()
    else:
        markdown = markdown_file
    # Split the content to get the front matter
    front_matter = markdown.split('---', 2)
    if len(front_matter) < 3:
        print("YAML front matter not found. Exiting!")
        print("File text or filename:")
        print(markdown_file)
        sys.exit(1)

    # Parse the front matter as YAML
    front_matter_data = yaml.safe_load(front_matter[1])
    # print(front_matter_data)
    metadata = {}
    # Extract the tags
    metadata['tags'] = front_matter_data.get('tags', [])
    if 'published' in front_matter_data:
        metadata['date'] = front_matter_data.get('published', [])
    if 'date' in front_matter_data:
        metadata['date'] = front_matter_data.get('date', [])
    metadata['updated'] = front_matter_data.get('updated', [])
    metadata['draft'] = front_matter_data.get('draft', [])
    return metadata
    
    

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
            
            metadata.append(convert_post_to_html('markdown/' + file, 'post_template.html'))

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

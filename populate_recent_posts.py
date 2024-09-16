#!/run/current-system/sw/bin/env python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bs4",
# ]
# ///

import sys
import os
from bs4 import BeautifulSoup

def populate_recent_posts(index_file, posts_folder):

    with open(index_file, 'w+') as f:
        index_soup = BeautifulSoup(f, features='html.parser')

        date_list_html = generate_sorted_date_list(posts_folder)

        soup = BeautifulSoup(date_list_html, features='html.parser')

        recent_posts = index_soup.find('div', {'class': 'recent-posts'})
        recent_posts.clear()
        recent_posts.append(soup)

        f.write(str(soup))
    return

def generate_sorted_date_list(directory):
    dates = []
    
    # Scan the directory for HTML files
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                
                # Find the date div
                date_div = soup.find('div', {'class': 'date'})
                
                if date_div and date_div.string:
                    # Extract the date string and append to the list
                    date_str = date_div.string.strip()
                    if date_str.startswith("Date: "):
                        date_str = date_str[6:]  # Remove "Date: " prefix
                    dates.append((date_str, filename, soup.head.title))
    
    # Sort the dates
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x[0], "%a %b %d %Y"), reverse=True)
    
    # Generate the HTML ordered list
    html_list = "<ol>\n"
    # only get first 5 posts
    for date, filename, title in sorted_dates[0:5]:
        formatted_date = datetime.strptime(date, "%a %b %d %Y").strftime("%B %d, %Y")
        html_list += f"  <li><a href='/posts/{filename}'>{title}: {formatted_date}</a></li>\n"
    html_list += "</ol>"
    
    return html_list

    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: uv run populate_recent_posts.py <index.html> <posts_folder>")
        sys.exit(1)

    index_file = sys.argv[1]
    posts_folder = sys.argv[2]

    populate_recent_posts(index_file, posts_folder)
    print(f"Populated recent posts of {index_file} with directory {posts_folder}.")

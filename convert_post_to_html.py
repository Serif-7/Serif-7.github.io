#!/run/current-system/sw/bin/env python

import sys
import re
import pypandoc

def convert_post_to_html(markdown_file, template_file, output_file):
    # Read the markdown file
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    # Extract the first header
    title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        # Remove the first header from the content
        # markdown_content = re.sub(r'^#\s+.+\n', '', markdown_content)
        markdown_content = markdown_content.replace(title_match.group(), "")
    else:
        title = "Untitled"

    print("Title: ", title)

    # Verify there is a date tag
    # example: Sat Sep 14 2024
    date = markdown_content.partition('\n')[0]
    print("Date: ", date)
    
    # Convert markdown to HTML using pandoc
    
    content_html = pypandoc.convert_text(markdown_content, 'html', format='md')
    # print(content_html)

    # Read the template file
    with open(template_file, 'r') as f:
        template_content = f.read()

    # Replace placeholders in the template
    final_html = template_content.replace('Template Terminal Webpage', f'{title}')
    final_html = final_html.replace('> Template', f'> {title}')
    final_html = final_html.replace('<p>Lorem Ipsum</p>', content_html)

    # Write the final HTML to the output file
    with open(output_file, 'w') as f:
        f.write(final_html)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <markdown_file> <template_file> <output_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    template_file = sys.argv[2]
    output_file = sys.argv[3]

    convert_post_to_html(markdown_file, template_file, output_file)
    print(f"Converted {markdown_file} to {output_file} using template {template_file}")

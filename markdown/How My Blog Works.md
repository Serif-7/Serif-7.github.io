---
tags:
  - technical
published: October 4, 2024
---
Having a blog is somewhat expected of career seeking techies now. Wasn't always this way. It used to be, and still is, something people did for fun, to show off their work and their website skills; As a way of contributing to the public knowledge. I used to have a Hugo blog, but didn't feel motivated to work on it. Felt very cookie cutter. I wrote one post about Morrowind and that was it. I didn't care to learn what shortcodes were or how the templating engine worked, I just wanted my posts online.

Recently I hacked together my own static site generator. I have made it according to my aesthetics and design philosophy, which is as simple and easily accessible as possible, with good documentation.

Follow along: https://github.com/Serif-7/Serif-7.github.io

It is written in python, with exactly two dependencies: `pypandoc`, which is just a binding to Pandoc and lets me convert markdown to HTML, and `BeautifulSoup`, which lets me manipulate the converted HTML. The site layout is as follows:

`index.html`: the homepage, with a recent posts list.
`search.html`: the search function. At the time of writing it allows for searching by name and sorting by tag. Eventually I will get around to sorting by date as well.
`posts/`: Obvious.

That's it. Most people don't spend much time on a stranger's blog -- I know I certainly don't -- so why make it complicated?

Two python scripts perform the site generation: `convert_post_to_html.py` and `generate_site.py`. The first one does just what it says, and is a separate file for reasons of testing. It converts an Obsidian-formatted markdown file to HTML, shoves the content into `template.html`, and puts it in `posts/`. The second has just three functions: one that gets a sorted list of dates from the available posts, one that takes that list and populates and sorts the recent posts list on the home page, and a third that orchestrates all the post converting and sorting and adds the post data to `search.html`.

And finally, to give everything the look I want, just one very messy CSS stylesheet: `terminal.css`. I'm not very good at writing CSS and don't really have any plans to get much better at it, but there are some effects I would like to add to this site at some point. A subtle background static effect to enhance the 90s atmosphere.

One more thing, the only JavaScript anywhere is a single embedded script in `search.html` to display posts based on the search query and whatever tag buttons are pressed. To be honest, I had Claude write this script as I didn't care to do it myself. Works perfectly well!

I have endeavored to make this system as exceedingly simple to understand and use as possible. I just write a post in obsidian, toss it in `markdown/`, run a script, push to github, and it's done. I enjoy having a system I know intimately, built according to my exact preferences and easily malleable according to any future whims. I have accomplished this by simply writing less code and offloading none of the responsibility for this system. I also enjoy that my site has it's own character, that it reflects me and no one else, despite it's simplicity. I personally think a person's writing will stand out more when it's on their own terms and their aesthetics. This is obvious when you read something like Gwern's blog. The visual and interactive characteristics of the site, the typography and infoboxes, make the experience more memorable than a Substack or, god forbid, Medium post.

It's my hope that, with *Ends of Lines*, I can produce writing that will be useful to someone, and perhaps be worth preserving.


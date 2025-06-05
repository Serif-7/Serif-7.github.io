+++
title = "> How to Torrent, for Dummies"
description = "Torrenting Guide"
date = 2025-06-04
+++

I was seeing people, several people, on Twitter say they didn't know how to download or use torrents, and that they were generally confused by how it all works, and considered it esoteric techie stuff. There are, of course, publicly available guides on how to use torrents and that explain the basic concepts, but I suppose I'll write my own so it's easier to bring people up to speed.

The basic problem torrenting solves is sharing files. Let's say you want to distribute a public domain book, which is perfectly legal to do. As an example, we will use *Frankenstein*. You could just have people download it directly from you, but that is relatively slow, and if you want to distribute that book to quite a lot of people, that would eat up your bandwidth and make your local network slower. So, the (oversimplified) way torrenting works is that I send the entire file to the first receiver myself. Then, I and the receiver each send *half* the file to the next receiver, and then the first receiver, the second receiver, and myself all send a *third* of the file to the next, and it proceeds like that in fourths, fifths, sixths, sevenths, eighths, ninths, tenths, and so on until we have a large enough group of people who are all sending fractional amounts of Frankenstein to anybody who might want it. This is essentially what the BitTorrent Protocol allows you to do. Instead of having a central server or site send every file, in full, directly to each person who asks for it, you have a network of people who send a little bit of the file when you announce to all of them you want it.

The way this works in practice looks like this:
1. you install a torrent client. I recommend [qbittorrent](https://www.qbittorrent.org/).
2. you find a site that distributes .torrent files (see public tracker list below)
	1. a .torrent file is essentially a list of everyone who is currently seeding the file.
3. you download a .torrent file
4. double-click on it or click the '+' symbol in qbittorrent
5. dialog pops up asking where you want to put the file on your computer
6. it downloads. Depending on the number of people seeding (actively sharing) the file it may take a while. You can see the number of seeders on the site before you download the file.
7. enjoy *Frankenstein*.

NOTE: you may notice that, even after downloading *Frankenstein*, that the file is still in your client with a '100%' next to it. That is because when you finish downloading a file via torrent, your client automatically switches to *seed mode*, and will begin actively sharing that file if the client receive a request from the network. As a person benefitting from torrents, it is your duty to give back to the community and let your files seed, if you can.

These are the basics of how to torrent. If any part of this was confusing, shoot me an email at the address at the bottom of the page and I will attempt to help you.

**Glossary:**
*Refer to this if you get confused.*
* **torrent client**: a program you install on your computer that can use .torrent files to download things.
* **tracker**: the tracker is a site that keeps track of who has downloaded which torrents. When you download a torrent from a tracker, they update the list of seeders to include you.
	* **public tracker**: a tracker open to the public, like thepiratebay.org. They can be sketchy and riddled with ads.
	* **private tracker**: a tracker closed to the public, usually invite-only. They tend to have non-popular stuff and much more dedicated users.
* **seeder**: a person seeding a torrent, meaning they are 'holding' it in their client and are ready to distribute parts of it when asked by the network. These are also called 'peers'.
* **leeching**: the act of torrenting a file.
* **seedbox**: a service that handles downloading and seeding for you.

**Popular public trackers:**
* https://1337x.to/
* https://thepiratebay.org/index.html
* https://github.com/ngosang/trackerslist?tab=readme-ov-file (big list)

NOTE: I strongly recommend you install ad blockers before using these sites, and also use your own judgement. Movie files tend to be .mkv or .mp4, and these are, in my experience, very safe. You aren't going to get a virus because of these. Same for .mp3, .flac, .opus (music) or .epub, .mobi, .azw3 (books). On the other hand, I would recommend not downloading .pdf and ESPECIALLY not .exe or .dmg files, as those are software. Do not trust torrented software, ever, as it can easily contain malware.


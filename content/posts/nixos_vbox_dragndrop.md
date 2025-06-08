+++
title = "> Bug: VirtualBox Drag and Drop and Bidirectional Clipboard not Working on NixOS"
description = ""
date = 2025-06-08
draft = false
+++

I wanted to drag and drop files from my VirtualBox VMs to my NixOS host, and also have a bidirectional clipboard. I searched my ~/Dotfiles folder for all relevant config:

```
18:  virtualisation.virtualbox.host.enable = true;
19:  virtualisation.virtualbox.guest.enable = true;
20:  virtualisation.virtualbox.guest.dragAndDrop = true;

```

Despite having `virtualisation.virtualbox.guest.dragAndDrop = true;` and `virtualisation.virtualbox.guest.clipboard = true;` in my configuration, neither of these features worked.

When I attempted to drag and drop, a window popped up with the following error:

```
DnD: Error: Dragging from guest to host not supported by guest -- make sure that the Guest Additions are properly installed and running.

Result Code: VBOX_E_DND_ERROR (0x80bb0011)
Component: GuestDnDSourceWrap
Interface: IGuestDnDSource {dedfb5d9-4c1b-edf7-fdf3-c1be6827dc28}
Callee: IDnDSource {d23a9ca3-42da-c94b-8aec-21968e08355d}

```

When I attempt to use the clipboard to transfer text, in either direction, nothing happens when I try to paste.

---
published: true
layout: post
title: rSync Files on Interval
tags: rsync docker pi armbian cli
featured: docker pi armbian cli
---

A recurring requirement for my [IOT] projects involves keeping a set of files synced with a central server. Many of these projects include media players, kiosk systems, or applications that need frequently updated configuration files, all while entirely unattended, and in most cases unreachable through firewalls. I have one project that alone has 2000+ devices pulling media continuously from an [rsync] server. Many of these devices are on doggy wifi networks.

The [rsync] utility works excellent on [Raspberry Pi] as well as an assortment of [Armbian] installed devices. However, writing scripts to manage [rsync] when it fails, or restarting it on some interval when it finishes can be a pain. I have a dozen rickety, cobbled-together [bash] hacks that have somewhat worked in the past. I needed something more stable, portable and upgradeable.

[![irsync: interval rsync](https://raw.githubusercontent.com/cjimti/irsync/master/irsync.png)](https://github.com/cjimti/irsync)

I built [irsync] to operate on any ([amd64/x86-64] or [armhf]) system that has [Docker] running on it.

An example [Docker] run command:

```bash
docker run --rm \
    -v "$(pwd)"/data:/data \
    -e RSYNC_PASSWORD=password \
    -e IRSYNC_INTERVAL=30 \
    -e IRSYNC_FROM=rsync://user@example.com:873/data/"\
    -e IRSYNC_TO=./data \
    -e IRSYNC_DELETE=true \
    cjimti/irsync
```

Say you need to ensure your device (or another server) always has the latest files from the server. However, syncing hundreds or even thousands of files could take hours or days. First [rsync] will only grab the data you don't have, or may have an outdated version of, yet you can never assume the state of the data on your device. [irsync] will use it's built-in [rsync] to the heavy lifting of determining your state versus the servers. But [rsync] is not perfect and dealing with an unstable network can sometimes cause it to hang or fail.

[irsync] manages the output of it's internal [rsync] and will restart a synchronization process if the timeout exceeds the specified directive. Most of the files I need to be synchronized are under 200 megabytes, so I sent my timeout to 2 hours per file. If a file takes longer than 2 hours to sync then I assume, there is a network or connection failure and let [irsync] start the process over.

[irsync] allows me to start a file synchronization on an interval. In other words, I want my device to sync every 10 seconds, but I don't want to start an [rsync] every 2 minutes. So if the sync takes 2 hours, then 2 hours and 2 minutes later another synchronization attempt will be made. When my device is up-to-date, these calls are relatively light on the device, and my client knows that only 2 minutes after they update their media it will likely be on it's way to their devices.

## Demo

You can run a simple little demo on your local workstation using a docker-compose file I put together.

<script src="https://gist.github.com/cjimti/6fdc17192a1b13366144ee0a92e3e3c1.js"></script>

I recorded a video performing the demo above:

<style>.embed-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; } .embed-container iframe, .embed-container object, .embed-container embed { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }</style><div class='embed-container'><iframe src='https://www.youtube.com/embed/gT_P2a-xpPw?rel=0' frameborder='0' allowfullscreen></iframe></div>


### Resources

- [irsync]
- [rsync] on Wikipedia
- [Armbian]
- [Docker]

[armhf]: https://en.wikipedia.org/wiki/ARM_architecture
[amd64/x86-64]: https://en.wikipedia.org/wiki/X86-64
[irsync]: https://github.com/cjimti/irsync
[rsync]: https://en.wikipedia.org/wiki/Rsync
[Raspberry Pi]: https://en.wikipedia.org/wiki/Raspberry_Pi
[Armbian]: https://www.armbian.com/
[bash]: https://www.gnu.org/software/bash/
[IOT]: https://en.wikipedia.org/wiki/Internet_of_things
[Docker]: https://www.docker.com/

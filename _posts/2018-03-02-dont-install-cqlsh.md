---
published: true
layout: post
title: Don't Install cqlsh
description: Don't Install cqlsh, or anything for that matter...
tags: cassandra docker cqlsh
---

Case: **Cassandra development and your local workstation.**

I use [Apache Cassandra] almost daily for my job. A lot of our services
require this high performance, highly available database. The command line
tool [`cqlsh`] is the official tool for interacting with Cassandra. [`cqlsh`] is 
an easy and intuitive terminal into [Apache Cassandra], but it has dependencies,
one of which is [Python]. Over the years of local development on my MacBook 
Pro I have had a number of tools that require [Python] and Python libraries. Some
of these tools I installed years ago require older versions of Python, or older
Python libraries not able to run in newer Python versiona. [Python] is a great 
language, but sooner or later you run into dependency nightmares, 
(see [The Nine Circles of Python Dependency Hell]) including missing libs, version 
conflicts and the list goes on. It makes sense to resolve these issues or use a 
[Python version manager](https://github.com/pyenv/pyenv)
like Ruby's [RVM](https://rvm.io/) if you are activly developing locally in 
[Python]. But wait, **im not developing in Python at the moment**, I just want to 
run [`cqlsh`] and it is not the weekend, so I am not motivated to Google my Python 
version conflicts and library dependency errors, because I have a ton of work 
to get done. Yes, my problems are likely cuased by something dumb I did 
playing around with questionable code I found in the far-off corners of Github.

We live in a world of process isolation and tools that make utilizing it extreamly 
simple, with apps like [Docker] we have the ability to perform 
dependency management with **dependency isolation**. As I am slowly becomming 
a fanboy of containerization, I look forword to the day when typing `ps` on my
local workstation or remote server is nearly synonymous with commands like `docker ps`
or `kubectl get services`.

So I'm going to ignore my confused local install of `cqlsh`, the 
broken state of my Python and the mess I made of it's libraries. I'm just going to run:

`docker run -it --rm cassandra cqlsh node1.example.com -u itsme -p mypassword`

It's a one time pull of the [Cassandra Docker] image and once im done the `--rm` flag
cleans up the stopped container. 

But that's a lot of command for me to think about when i just need my `cqlsh` so 
I add a simple alias to my `.bashrc`

`alias cqlsh='docker run -it --rm cassandra cqlsh` 

From now on I run the command `cqlsh` and get just that, will all it dependencies in isolation, 
not worried about Python versions or state of my local workstation. Just keep Docker 
running well an imgood.

This is fine for the times I just need a cqlsh terminal to issue a few commands. However
I am often needing to pass cql scripts into [`cqlsh`]. So I updated my alias to always 
mount my current directory into a `/src` directory in the container. All have have
to remember is that that path to a local file is `./src` and not `./`. 

`alias cqlsh='docker run -it --rm -v "$(pwd)":/src cassandra cqlsh`

This allows me to run commands that pass in files, like:

`cqlsh node1.example.com 9042 -f /src/setup_some_keyspace_and_tables.cql`

The [Cassandra Docker] image is 323MB, and when run without a command will start up
a fully functional Cassandra node, which is usefull for testing. However if
this is not something you need, then a 323MB image is a bit overkill. You can 
always make a small Docker image using [Alpine Linux], adding only the packages 
you need. However that is a subject of another article I suppose.

[Docker]: https://www.docker.com/
[Apache Cassandra]: http://cassandra.apache.org/
[Python]: https://www.python.org/
[`cqlsh`]: http://cassandra.apache.org/doc/latest/tools/cqlsh.html
[Cassandra Docker]: https://hub.docker.com/_/cassandra/
[The Nine Circles of Python Dependency Hell]: https://medium.com/knerd/the-nine-circles-of-python-dependency-hell-481d53e3e025
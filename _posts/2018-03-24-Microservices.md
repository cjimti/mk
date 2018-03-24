---
published: true
layout: post
title: Microservices
---

The following is a collection of articles on [Microservices]. The [Microservices] architecture is a variant of the 
[service-oriented architecture] (SOA), a collection of loosely coupled services.

#### Key Goals of Microservices
- Rapid development
- Continuous deployment

#### Best Practices
- [Version Control](https://12factor.net/codebase) - All code and **configuration** should be versioned.
- [Log to Standard Out](https://12factor.net/logs) - This unifies the log collection process.
- [Package Dependencies](https://12factor.net/dependencies) - Ensure the stability of the build process.

#### Twelve-Factor Principles
- Portable - Service (container) should be able to be run anywhere.
- Continually Deployable - Able to deploy any time without disruption.
- Scalable - Multiple copies should be able to run concurrently (stateless)

#### JSON Web Tokens (JWT) - Client -> Server trust.
- Compact, self contained method for transferring secure data as a JSON object.
- Use for Authentication and Information Exchange
- See [https://jwt.io/](https://jwt.io/)
- Server creates a token, client uses token to make requests.

#### Containers - Docker
- Docker is simply an API on top of existing process isolation technology.
- Independent packages
- Namespace Isolation

#### Alpine Linux
[Alpine Linux](https://alpinelinux.org/) **Small. Simple. Secure.** Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox.
- [Alpine container image](https://hub.docker.com/_/alpine/)
- [Docker gets minimalist with plan to migrate images to Alpine Linux](http://siliconangle.com/blog/2016/02/09/docker-gets-minimalist-with-plan-to-migrate-images-to-alpine-linux/)
- [Solomon Hykes, founder and CTO of Docker (on the move to Alpine)](https://news.ycombinator.com/item?id=11000827)

## Articles
- Background concept - ["Open Data: Small Pieces Loosely Joined"](http://radar.oreilly.com/2006/09/open-data-small-pieces-loosely.html), Tim O’Reilly
- Modern software design problems and solutions - ["12-Fractured Apps"](https://medium.com/@kelseyhightower/12-fractured-apps-1080c73d481c), Kelsey Hightower (SysAdmin @ Google)
- 12-Factor Defined - ["The 12-Factor App"](https://12factor.net/), Adam Wiggins
- Pros and Cons of Microservices - ["Microservices"](https://martinfowler.com/articles/microservices.html) and [Microservice Trade-Offs](https://martinfowler.com/articles/microservice-trade-offs.html), Martin Fowler
- ["What are containers and why do you need them?"](https://www.cio.com/article/2924995/software/what-are-containers-and-why-do-you-need-them.html) - CIO
- ["Containers bring a skinny new world of virtualization to Linux"](http://www.itworld.com/article/2698646/virtualization/containers-bring-a-skinny-new-world-of-virtualization-to-linux.html) - ITWorld

## Videos
- ["Microservices"](https://www.youtube.com/watch?v=wgdBVIX9ifA), Martin Fowler
- ["The Evolution of Microservices"](http://www.ustream.tv/recorded/86151804), Martin Fowler
- ["The State of the Art in Microservices"](https://www.youtube.com/watch?v=pwpxq9-uw_0) with Docker, Adrian Cockroft




[Microservices]: https://en.wikipedia.org/wiki/Microservices
[service-oriented architecture]: https://en.wikipedia.org/wiki/Service-oriented_architecture
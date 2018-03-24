---
published: false
layout: post
title: Helm
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

## Articles
- Background concept - ["Open Data: Small Pieces Loosely Joined"](http://radar.oreilly.com/2006/09/open-data-small-pieces-loosely.html), Tim O’Reilly
- Modern software design problems and solutions - ["12-Fractured Apps"](https://medium.com/@kelseyhightower/12-fractured-apps-1080c73d481c), Kelsey Hightower (SysAdmin @ Google)
- 12-Factor Defined - ["The 12-Factor App"](https://12factor.net/), Adam Wiggins
- Pros and Cons of Microservices - ["Microservices"](https://martinfowler.com/articles/microservices.html) and [Microservice Trade-Offs](https://martinfowler.com/articles/microservice-trade-offs.html), Martin Fowler

## Videos
- ["Microservices"](https://www.youtube.com/watch?v=wgdBVIX9ifA), Martin Fowler
- ["The Evolution of Microservices"](http://www.ustream.tv/recorded/86151804), Martin Fowler
- ["The State of the Art in Microservices"](https://www.youtube.com/watch?v=pwpxq9-uw_0) with Docker, Adrian Cockroft




[Microservices]: https://en.wikipedia.org/wiki/Microservices
[service-oriented architecture]: https://en.wikipedia.org/wiki/Service-oriented_architecture
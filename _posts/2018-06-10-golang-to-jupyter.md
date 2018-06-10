---
published: false
layout: post
title: Golang to Jupyter
tags: coding golang jupyter
featured: cli
mast: juypter
---
[Jupyter Notbooks](http://jupyter.org/) have have been a popular technology in the Python data science community for awhile now, especially in academics. Jupyter Notbooks are a way to mix inline, executable code with documentation in a presentation format. Best practices in organizing source code are not always the most effecient at communicating it's functionality to a user. 

While programming languages are intended to abstract computational complexity into a simplified language humans can read and write, they must always weigh toward the effeciency of the primary interpreter, the computer. Jupyter Notbooks are intended to communicate souce code to humans first and computers second. We can use Jupyter Notbooks to communicate to humans not only the source, but the inprepreted result.

Jupyter can use an growing number of interpreters (called [kernels](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels)) to run and render output, including my favorite, [Golang](https://golang.org/). 

Although data science expresse in Python is first and most popular use of Jupyter Notbooks I see a lot of other extreamly usefull applications, inclusing:

- Programming tutorials in a variety of languages.
- Coding Best practices and style guides.
- Any technical blog or article writing.

Beyond the ability to execute code in-line, the most usefull features to me is exporting these notebooks as Makdown. Site builders like [Jekyll](https://jekyllrb.com/) and [Hugo](https://gohugo.io/) use [Markdown](https://daringfireball.net/projects/markdown/syntax) to generate [beautiful static websites and blogs](https://gohugo.io/showcase/).

## Example

In the sections below I demonstrate simple http client call from go.


```go
import (
    "net/http"
    "io/ioutil"
    "fmt"
)

resp, err := http.Get("https://jsonplaceholder.typicode.com/posts/1")
if err != nil {
    panic(err)
}

body, err := ioutil.ReadAll(resp.Body)
if err != nil {
    panic(err)
}

fmt.Printf("RAW JSON: %s", body)
```

    RAW JSON: {
      "userId": 1,
      "id": 1,
      "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
      "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
    }




    302 <nil>



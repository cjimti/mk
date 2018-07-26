# Mk Blog

Just a personal website for development thoughts and notes.


## Maintance Notes

Run `./tag_generator.py` to generate any new tag pages in the `./tag` directory.

.


## Mathjax

```html
    <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
      extensions: ["tex2jax.js"],
      jax: ["input/TeX", "output/HTML-CSS"],
      tex2jax: {
        inlineMath: [ ['$','$'] ],
        displayMath: [ ['$$','$$'] ],
        processEscapes: true
      },
      "HTML-CSS": { fonts: ["TeX"] }
    });
    </script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js' async></script>
```

## Serve

```bash
docker run --rm -v "$(pwd)":/src -w /src -p 4000:4000 cjimti/jekyll serve --incremental -H 0.0.0.0
```
# Mk Blog

Just a personal website for development thoughts and notes.


## Maintance Notes

Run `./tag_generator.py` to generate any new tag pages in the `./tag` directory.

.


## Serve

```bash
ocker run --rm -v "$(pwd)":/src -w /src -p 4000:4000 cjimti/jekyll serve --incremental -H 0.0.0.0
```
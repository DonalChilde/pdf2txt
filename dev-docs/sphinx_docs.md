# How to setup sphinx docs

uses a split source/build layout, with an additional source/documentation directory to keep the source dir clean.

```bash
# After code changes, and
# before each release at a minimum,
# generate the api files for autodoc.
sphinx-apidoc -f -o ./source/documentation/api-generated/ ../src/pdf2txt/
```

```bash
# run this from the project/docs directory to build docs
sphinx-build -M html ./source ./build --fail-on-warning
```

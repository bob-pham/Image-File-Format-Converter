# Image-File-Format-Converter

Python script that recursively converts all images of X file type to Y file type

Places all converted files into a new nested directory called "converted_images"

### Dependencies

- [ImageMagick](https://docs.wand-py.org/en/0.6.11/guide/install.html)
- [Wand](https://docs.wand-py.org/en/0.6.11/)

### Inputs

```
-d, --directory
    Target Directory (required)
    
-i, --input
    Target Input File Type (required)
    
-o, --output
    Target Output File Type (required)
```
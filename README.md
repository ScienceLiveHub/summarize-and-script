# summarize-and-script
Summarize documents and draft simple scenarios to create social media posts

## Install dependencies

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Update config.json

The configuration file `config.json` contains the list of pdf files to process:
```
{
  "pdf_urls": [
    "https://zenodo.org/records/10672494/files/personas%20&%20interview%20STEP2Adapt.pdf"
  ]
}
```

## Process article URLs from config.json

```
python scripts/process_articles.py
```

# scrape-youtube

## YouTube

According to the latest traffic report, [YouTube](https://www.youtube.com/) has the world's second largest traffic and in **Arts & Entertainment** category, it is second to none. In last one month (June, 2020),there has been **31.05B** total visits. As the most popular Art & Entertainment content-providing systems, YouTube spans across cultures and nations, with its videos viewed by a wide range of audiences around the globe and generates a gazillion of data. Thus, learning about characteristics of YouTube videos supports the design and evaluation of personalization services, from precise advertising to recommender systems.

This repository is an honest attempt to scrape a bite of data from this huge pile with ease.

## Requirements

Modules or libraries required to run the scripts in this repository are mentnioned in `requirements.txt`. Install all the modules/ libraries mentioned there or run the following:

- In Jupyter Notebook:
  - `!pip install -r requirements.txt`
- In python scripts: _Add the following block of code._

  - ```
    import subprocess

    def install(package):
      subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    for module in open('requirements.txt', 'r'):`
      install(module)
    ```

## Instrunctions

- Run `execute.py`

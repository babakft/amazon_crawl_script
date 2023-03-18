# amazon crawl script ![coverage](https://img.shields.io/badge/coverage-89%25-green)


The Amazon crawl script is a project that helps you get information of an item from Amazon

Beside this is useful for iranian because we can't use the default amazon api 
so there is high possibility for this crawler to get banned  :neutral_face:
## how to use

To use, download the .zip and extract the contents or clone the repository by typing

```bash
git clone https://github.com/babakft/amazon_crawl_script.git
```

- Setup virtual environment for that scripts:
    - `python -m venv env`
    - `source env\bin\activate`
    - `pip install -r requirements.txt`

Run the script from the terminal through main.py and use --help to see the arguments

`python main.py --help`

the needed arguments for script

- positional arguments:
    - search_text
    - page_number
    - storage_type {mongodb,file,csv,redis}

- options:
    - -I (download images)

---

## storage explanation

mongodb: this nosql database will save the result in json format ,but you need to download mongodb compass and run it in
localhost

* Download [mongodb](https://www.mongodb.com/products/compass) from this link

redis: Redis will save data in your ram, for using this you need to run redis locally  

* check [redis](https://redis.io/docs/getting-started) to lear how to run it 

file: store data in result folder with json format

csv: store data in result folder with csv format


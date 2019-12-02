import os
import csv

from io import StringIO


config_dir = "~/.kaggle"
os.environ["KAGGLE_CONFIG_DIR"] = os.path.expanduser(config_dir)

def list(sort=None, max_size=None, min_size=None, file_type=None, license_name=None, tags=None, search=None):
    args_dict = {
        "--sort-by": sort,
        "--max-size": max_size,
        "--min-size": min_size,
        "--file-type": file_type,
        "--license": license_name,
        "--tags": tags,
        "--search": search
    }

    args = "kaggle datasets list"
    for key in args_dict.keys():
        if args_dict[key] is not None:
            args += " %s '%s'" % (key, args_dict[key])
    args += " --csv"

    links = []
    reader = csv.DictReader(StringIO(os.popen(args).read()))
    for row in reader:
        links.append((row['title'], row['ref']))
    return links

def files(dataset):
    args = "kaggle datasets list %s --csv" % dataset
    res = os.popen(args).read()
    return res

def download(dataset):
    args = "kaggle datasets download %s" % dataset
    os.system(args)

def metadata(dataset):
    args = "kaggle datasets metadata %s" % dataset
    os.system(args)

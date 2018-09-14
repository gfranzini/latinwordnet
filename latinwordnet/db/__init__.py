""" Contains the WordNet databases  """

import codecs
import os
import sqlite3
from os import listdir
from sqlite3 import OperationalError

from tqdm import tqdm


def connect(language, database):
    """ Connects to a database """

    try:
        if os.path.exists(f"../latinwordnet/latinwordnet/db/{language}/{language}_{database}.db"):
            cursor = sqlite3.connect(f"../latinwordnet/latinwordnet/db/{language}/{language}_{database}.db").cursor()
        else:
            raise OperationalError
    except OperationalError:
        cursor = None
    finally:
        return cursor

def compile(language, *tables):
    if not tables:
        tables = [filename.split('_')[0].replace('.sql', '') for filename in listdir(f"../latinwordnet/latinwordnet/db/{language}/") if filename.endswith('.sql')]

    for table in tables:
        f = codecs.open(f"../latinwordnet/latinwordnet/db/{language}/{language}_{table}.sql", encoding='utf-8')
        if f:
            db = sqlite3.connect(f"../latinwordnet/latinwordnet/db/{language}/{language}_{table}.db").cursor()

            if db:
                for sql in tqdm(f.readlines(), ncols=80, desc=f"{language}_{table}.sql"):
                    if sql.startswith('#') or sql == '\n':
                        continue
                    else:
                        db.executescript(sql)

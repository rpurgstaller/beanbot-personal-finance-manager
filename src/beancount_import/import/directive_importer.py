import itertools
import inspect
import logging
import sys
import textwrap

from beancount.core import data
from beancount.ingest.extract import HEADER, print_extracted_entries
from beancount.parser import printer
from beancount.ingest import similar
from beancount.ingest import identify
from beancount.ingest import cache
from beancount import loader


class DirectiveImporter():

    def extract():
        pass


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


def write(new_entries_list : list, output=sys.stdout):

    
    
    assert isinstance(new_entries_list, list)
    assert all(isinstance(new_entries, tuple) for new_entries in new_entries_list)
    assert all(isinstance(new_entries[0], str) for new_entries in new_entries_list)
    assert all(isinstance(new_entries[1], list) for new_entries in new_entries_list)

    # Print out the results.
    output.write(HEADER)
    for key, new_entries in new_entries_list:
        output.write(identify.SECTION.format(key))
        output.write('\n')
        print_extracted_entries(new_entries, output)
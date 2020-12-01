#!/usr/bin/env python3

import argparse
import os
#import shutil
import sys
import sqlite3
import re
#import textwrap

# Main routine
def main(args):
    # Open database file
    dbc = open_db(args.dbfile)

    # Loop over all published articles in the database
    for a in dbc.execute("select art_id, filename from articles where status=\"published\""):
        art_id = a[0]
        filename = a[1]
        filename_without_html = re.sub(".html$", "", filename)

        # Check, if art_id is contained in the command line arguments
        # (args.artids). If yes, the articles is to be converted and we
        # construct a proper redirection directive for Nikola.
        # If not, redirect to a "sorry page".
        if art_id in args.artids:
            print("(\"art/", filename, "\", \"/posts/", filename_without_html, "/index.html\"),", sep="")
        else:
            print("(\"art/", filename, "\", \"/pages/sorry/index.html\"),", sep="")

###############################################################################

#------------------------------------------------------------------------------
# Check if database file exists. If yes, open database and return
# database cursor
def open_db(dbfile):
    if not os.path.isfile(dbfile):
        print("Error: database file doesn't exist. Quitting!")
        sys.exit()
    db = sqlite3.connect(dbfile)
    dbc = db.cursor()
    return dbc

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dbfile", help="SQLite database file")
    parser.add_argument("artids", type=int, nargs="+", help="Article IDs")
    args = parser.parse_args()
    main(args)

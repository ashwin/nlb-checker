#!/usr/bin/env python

# BRN: ID used for items in NLB website

import argparse
import bs4
import requests
import string

def read_brn_file(books_path):

    brn_file = open(books_path)
    brn_list = []

    for line in brn_file:
        line = string.split(line, "#")[0] # Ignore everything after hash
        line = string.rstrip(line)        # Remove newline
        line = string.lstrip(line)        # Remove spaces in front
        if len(line) > 0:
            brn_list.append(line)

    return brn_list

def read_lib_file(libs_path):

    libs_file = open(libs_path)
    libs_list = []

    for line in libs_file:
        line = string.rstrip(line)        # Remove newline
        line = string.lstrip(line)        # Remove spaces in front
        if len(line) > 0:
            libs_list.append(line)

    return libs_list

def get_brn_url(brn):

    base_url = "http://catalogue.nlb.gov.sg/cgi-bin/spydus.exe/ENQ/EXPNOS/BIBENQ?BRN="
    brn_url = base_url + brn
    return brn_url

def make_brn_soup(brn):
    brn_url = get_brn_url(brn)
    response = requests.get(brn_url)
    soup = bs4.BeautifulSoup(response.text)
    return soup

def get_brn_title(soup):
    """
    Title of book is stored in table 2, row 0, column 2
    """

    table_list = soup.find_all("table")
    row = table_list[2].find("tr")

    col_list = row.find_all("td")
    col = col_list[2]

    title = col.get_text()
    return title

def check_brn_avail(brn, soup, lib_list, lib_brn_list):

    table = soup.select("table.clsTab1")
    row_list = table[0].find_all("tr")
    row_list = row_list[1:] # Skip header row at top

    for row in row_list:
        col_list = row.find_all("td")

        # Check if available
        status = col_list[3].get_text()
        if "Available" != status:
            continue

        # Match library
        lib = col_list[0].get_text()
        if lib not in lib_list:
            continue

        # Find matched library
        li = lib_list.index(lib)
        lib_brn_list[li].append(brn)


def check_brn_list(brn_list, lib_list):

    brn_title_dict = {}
    lib_brn_list = [[] for _ in lib_list]

    for brn in brn_list:
        soup = make_brn_soup(brn)

        # Uncomment to see HTML of page
        #print soup.prettify().encode("UTF-8")

        title = get_brn_title(soup)
        brn_title_dict[brn] = title

        check_brn_avail(brn, soup, lib_list, lib_brn_list)

    for li, lib in enumerate(lib_list):
        print
        print "Books available in", lib, ":"
        print
        for brn in lib_brn_list[li]:
            print "(", brn, ")", brn_title_dict[brn]
        print
        print "***"


def get_args():

    argParser = argparse.ArgumentParser()
    argParser.add_argument("--books-path", dest="books_path", type=str, default="", help="Path to file with list of BRN (book key numbers)")
    argParser.add_argument("--libs-path", dest="libs_path", type=str, default="", help="Path to file with list of library names")
    args = argParser.parse_args()

    # Default books path
    if not args.books_path:
        args.books_path = "./books.txt"

    # Default libs path
    if not args.libs_path:
        args.libs_path = "./libs.txt"

    return args

def main():

    args = get_args()
    brn_list = read_brn_file(args.books_path)
    lib_list = read_lib_file(args.libs_path)
    check_brn_list(brn_list, lib_list)

if "__main__" == __name__:
    main()

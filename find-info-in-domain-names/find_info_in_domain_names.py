#!/usr/bin/python3
import json
import urllib.request, urllib.parse
import csv
from io import StringIO
import codecs
import sys
import configparser
import codecs
from guess_language import guess_language
import bs4 as BeautifulSoup


def is_allowed(url, exclude_sites):
  for site in exclude_sites:
    if url.find(site) != -1:
      return False
  return True

def get_content(dom_elem):
    if dom_elem is not None:
        temp = dom_elem.get('content')
        if temp is None:
            temp = dom_elem.get_text()
            if temp != '':
                return temp
    return None

"""
    return 2 letters iso lang code or "UNKNOWN" if language not found
"""
def find_language(string):
    return guess_language(string)

def get_language(html_title, soup_document):
    language = find_language(html_title)
    if language == "UNKNOWN":
        meta_lang = soup_document.find('html').get('lang')
        return meta_lang[:2] if meta_lang is not None else ''
    else:
        return language

"""
    Try to find the author by looking in most common spots in the DOM
    Improvement: parse the hcard ?
"""
def find_author(soup_document):
    for args in [('a', {'rel': 'author'}), ('meta', {'name': 'author'}), {"itemprop": "author"}, ('meta', {'property': 'article:author'}), {"itemprop": "name"}, ('meta', {'name': 'article:author'})]:
        try:
            if isinstance(args, dict):
                author = get_content(soup_document.find(**args))
            else:
                author = get_content(soup_document.find(*args))
            if author is not None:
                return author
        except Exception as e:
            print('error find_author: %s' % e)
    return ''

"""
    Perform the search on google.
    I had a previous version using the api : http://ajax.googleapis.com/ajax/services/search/web?v=1.0 but it has been made unavailable in May 2016
    so I got to use the custom search engine but this come with heavy limitations in the free version (100queries/day)
"""
def google_search(target_url, search_term, config):
    result = {}
    excluded_sites = config['SEARCH']['exclude_sites']
    if ", " in excluded_sites:
        excluded_sites = excluded_sites.split(", ")
    api_key = config['SEARCH']['api_key']
    cse_id = config['SEARCH']['cse_id']
    if len(api_key) == 0 or len(cse_id) == 0:
        print('You need to set a valid google api key and a valid custom search engine id')
        return result
    search = format_search(target_url, search_term)
    query = urllib.parse.urlencode({'q': search})
    url = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&%s' % (api_key, cse_id, query)
    #print("searching ", search_term " on", url)
    search_response = urllib.request.urlopen(url)
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    if "items" in results and len(results['items']) > 0:
        result['mentioned'] = False
        hits = results['items']
        for h in hits:
            #check if the search term appears and is worth scrapping
            if is_allowed(h['link'], excluded_sites) and (h['link'].lower().find(search_term) != -1 or h['title'].lower().find(search_term) != -1 or h['snippet'].lower().find(search_term) != -1):
                print('Found: ', h['link'])
                result['mentioned'] = True
                result['link'] = h['link']
                result['title'] = h['title']
                return result
    return result

def format_search(domain, term):
  return 'inurl:'+domain+' "'+term+'"'

def parse_file(input_file_name, output_file_name, search_term, config):
    output_file = open(output_file_name, "w+", newline='', encoding='utf-8')
    writer = csv.writer(output_file, delimiter=';');
    with open(input_file_name, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for line in reader:
            new_array = list(line)
            if len(new_array) > 0:
                res = google_search(new_array[0], search_term, config)
                if "mentioned" in res and res["mentioned"]:
                    try:
                        new_array.append('Yes')
                        new_array.append(res['link'])
                        html = urllib.request.urlopen(res['link'], timeout=10).read()
                        soup = BeautifulSoup.BeautifulSoup(html)
                        author = find_author(soup)
                        if len(author) > 0:
                            new_array.append(author)
                            #print('author =', new_array[3].encode('ascii', 'ignore'))
                        language = get_language(res["title"], soup)
                        if len(language) > 0:
                            new_array.append(language)
                            #print('language =', new_array[4].encode('ascii', 'ignore'))
                    except Exception as e:
                        print('error', str(e).encode('ascii', 'ignore'))
                        pass
                else:
                    new_array.append('No')
            print('line to write', new_array)
            writer.writerow(new_array)
    output_file.close()

def main():
    try:
        config = configparser.ConfigParser()
        config.read(['config.cfg', 'config.local.cfg'])
    except Exception as e:
        print('error', e)
    if len(sys.argv) > 3:
        parse_file(sys.argv[1], sys.argv[2], sys.argv[3], config)
    else:
        print('Usage: python3 find_info_in_domain_names.py input_file.csv output_file.csv search_term')

main()

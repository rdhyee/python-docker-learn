#!/bin/env python

import re
from lxml.html import parse, fromstring
from lxml import etree
import requests
import urllib

from pandas import DataFrame

# bach_cantatas_url =  'http://en.wikipedia.org/wiki/List_of_cantatas_by_Johann_Sebastian_Bach'
bach_cantatas_url = "https://en.wikipedia.org/w/index.php?title=List_of_cantatas_by_Johann_Sebastian_Bach&oldid=307865758"

bwv_re = re.compile("BWV\s+(\d[^\s]*)")
bwv_anh_re = re.compile("BWV\s+(Anh\.\s+[^\s]*)")
title_re = re.compile("title=([^&]+)")

cantatas = []
page = requests.get(bach_cantatas_url).content.decode("UTF-8")
doc = fromstring(page)


for e in doc.xpath('//*[@id="mw-content-text"]/div[1]/ul[2]/li'):
    # check for a child <a>
    a = e.find("./a")

    # extract bwv
    matches_bwv = bwv_re.match(e.text)
    if matches_bwv:
        bwv = matches_bwv.group(1)
    else:
        matches_bwv_anh = bwv_anh_re.match(e.text)
        if matches_bwv_anh:
            bwv = matches_bwv_anh.group(1)
        else:
            bwv = ""

    if a is not None:
        href = a.attrib["href"]
        title = a.attrib["title"]

        # figure out whether the page exists and if so, what the wikipedia ID is.
        #  /wiki/Ich_habe_genug
        # /w/index.php?title=Ich_bin_ein_guter_Hirt&action=edit&redlink=1
        if href.find("&redlink=1") > -1:
            exist = False
            matches_title = title_re.search(href)
            if matches_title:
                wiki_id = matches_title.group(1)
            else:
                wiki_id = ""
        else:
            exist = True
            wiki_id = urllib.parse.unquote(re.sub("^/wiki/", "", href))

        cantatas.append(
            {
                "bwv": bwv,
                "title": title,
                "wiki_id": wiki_id,
                "exist": "True" if exist else "False",
                "text": e.text,
            }
        )
    else:
        cantatas.append(
            {"bwv": bwv, "title": "", "wiki_id": "", "exist": "False", "text": e.text}
        )

df = DataFrame(cantatas)
df.to_csv("cantatas.csv")
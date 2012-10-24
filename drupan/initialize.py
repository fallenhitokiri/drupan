# -*- coding: utf-8 -*-

"""everything that is needed to create a new drupan site"""

import os


DIRECTORIES = ['content', 'template', 'site', 'draft', 'content/images', 'template/css']

CONFIG = """name: "Local drupan Test"
url: "/"

plugins: ['fsreader', 'blank', 'sorted', 'tags', 'markdown', 'jinja', 'fswriter', 'imagecopy']

input: "content"
template: "template"
output: "site"

# url scheme - form: layout: url
# $foo means: relpace $foo with $foo from "meta"
# %foo means: replace %foo with attribute foo from ContentObject
layouts:
  post: ["$year/$month/$day/%slug/", "_post.html"]
  page: ["%slug/", "_page.html"]
  archive: ["archive/", "_archive.html"]
  index: ["", "_index.html"]
  feed: ["feed/", "_feed.xml"]
  tags: ["tag/$title/", "_tag.html"]


options:
"""

ARCHIVE = """{% extends "_base.html" %}

{% block title %}
 - Archive
{% endblock %}

{% block content %}
    <h6>Archive</h6>
    {% if site.tags > 0 %}
    <p><strong>Tags:</strong>
    {% for tag in site.tags %}
        <a href="{{ site.tags[tag] }}">{{ tag }}</a>{% if not loop.last %},{% endif %}
    {% endfor %}
    </p>
    {% endif %}

    <p class="box">If you do not want to miss new posts subscribe to my <a href="/feed/">RSS feed</a>.</p>

    <ul>
    {% for item in site.sorted %}
        <li><a href="{{ item.url }}">{{ item.meta['title'] }}</a> <span>written on: {{ item.meta['date'] }}</span></li>
    {% endfor %}
    </ul>
{% endblock %}
"""

BASE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <title>drupan - {% block title %}{% endblock %}</title>

        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <meta http-equiv="expires" content="0">
        <meta name="description" content="This is the default drupan template." />
        <meta name="keywords" content="super awesome, drupan" />
        <meta name="author" content="someone cool" />
        <meta name="robots" content="all" />

        <link href="{{ site.config['url'] }}css/screen.css" rel="stylesheet" type="text/css" />
        <link href="{{ site.config['url'] }}feed/" rel="alternate" type="application/rss+xml" title="RSS Feed" />
    </head>

    <body {% block bodyid %}id="default"{% endblock %}>

        <!--CONTAINER-->
        <div id="container">

            <!--CONTENT-->
            <div id="content">
                {% block content %} no content {% endblock %}
            </div>
            <!--END CONTENT-->

            <!--SIDEBAR-->
            <div id="sidebar">

                <!--LOGO-->
                <div id="logo">

                    <p><a href="/">Logo</a></p>

                </div>
                <!--END LOGO-->

                <!--RIBBON-->
                <div id="ribbon-wrapper">
                    <div id="ribbon-front">
                        <p>{{ site.config['name'] }}</p>
                    </div>

                    <div id="ribbon-edge-bottomleft"></div>
                    <div id="ribbon-edge-bottomright"></div>
                    <div id="ribbon-back-left"></div>
                    <div id="ribbon-back-right"></div>
                </div>
                <!--END RIBBON-->

                <!--MENU-->
                <div id="menu">
                    <ul>
                        {% for cur in site.content %}
                            {% if cur.menu == True or cur.meta['menu'] == True %}
                                <li><a href="{{ cur.url }}">{{ cur.meta['title'] }}</a></li>
                            {% endif %}
                        {% endfor %}
                    </ul>

                    <!--<p id="social">
                        social
                    </p>-->
                </div>
                <!--END MENU-->

            </div>
            <!--END SIDEBAR-->

            <div class="clearer"></div>

        </div>
        <!--END CONTAINER-->

    </body>

</html>
"""

FEED = """<?xml version="1.0" encoding="utf-8" ?>

<rss version="2.0">

    <channel>
        <title>{{ site.config['name'] }}</title>
        <link>{{ site.config['url'] }}</link>
        <description>what's hot</description>
        <language>en-en</language>
        <copyright>you!</copyright>
        <pubDate>{{obj.meta['date']}} GMT</pubDate>

        {% for item in site.sorted %}
            {% if loop.index <= 10 %}
            <item>
                <title>{{item.meta['title']}}</title>
                <link>{{item.meta['url']}}</link>
                <description>{{item.markup}}</description>
                <pubDate>{{item.meta['date']}}</pubDate>
            </item>
            {% endif %}
        {% endfor %}
    </channel>

</rss>
"""

INDEX = """{% extends "_base.html" %}

{% block bodyid %}id="index"{% endblock %}

{% block content %}
    <p class="box">Hi, this is an example drupan site.</p>

    {% for cur in site.sorted %}

        {% if loop.index <= 5 %}

            <h4><a href="{{ cur.url }}" alt="{{ cur.meta['title'] }}">{{ cur.meta['title']}}</a></h4>
            <p class="date">posted on: {{ cur.meta['date'] }}</p>
            {{ cur.markup|more }}
            <p class="more"><a href="{{ cur.url }}" alt="{{ cur.meta['title'] }}">continue reading</a></p>

        {% endif %}

    {% endfor %}
{% endblock %}
"""

PAGE = """{% extends "_base.html" %}

{% block title %}
 - {{ obj.meta['title'] }}
{% endblock %}

{% block content %}
    <h5>{{ obj.meta['title'] }}</h5>
    {{obj.markup}}
{% endblock %}
"""

POST = """{% extends "_base.html" %}

{% block title %}
 - {{ obj.meta['title'] }}
{% endblock %}

{% block content %}
    <h1>{{ obj.meta['title'] }}</h1>
    <p class="date">posted on {{ obj.meta['date'] }}</p>
    {{obj.markup}}
{% endblock %}
"""

TAG = """{% extends "_base.html" %}

{% block title %}
 - Tag: {{ obj.meta['title'] }}
{% endblock %}

{% block content %}
    <h6>Tag: {{ obj.meta['title'] }}</h6>
    <ul>
    {% for tag in obj.tags %}
        <li><a href="{{ tag.url }}">{{ tag.meta['title'] }}</a></li>
    {% endfor %}
    </ul>
{% endblock %}
"""

SCREEN = """@import "reset.css";


/* BASIC LAYOUT */
html, body {
    height:100%;
}

body {
    font-family:"Helvetica";
    font-size:14px;
    background:#FFFFFF;
}

.clearer { clear:both; }

#container {
    width:860px;
    margin:0 auto;
}

#content {
    width:600px;
    float:right;
    padding:20px 0px 0px 0px;
}

#sidebar {
    width:200px;
    height:100%;
    float:left;
    background:#222326;
    box-shadow:inset 0 0 10px #000000;
    moz-box-shadow:inset 0 0 10px #000000;
    webkit-box-shadow:inset 0 0 10px #000000;
    position:fixed;
}

/*
 * CONTENT
 */
#default p {
    margin:0px 0px 21px 0px;
    line-height:23px;
    letter-spacing:0.4px;
    word-spacing:1.2px;
}

#index p {
    margin:0px 0px 10px 0px;
    line-height:23px;
    letter-spacing:0.4px;
    word-spacing:1.2px;
}

#content h1, h2, h3, h4, h5, h6 {
    margin:0px 0px 10px 0px;
}

#content h1 {
    font-size:32px;
    margin:0px 0px 5px 0px;
    width:100%;
    border-color:#CCCCCC;
    border-width:0px 0px 2px 0px;
    border-style:solid;
}

#content h2 {
    font-size:24px;
}

#content h3 {
    font-size:18px;
}

#content em {
    font-style:italic;
}

#content strong {
    font-weight:bold;
}

#content code {
    color:#262626;
}

/*INDEX*/
#content h4 {
    font-size:20px;
    margin:0px 0px 5px 0px;
    width:100%;
    border-color:#CCCCCC;
    border-width:0px 0px 1px 0px;
    border-style:solid;
}

#content h4 a {
    text-decoration:none;
    color:#262626;
}

/*PAGE*/
#content h5 {
    font-size:32px;
    margin:0px 0px 15px 0px;
    width:100%;
    border-color:#cccccc;
    border-width:0px 0px 2px 0px;
    border-style:solid;
}

/*ARCHIVE*/
#content h6 {
    font-size:32px;
    margin:0px 0px 15px 0px;
    width:100%;
    border-color:#cccccc;
    border-width:0px 0px 2px 0px;
    border-style:solid;
}

#content a {
    color:#AD2731;
}

#content a:hover {
    text-decoration:none;
}

#content .date {
    color:#AD2731;
    font-size:12px;
    margin:-5px 0px 10px 0px;
}

#index .more {
    margin:0px 0px 35px 0px;
}

#content .box {
    box-shadow:0 0 3px #222326;
    moz-box-shadow:0 0 3px #222326;
    webkit-box-shadow:0 0 3px #222326;
    margin:0px 0px 35px 0px;
    padding:5px 10px 5px 10px;
    color:#FFFFFF;
    background-image: linear-gradient(bottom, #222326 0%, #4D4D4F 100%);
    background-image: -o-linear-gradient(bottom, #222326 0%, #4D4D4F 100%);
    background-image: -moz-linear-gradient(bottom, #222326 0%, #4D4D4F 100%);
    background-image: -webkit-linear-gradient(bottom, #222326 0%, #4D4D4F 100%);
    background-image: -ms-linear-gradient(bottom, #222326 0%, #4D4D4F 100%);
    background-image: -webkit-gradient(linear, left bottom, left top, color-stop(0, #222326), color-stop(1, #4D4D4F));
}

#content .box a {
    color:#A4A4A4;
}

#content .box a:hover {
    color:#AD2731;
}

#content ul {
    list-style-type:disc;
    padding:0px 0px 0px 50px;
    margin:0px 0px 21px 0px;
    line-height:23px;
    letter-spacing:0.4px;
    word-spacing:1.2px;
}

#content ol {
    list-style-type:decimal;
    padding:0 0 0 50px;
    margin:0 0 21px 0;
    line-height:23px;
    letter-spacing:0.4px;
    word-spacing:1.2px;
}

#content em {
    font-weight:bold;
}

#content li {
    margin:0px 0px 2px 0px;
}

#content ul span {
    display:block;
    margin:0px 0px 8px 0px;
}

#content #twitter {
    width:100%;
    text-align:right;
}

/*
 * SIDEBAR
 */
#sidebar #logo p {
    width:200px;
    text-align:center;
    color:#FFFFFF;
    padding:10px 0px 0px 0px;
    margin:0px 0px 0px 0px;
}

/* RIBBON */
#ribbon-wrapper {
    position: relative;
    margin:10px 0px 25px 0px;
}

#ribbon-front {
    background-color: #AD2731;    height: 40px;
    width: 214px;
    position: relative;
    left:-7px;
    z-index: 2;
}

#ribbon-front, #ribbon-back-left, #ribbon-back-righ {
    -moz-box-shadow: 0px 0px 4px rgba(0,0,0,0.55);
    -khtml-box-shadow: 0px 0px 4px rgba(0,0,0,0.55);
    -webkit-box-shadow: 0px 0px 4px rgba(0,0,0,0.55);
    -o-box-shadow: 0px 0px 4px rgba(0,0,0,0.55);
}

#ribbon-edge-topleft, #ribbon-edge-topright, #ribbon-edge-bottomleft, #ribbon-edge-bottomright {
    position: absolute;
    z-index: 1;
    border-style:solid;
    height:0px;
    width:0px;
}

#ribbon-edge-bottomleft, #ribbon-edge-bottomright {
    top: 40px;
}

#ribbon-edge-topleft, #ribbon-edge-bottomleft {
    left: -7px;
    border-color: transparent #701A20 transparent transparent;
}

#ribbon-edge-topleft {
    top: 0px;
    border-width: 0px 7px 0 0;
}

#ribbon-edge-bottomleft {
    border-width: 0 7px 7px 0;
}

#ribbon-edge-topright, #ribbon-edge-bottomright {
    left: 200px;
    border-color: transparent transparent transparent #701A20;
}

#ribbon-edge-topright {
    top: 0px;
    border-width: 0px 0 0 7px;
}

#ribbon-edge-bottomright {
    border-width: 0 0 7px 7px;
}

#ribbon-back-left {
    position: absolute;
    top: 7px;
    left: 0px;
    width: 0px;
    height: 40px;
    z-index: 0;
}

#ribbon-back-right {
    position: absolute;
    top: 7px;
    right: 0px;
    width: 0px;
    height: 40px;
    z-index: 0;
}

#ribbon-wrapper p {
    color:#FFFFFF;
    font-weight:bold;
    font-size:16px;
    letter-spacing:1.2px;
    word-spacing:1.2px;
    text-align:center;
    padding:8px 0px 0px 0px;
}

/* MENU */
#sidebar #menu {
    width:200px;
    font-size:15px;
    margin:0px 0px 50px 0px;
}

#sidebar ul {
    width:200px;
}

#sidebar ul li {
    width:200px;
}

#sidebar ul li a {
    width:180px;
    display:block;
    padding:10px 0px 10px 20px;
    color:#FFFFFF;
    text-decoration:none;
}

#sidebar ul li a:hover {
    background:#151515;
}

#sidebar #social {
    text-align:center;
    margin:25px 0px 0px 0px
}
"""

RESET = """html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 100%;
    font: inherit;
    vertical-align: baseline;
}
article, aside, details, figcaption, figure,
footer, header, hgroup, menu, nav, section {
    display: block;
}
body {
    line-height: 1;
}
ol, ul {
    list-style: none;
}
blockquote, q {
    quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
    content: '';
    content: none;
}
table {
    border-collapse: collapse;
    border-spacing: 0;
}
"""

DRAFT_PAGE = """title: title
date: yyyy-mm-dd hh:mm:ss
layout: page
menu: True
---
Content
"""

DRAFT_POST = """title: title
date: yyyy-mm-dd hh:mm:ss
layout: post
tags: [tag1, tag2]
---
Teaser
<!--MORE-->
Content
"""

TEST_PAGE = """title: I am a page
date: 2012-10-21
layout: page
menu: True
---
Awesome content goes here!
"""

TEST_POST = """title: I am a post
date: 2012-10-21
layout: post
tags: ["tag1", "tag2"]
---
Intro
<!--MORE-->
For a great post.
"""

FILES = [
    ['config.yaml', CONFIG],
    ['draft/_post.md', DRAFT_POST],
    ['draft/_page.md', DRAFT_PAGE],
    ['content/post.md', TEST_POST],
    ['content/page.md', TEST_PAGE],
    ['template/_archive.html', ARCHIVE],
    ['template/_base.html', BASE],
    ['template/_feed.xml', FEED],
    ['template/_index.html', INDEX],
    ['template/_page.html', PAGE],
    ['template/_post.html', POST],
    ['template/_tag.html', TAG],
    ['template/css/screen.css', SCREEN],
    ['template/css/reset.css', RESET],
]


def directories(path):
    """create directories in path"""
    os.makedirs(path)

    for directory in DIRECTORIES:
        print "creating %s" % directory
        new_dir = path + directory
        os.makedirs(new_dir)


def files(path):
    """create files in path"""
    for base_file in FILES:
        print "writing %s" % base_file[0]
        name = path + base_file[0]
        with open(name, 'w') as output:
            output.write(base_file[1])


def bootstrap(path):
    """setup a new site"""
    print "creating new site at %s" % path

    if not path[-1:] is os.sep:
        path = path + os.sep

    directories(path)
    files(path)

    print "your new site is created. Have fun :)"

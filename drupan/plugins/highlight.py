# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
# TODO: Python 3 renames this to html.parser - transition?

from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter


class CodeParser(HTMLParser):
    """Handler based on HTMLParser for code"""
    def __init__(self):
        HTMLParser.__init__(self)
        self.found_pre = False
        self.code = []

    def handle_starttag(self, tag, attrs):
        """find beginning of code block"""
        if tag == 'pre':
            self.found_pre = True
    
    def handle_endtag(self, tag):
        """find end of code block"""
        if tag == 'pre' and self.found_pre:
            self.found_pre = False
    
    def handle_data(self, data):
        """add code to array"""
        if self.found_pre == True:
            self.code.append(data)


class Feature(object):
    """Highlight code blocks using Pygments"""
    def __init__(self, site):
        self.site = site
        self.options = site.config.options_for_key('highlight')
        self.linenos = True
        self.css = "highlight"
        
        if self.options:
            if linenos in self.options:
                self.linenos = self.options['linenos']
            
            if css in self.options:
                self.css = self.options['css']

    def run(self):
        """run the plugin"""
        for cobj in self.site.content:
            if cobj.markup is not None:
                parser = CodeParser()
                parser.feed(cobj.markup)
                
                for code in parser.code:
                    lexer = guess_lexer(code)
                    formatter = HtmlFormatter(linenos=self.linenos, cssclass=self.css)
                    highlighted = highlight(code, lexer, formatter)
                    cobj.markup = cobj.markup.replace(code, highlighted)

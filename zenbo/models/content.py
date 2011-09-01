# -*- coding: utf-8 -*-

import yaml

from io import read


class Content(object):
    """Content object"""
    def fromFile(self, path, name, site):
        """
        parse content from files
        <- path: path to file
           name: filename
           site: site object
        """
        raw = read(path, name)

        (header, seperator, content) = raw.partition('---')
        
        meta = yaml.load(header)
        
        self.title   = meta['title']
        self.date    = meta['date']
        self.layout  = meta['layout']
        self.userdef = meta['userdef']
        self.content = content

        self._friendly()
        self._highlight(site)
        self._url(site)


    def fromDict(self, dic, site):
        """
        parse dictionary
        <- dic: content from generator
           site: site object
        """
        for key in dic:
            setattr(self, key, dic[key])

        self._friendly()
        self._url(site)


    def _friendly(self):
        """
        generate url friendly title
        """
        t = self.title
        t = t.replace(' ', '_')
        t = t.replace('!', '_')
        t = t.replace('?', '_')
        t = t.replace('&', '_')
        t = t.replace(';', '_')
        t = t.replace(':', '_')
        t = t.replace('#', '_')
        t = t.replace('~', '_')
        t = t.replace('*', '_')
        t = t.replace('¬¥', '_')
        t = t.replace('`', '_')
        t = t.replace('\'', '_')
        t = t.replace("\"", "_")
        t = t.replace('¬ß', '_')
        t = t.replace('$', '_')
        t = t.replace('@', '_')
        t = t.replace('‚Ç¨', '_')
        t = t.replace('%', '_')
        t = t.replace('/', '_')
        t = t.replace('(', '_')
        t = t.replace(')', '_')
        t = t.replace('[', '_')
        t = t.replace(']', '_')
        t = t.replace('{', '_')
        t = t.replace('}', '_')
        t = t.replace('=', '_')
        t = t.replace('\\', '_')
        t = t.replace('^', '_')
        t = t.replace('¬∞', '_')
        t = t.replace('<', '_')
        t = t.replace('>', '_')
        t = t.replace('|', '_')
        t = t.replace('√§', '_')
        t = t.replace('√∂', '_')
        t = t.replace('√º', '_')
        
        self.friendly = t.lower()


    def _highlight(self, site):
        """
        highlight sourcecode
        <- site: site object
        """
        import re
        from pygments.lexers import guess_lexer
        from pygments.formatters import HtmlFormatter
        from pygments import highlight

        code = re.compile(site.highlight, re.DOTALL).findall(self.content)

        if code:
            for c in code:
                lexer = guess_lexer(c)
                formatter = HtmlFormatter(linenos=True)
                hl = highlight(c, lexer, formatter)

                self.content = self.content.replace(c, hl)


    def _url(self, site):
        """
        generate url
        <- site: site object
        """
        var = {
                'year'  : str(self.date.year),
                'month' : str(self.date.month),
                'day'   : str(self.date.day),
                'title' : self.friendly
                }

        layout = site.urls[self.layout]
        
        for key in var:
            layout = layout.replace("$" + key, var[key])

        self.url = "%s%s" % (site.url, layout)


    def __unicode__(self):
        """
        return title and date
        """
        return "[%s] %s" % (self.date, self.title)

    
    def __str__(self):
        """
        return title and date
        """
        return unicode(self).encode('utf-8')
    

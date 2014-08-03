# Designing a site
Drupan uses the [Jinja2 template engine](http://jinja.pocoo.org) which is
powerful and allows you to realize nearly everything you can imagine. To
further support this drupan provides additional filters you can use.

##### more
With the `more` filter you can split the content that is passed to the filter
and get either the part before the separator or the whole content if the
separator does not exist.

The default separator is `<!--MORE-->`

###### Usage
In your template where you want your content you do `{{ entity.content|more }}`.

##### filter
If you used the Django ORM once you know what `filter` is doing. You can
filter your entities based on a key and value and get a list of entities
returned.

Filter will use `Site.search` so it looks up keys in the entities meta
dictionary and also checks the attributes.

###### Usage
Let us output a list of all entities where the key `foo` has the value `bar`

     {% for entity in site|filter("foo", "bar") %}
     - {{ entity.title }}
     {% endfor %}

##### get
Get works like filter but returns execatly one result or raises an exception.

###### Usage
If you want to output the URL for your about page you can do

     {% with entity = site|get("title", "About") %}
       {{ entity.url }}
     {% endwith %}

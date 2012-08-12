# Detailed informations about Zenbo
With this guide I will give you a short introduction how you can start blogging with Zenbo.

The standard setup involves shell access to your webserver and some basic knowledge of Git.

## Just run it
Since I do not believe that you need a long explanation or some newbie friendly guide, I suggest you copy doc/example to a location of your choice and run ```python zenbo.py /path/to/example```.

Take a look at the configuration file and the templates and you should understand what you need to create your site. If you want more informations read on or dive into the real documentation.

## Setup
We will setup Zenbo to deploy awesumsite.tld. We start on our local machine. Before you start typing I suggest you take a look at doc/example. There you will find an existing directory structure and a configuration file.

	local $ mkdir awesumsite
	local $ touch awesumsite/config.yaml
	local $ mkdir awesumsite/content
	local $ mkdir awesumsite/content/images
	local $ mkdir awesumsite/htdocs
	local $ mkdir awesumsite/template
	local $ cd awesumsite
	local $ git init
	local $ git add .
	local $ git commit -a -m "initial commit"

Now we connect to our server. We create a bare repository to push our site to the server and a post-receive hook to automatically checkout out to the web server directory. There is also a possibility to work with one repository and use ```receive.denyCurrentBranc``` but rumors are that this is not the best idea.

	server $ mkdir awesumsite
	server $ cd awesumsite
	server $ git init --bare
	server $ mkdir /path/to/server/root/awesumsite.tld
	server $ cat > hooks/post-receive
	#!/bin/sh
	GIT_WORK_TREE=/path/to/server/root/awesumsite.tld git checkout -f
	chmod +x hooks/post-receive

## Configuration file
We need to add some configuration options to our ```config.yaml```. As the name suggests it is written in YAML.

See ```doc/example/config.yaml```

With the example configuration you get a blog with pages.

## Defaults
You can customize Zenbo to the point where you have nearly no default code in it - and it will still work if you stick to the plugin guidelines. The example configuration assumes you want to store your files locally and push them to you server with git. You get a blog and pages for an 'about' page or something else.

Every page is represented as a so called ```ContentObject```.

### Input
Content is loaded using the ```filesystem``` plugin. Make sure to change the file extension if you want to use something else than markdown or if you are not happy with files ending on ```.md```.

### Generators
You have two generators.

#### blank
Blank generates empty ```ContentObjects```. This way you can add an index page, archives or RSS feeds to your page. They are basically just there so Zenbo knows to load the template files and render them. You can access all content in them and freely generate whatever is possible using [Jinja2][jinja].

If the second value is set to "True", then ```ContentObject``` will be added to your menu.

#### sorted
Sorted adds a new array to your ```site``` object. This array holds a reference to all ContentObjects with a layout you specify in your configuration file and sorts them with the newest object as first item.

With this generator you do not have to sort stuff in your template to generate an archive.

### Converters
```markdown``` does exactly one thing. Iterate through all ContentObjects, check if ```content``` is not None, convert it using [markdown2][markdown] and safe it to in ```markup```.

### Rendering
We use Jinja as template engine. For more informations you should read the excellent documentation they provide or take a look at the existing template. It is pretty easy to understand.

### Finalizers
There is only one. ```imagecopy``` parses all ```ContentObjects```, searches for images and copies them in the corresponding directory.

### Output
We write our rendered site to the filesystem.

### Deploy
Git. Running with ```subprocess```.

### Layouts
Zenbo uses this to map layouts to template files and how to construct URLs. Easily customizable. If you do not want the day in your "post" URLs just remove ```$day/```.

## Further reading
If you want to learn more about the different plugins see the plugin documentation in ```doc/plugins```. If you want to write your own I suggest you start looking at one of the existing plugins and read ```doc/developer/plugins```.

[jinja]: http://jinja.pocoo.org
[markdown]: https://github.com/trentm/python-markdown2
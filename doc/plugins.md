# Plugins
If you understand what each plugin is doing you have a
pretty good idea what happens while generating your site.
Remember that plugins are executed in the order in which
they are listed on the ```plugins``` array in your 
```config.yaml```.

If there are options described here they go to the
```options:``` part of your ```config.yaml```. They are all
optional. Necessary configuration options are described in
```doc/configuration.md```.

You *always* name the configuration key after the plugin.

## fsreader
Reads your content from your file system and creates
```ContentObjects```. The header will be stored in ```meta```
and your content in ```content```.

The object will be added to your ```Site``` object in the
```content``` array.

### Configuration
If you want to use another file extension than ```.md``` specify
it in ```options```.

```fsreader: '.txt'```

## fswriter
Writes everything in the ```content``` array of your ```Site```
object to the file system. It will use the ```path``` of the
current object, split it, create the folders and write and
```index.html```.

Before it starts writing it will wipe your output folder and
copy everything in your template folder to the new output folder
beside files starting with an underscore.

## blank
Creates empty ```ContentObjects```. Thanks to the templating
engine you can do a lot of stuff with those, like creating
RSS and Atom feeds or archive pages.

### Configuration
In the default configuration you get three blank objects. One 
acting as index for your site, an archive and a rss feed. If you
need additional objects you have to specify those three plus the 
ones you need.

    blank:
        index: ["Index", False]
        archive: ["Archive", True]
        feed: ["RSS Feed", False]
        newobject: ["Doing Stuff", True]

The format is easy. ```newobject``` is the name for your layout, 
the first string in the array is the name of your object and you 
can specify if you want it to appear in the menu (True) or not 
(False).

Remember to add a layout.

## gitsub
Deploy a site using git. See ```doc/Deployment.md```.

## highlight
Your ```ContentObjects``` have a variable ```markup``` which
stores the final HTML of your content. highlight search for
```<pre><code>``` tags, extracts the code and uses pygments to
highlight it.

### Configuration
You can change if line numbers are display and the class of your CSS.

    highlight:
        linenos: False
        css: "codeblock"

Default: ```linenos: True```, ```css:  "highlight"```

## imagecopy
Search in your ```ContentObjects``` for images. It assumes that
everything in an img tag which starts with a slash is a link to
an image.

After finding images it extracts the filename and copy the file
in the corresponding directory.

### Configuration
Add it *after* fswriter. The only option you can add is the path
to your images if they are not stored in ```content/images```.

## jinja
Runs jinja on all ```ContentObjects``` with content

### Filters
There are filters in ```jinja_filters``` you can use.

#### more
If you only want an excerpt of your content on some pages add
```<!--MORE-->```. If you add the filter you will only get
everything above the tag.

#### twitter
To use Twitters site preview you can add 200 characters. This
filter just returns the first 200 characters.

## markdown
Uses markdown to convert your input to HTML.

## sorted
Adds a ```sorted``` array to your ```Site``` object. All objects
in this array will be sorted using ```.meta['date']``` as key
starting with the most recent object.

### Configuration
Add an array to your options and include all *layouts* that should
be added to the array.

    sorted: ['post', 'note', 'link', 'image']

Default: ```post```

## tags
Look for a ```tags``` array in ```ContentObject.meta``` and create
content objects for every tag. Give them a URL and add all
```ContentObjects``` with the tag to it.

### Configuration
Remember to add a layout.

# Example
An example how ```options``` could look

    options:
      sorting: ['post', 'note', 'link', 'image']
      blank:
        index: ["Index", False]
        archive: ["Archive", True]
        feed: ["RSS Feed", False]
        newobject: ["Doing Stuff", True]

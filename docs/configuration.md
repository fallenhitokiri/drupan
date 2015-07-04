# Configuration
For plugin specific configuration options please read the plugin documentation.
A standard configuration can look like this

    reader: "filesystem"
    writer: "filesystem"
    plugins: ["markdown", "blank", "tags"]
    deployment: "s3cf"
    url_scheme:
        index: ""
        archive: "/archive/"
        tag: "/tag/%slug/"
        post: "/%year/%month/%slug/"
        page: "/%slug/"
        feed: "/feed/"
        error: "/error/"
    options:
        reader:
            content: "/Users/timo/tmp/screamingatmyscreen/content"
            extension: "md"
            template: "/Users/timo/tmp/screamingatmyscreen/template"
        writer:
            directory: "/Users/timo/tmp/screamingatmyscreen/site"
        markdown:
            extras: ["tables", "code-highlight"]
        blank:
            generate:
                index: "index"
                archive: "archive"
                feed: "feed"
                error: "error"
        s3cf:
            bucket: "screamingatmyscreen.com-fail"
            aws_access_key: "foo"
            aws_secret_key: "bar
            cloudfront_id: "asdf"
            redirects:
                "/feed.xml": "/feed/"

The only optional option is deployment. If you configure a plugin, reader,
writer or deployment option you have to add *all* options it expects to the
options section.

## url_scheme
Here you specify the URL scheme for a layout - format: layout: URL

In your URLs you can set a variable name prefixed by '%'. This will do the
following lookup on generation time

  - part of the created timestamp
  - in the meta dictionary
  - as attribute of an entity instance

This means `%year` becomes the year of the created   timestamp, `%title`
would be the title in the meta dictionary and `%foo` an attribute that was
added by a plugin.

# Readers
A reader is the way drupan gets the raw information and content to generate
a site.

Options go in the ```reader``` section - this is necessary to prevent name
conflicts with the filesystem writer.

## filesystem
The filesystem reader reads the content from files in a directory. 

###### Options

  - ```content``` path to the content directory. Relative to the current
  directory or the full path
  - ```extension``` file extension the content files have. All files with
  another extension will be ignored
  - ```template``` directory with the template

# Writers
A writers' job is to somehow save the generated site and take care of all
required tasks to make the site fully workable, like copying images to the
posts.

Options go in the ```writer``` section - this is necessary to prevent name
conflicts with the filesystem writer.

## filesystem
The filesystem writer writes the generated site to a directory. Several
things happen when the writer is running

  - the old site directory is deleted
  - the contents of the template directory are copied to the new site
  directory (files starting with an ```_``` are ignored)
  - the generated site is written
  - images from content/images are copied in the directory where the
  file referencing them is stored

###### Options

  - ```directory``` directory to write the generated site to

# Plugins
A plugin is running after the content is read and before the template engine
is running. You can use plugins to convert a markup language to HTML, highlight
code blocks or generate additional entities like tag pages.

## blank
Blank generates blank entities for a specific URL. They can be used to create
index or archive pages.

###### Options

  - ```generate``` entities to generate - format: title: layout

## markdown
Converts markdown in the content part of the input material to HTML. For a list
of supported extras please see the
[python-markdown2 wiki](https://github.com/trentm/python-markdown2/wiki/Extras)

###### Options

  - ```extras``` a list fo extras to use

## tags
A plugin to generate tags based on a tag list in the header of entity files.
This plugins has no options.

# Deployment
Deployment plugins are in charge of publishing your generated site the way
you prefer and your target server supports. If you are planning to deploy to
AWS S3 and CloudFront using s3cf is the recommended way to do so.

## s3cf
This plugins uses the [boto library](https://github.com/boto/boto) to deploy
your site to S3 and it will also invalidate all changed files on CloudFront. If
you are not planning to use CloudFront just do not add a distribution ID.

###### Options

  - ```bucket``` name of the S3 bucket to upload to
  - ```aws_access_key``` AWS access key with permissions for your S3 bucket and
  CF distribution
  - ```aws_access_key``` AWS secret key with permissions for your S3 bucket and 
  CF distribution
  - ```cloudfront_id``` ID of your CloudFront distribution (optional)
  - ```redirects``` redirects to create - format: old url: new url (uses S3 
  redirect feature)

## gitsub
This plugins runs git as subcommand and pushes your site to the remote called
```server```. It runs the following commands

  - ```git add .```
  - ```git commit -a -m "$foo"``` where $foo is the current date and time
  - ```git push -u server master```

No path is assumed as default so you can either push the whole drupan directory
or just the generated site directory. It is up to you to decide what you prefer.

###### Options

  - ```path``` path to run the git commands in

## s3sub
This plugin runs the AWS cli tools as subcommand and uploads your site to
S3. You have to make sure the AWS cli tools are in your path and that you
have a profile with access keys that is allowed to read and write to the
target bucket.

After the initial upload only changed files will be uploaded. To make this
possible MD5 checksums of all files will be generated.

###### Options

  - ```bucket``` name of the bucket to upload to
  - ```profile``` profile in your AWS cli configuration file to use
  - ```md5path``` Path where to store the MD5 checksum
  - ```site_url``` URL of your site
  - ```skip_upload``` a list with files - if only files that are listed here
  changed when running drupan the site will not be uploaded
  - ```redirects``` redirects to create - format: old url: new url

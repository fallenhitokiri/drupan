#Directory Structure
First you have to create 3 directories to hold the following file
 * content
 * your generated site
 * template to be used
After you have those 3 copy the default_config.yaml to a directory of your choice, rename it /config.yaml/ and edit it.
With the comments it should explain itself.

I suggest you use one directory for all this stuff so you get a structure that looks like the following:
 site_name/
 - content/
 - site/
 - template/
 - config.yaml

#Deployment
/add deployment section after the whole documentation is finished/

#Blogging
Adding a new post to you blog is easy. Create a file in /content/ named "blogpost".markdown (default configuration), add the yaml header in default_post.markdown (or just copy this file and rename it), write your content and run
  zenbo /path/to/your/site
If you want to create a page do the same thing but use the yaml header from default_page.markdown

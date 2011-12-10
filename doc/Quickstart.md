# Quickstart

With this guide I will give you a short introduction how you can start blogging with Zenbo.

I will use git and lighttpd but feel free to use whatever you want. Check out the documentation of the other deployment modules if you prefer rsync or something else.

## Setup

You need 3 directories and one configuration file.

 * one directory for your content
 * one for the generated site
 * and one for your template

I suggest you copy the default.yaml to your directory and rename it to config.yaml. Thanks to the comments you should be able to figure it out by yourself.

### Git

After everything is created and configured run

  git init

and add a remote location named server. I suggest you use git over ssh with pub/priv key authentification. This way you can just run Zenbo and everything happens without bothering you.

### Server

On your server you need git and a webserver. Pick a directory, run

  git init

and point your webservers document root to the site directory in your git directory. Now run

  chmod +x .git/hooks/post-received

and edit it using your favorit edit. There should already be a shebang at the beginning. Add

  GIT_WORKING_DIRECOTY=$foo git checkout -f

Replace $foo with your git directory. Now git will automatically run checkout -f whenever you push your site to the repository. This way it will automatically be up to date.

## Content

To create content for your new site just create a file in your content directory with the extension specified in your config and add one of the following headers.

### Blog Post

header

### Page

Currently you can only write your content using markdown.

## Template

You can use Jinja to create your template. The variable holding all the informations is named obj for the current site content and site with everything you can imagine. If you want some ideas how to create your menu or how to structure your template take a look at [http://www.github.com/fallenhitokiri/Zenbo-test|Zenbos Test repository].


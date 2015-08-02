# drupan - flexible static site generator
Drupan is a flexible static site generator helping you to create blogs, single
page applications or traditional websites. While being opinionated the plugin
system allows you to extend it with any functionality you desire.

## Quickstart
Install drupan, clone this [example site](https://github.com/fallenhitokiri/drupan-template-blog)
repository and run `drupan config.yaml --serve` in the cloned directory.

## Noteworthy Features
- deployment your site using git or directly to AWS S3 and AWS CloudFront
- fast page generation
- Jinja2 with custom template tags and filters
- powerful plugin system

## Usage
You can install drupan via pip. To generate your site you just run
`drupan ~path/to/config.yaml`.

Supported command line switches

- `nodeploy` do not deploy the generated site
- `serve` runs a development server on port 9000
- `deploy` deploy your output directory without generation

### Readers

- `filesystem` reads content from files with a YAML header

### Writers

- `filesystem` writes the generated site to a directory

### Deployment

- `s3cf` deploy your site to AWS S3 and optionally invalidate changed files on
AWS CloudFront using boto
- `gitsub` commits the changes to git and pushes to a remote server
- `s3sub` uploads your site to AWS S3 using the AWS CLI package 

### Plugins

- `blank` generates empty Entity instances with a given layout. This can be
used to generate index or archive pages
- `markdown` converts entity content from markdown to HTML
- `tags` support for tags which are added to a posts meta information

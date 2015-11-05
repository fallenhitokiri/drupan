# Migrating from 2.0 and 2.1 to 2.2
The primary goal of drupan 2.2 is to decouple the different parts of the system.
To make this happen some configuration options were removed or move to a
different step. As always, this is fully compatible with a working 2.x site, but
you will see warnings to change your configuration file format to prepare you
for future releases which break backwards compatibility.

## reader: filesystem
A reader plugin is now in charge to read *everything*, this includes the
template files and assets. To make this possible two configuration options
changed.

  - `directory` renamed to `content`
  - new option: `template` replaces `jinja/template` (path to your template
  directory)

## s3cf
It is not required anymore to write md5 files to a file
to keep track of changed files between two uploads. This allows drupan to work
without writing the files locally, so the fsreader and s3cf would be sufficient
to deploy a site to S3 and CloudFront (no fswrite is required)

For this reason the following configuration options were removed

  - `md5path`
  - `skip_upload`
  - `site_url`
 
Drupan 2.2 also introduces optional settings. The following settings became 
optional - if you do not want to use the feature just remove the key.

  - `redirects`
  - `cloudfront_id`

Additionally you can now define redirects as a top level configuration option.
This is just a logical move of the key since the redirects should not be tied
to a certain deployment option.

## Plugin: Blank
The configuration option `generate` now expects a list instead of a dictionary.
This means the title and layout of the generated entities will be the same. For
compatibility reasons the old behavior is still supported.

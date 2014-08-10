# Migration from drupan version 1 to version 2
This is a short guide how to migrate a site from drupan 1 to drupan 2.
For more information why incompatibilities were acceptable - beside the
fact that we are talking about a major release - please read [this blog
post](http://screamingatmyscreen.com/2014/7/state-of-drupan-2-rawr/).

### Configuration
The changes are mostly in the configuration file. Most importantly: 
drupan expectes the configuration file, not the directory as argument.
This helps if you manage multiple sites form the same system.

The format of the file completly changed. Please read `configuration.md`
in the `docs` directory for more information.

### Templating
Templating became a lot more powerful so it can happen that some clever
tricks to access some entities, configuration options or specifc sites
do not work anymore. But the good part is that templating became more
powerful, so fixing it should be quite easy.

Some improvements are that you can now access the configuration directly
in the template and that you have more filters and helpers attached to
the site instance. See the `templates.md` file in the `docs` directory
for more information.

##### Important changes

  - templates always have the extension `html`, no matter what they contain
  - tags: `obj.tags` became `obj.entities`
  - there are no special attributes like `site.sorted` anymore, they were
  replaced by template tags and filters. See `templates.md`

### Git deployment
You can now specify the path for git which means you can only push have
your site directory under version control and pushed to your server.

# Developer guide
If you want to contribute to drupan this is a good place to start.
Please read the following introduction carefully since I will not
consider any submissions that do not conform those guidelines.

## Directories
If you need more than one file for a plugin feel free to create a 
directory named "$pluginname{_potentialAdditions}".

If your plugin provides an interface to additional plugins a 
directory for those plugins *is* necessary. If you add a new 
templating engine which supports filter e.x. create a directory 
"$plugin_filters".

There are no directories beside the one for plugins. If you want 
to add something to the core functionality stay out of the plugin 
directory and add it to the drupan package.

## Tests
No matter if you love or hate tests include one. There is an 
example site or you can just create objects which only contain 
the data you need.

I prefer to write my tests as subclass of ```unittest.Testcase```.
Nose is fine, too. Please do no use a framework which is not 
compatible to them.

## License
Your work has to be compatible with the BSD 2 clause license.

## Submitting patches and plugins
Send me a pull request on [GitHub][github].

[github]: https://github.com/fallenhitokiri/drupan
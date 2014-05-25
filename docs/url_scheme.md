# URL schemes
In your URLs you can set a variable name refixed by '%'. This will do the
following lookup on generation time

- part of the created timestamp
- in the meta dictionary
- as attribute of an Entity instance

This means `%year` becomes the year of the created timestamp, `%title`
would be the title in the meta dictionary and `%foo` an attribute that was
added by a plugin.

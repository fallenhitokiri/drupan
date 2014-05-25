# Configuration
For plugin specific configuraiton options please read the plugin documentation.
A standard configuration can look like this

    reader: "filesystem"
    writer: "filesystem"
    plugins: ["markdown", "blank", "tags"]
    deployment: "s3sub"
    url_scheme:
        index: ""
        post: "/%slug/"
    options:
        reader:
            directory: "/Users/tizi/tmp/screamingatmyscreen/content"
            extension: "md"
        writer:
            directory: "/Users/tizi/tmp/screamingatmyscreen/site"
        jinja:
            template: "/Users/tizi/tmp/screamingatmyscreen/template"
        markdown:
            extras: ["tables"]
        blank:
            generate:
                index: "index"
        s3sub:
            bucket: test-bucket-sams
            profile: default

You always have to configure a `reader`, `writer`, `plugins`, and `url_scheme`.

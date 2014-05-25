# Embedding drupan
You can easily embed drupan in your application. First you setup an instance
of `Engine`

    from drupan.engine import Engine
    engine = Engine()
    engine.config.from_dict(cfg)
    engine.prepare_engine()

Now you can run the following commands

- `engine.run()` runs the site generation
- `engine.serve()` runs the development server
- `engine.deploy()` deploys the site

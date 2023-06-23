__author__ = "reed@reedjones.me"

import os
import shutil
import subprocess
from pathlib import Path, PurePosixPath

import frontmatter
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from drupan.entity import Entity
from drupan.file_wrapper import FileWrapper
from drupan.template import filter_more, filter_filter, filter_get


def copy_files(start_dir, target_dir):
    for root, dirs, files in os.walk(start_dir):  # replace the . with your starting directory
        for file in files:
            path_file = os.path.join(root, file)
            shutil.copy2(path_file, target_dir)  # change you destination dir


def render_it(root_path=None, item_path=None, config_obj=None, site_obj=None, obj=None):
    if not root_path or not item_path or not config_obj or not site_obj or not obj:
        print("Bad call ")
        exit(1)
    env = Environment(
        loader=FileSystemLoader([root_path, "C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog"]),
        extensions=["jinja2.ext.do"]
    )

    env.filters["more"] = filter_more
    env.filters["filter"] = filter_filter
    env.filters["get"] = filter_get
    print(f"Rendering {item_path} from {root_path} \n Searching for file,path")
    try:
        print("trying posix with replace")
        template = env.get_template(str(PurePosixPath(item_path)).replace('\\', '/'))
    except TemplateNotFound:
        try:
            print("trying normal")
            template = env.get_template(item_path)
        except TemplateNotFound:
            try:
                print("trying posix no replace")
                template = env.get_template(str(PurePosixPath(item_path)))
            except TemplateNotFound:
                print("trying realtive")
                try:
                    template = env.get_template(str(Path(item_path).relative_to(Path(root_path))))
                except TemplateNotFound:
                    template = env.get_template(str(Path(item_path).relative_to(Path(root_path))).replace('\\', '/'))

    print("Got file, now rendering")
    rendered = template.render(
        obj=obj,
        site=site_obj,
        config=config_obj
    )
    return rendered


def check_files(start_dir, **kwargs):
    render_args = kwargs
    for root, dirs, files in os.walk(start_dir):  # replace the . with your starting directory
        for file in files:
            path_file = os.path.join(root, file)
            render_args['item_path'] = path_file
            t = ['dir_index.html', 'dirtree.html']
            if path_file.endswith(".html"):
                handle = open(path_file, "r", encoding="utf-8")

                # reading the file and storing the data in content
                content = handle.read()
                # replacing the data using replace()
                change = False
                new_content = None
                if "{%" in content:
                    for i in t:
                        if i in path_file:
                            print(f"Needs to be rendered (jinja): {path_file}")
                            change = True
                            new_content = render_it(**render_args)
                # close the file
                handle.close()
                if change and new_content:
                    print(f"Now updating {path_file}")
                    handle = open(path_file, "w", encoding="utf-8")
                    handle.write(new_content)
                    handle.close()

            # handle = open("favtutor.txt", "w")
            # handle.write(content)
            # handle.close()


def get_entities(md_source, html_source, config_obj, site_obj, rp):
    e = []
    for root, dirs, files in os.walk(md_source):
        for file in files:
            path_file = os.path.join(root, file)
            if path_file.endswith(".md"):
                entity_name = Path(path_file).name
                entity_html_name = entity_name.replace(".md", ".html")
                entity_html_path = path_file.replace(entity_name, entity_html_name).replace(md_source, html_source)
                if not os.path.isfile(entity_html_path):
                    print(f"problem {entity_html_path}")
                    exit(1)
                entity_html_relpath = str(Path(entity_html_path).relative_to(Path(rp)))
                if not os.path.isfile(entity_html_relpath):
                    print(f"problem {entity_html_relpath}")
                    exit(1)

                post = frontmatter.load(path_file)
                meta = post.metadata

                env = Environment(
                    loader=FileSystemLoader(searchpath=rp),
                    extensions=["jinja2.ext.do"]
                )

                env.filters["more"] = filter_more
                env.filters["filter"] = filter_filter
                env.filters["get"] = filter_get
                template = env.get_template(str(PurePosixPath(entity_html_relpath)).replace('\\', '/'))
                entity = Entity(config_obj)
                entity.meta = meta
                entity.rendered = template.render(
                    obj=entity,
                    site=site_obj,
                    config=config_obj
                )
                entity.name = Path(entity_html_path).stem

                e.append(entity)
                print(f"Created Entity")
                output_path = entity_html_path.replace(html_source,
                                                       "C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog\\site")
                print(f"Writing content to {output_path}")
                if "index.html" in output_path:
                    output_path = output_path.replace("index.html", "obs_index.html")
                write(entity.rendered, output_path)
    copy_files("C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog\\output\\html\\obs.html",
               "C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog\\site")

    return e


class Plugin(object):
    """
    obsidian_folder_path_str: "" #The location of your vault directory
    obsidian_entrypoint_path_str: "" #The location of your entrypoint note
    md_folder_path_str: "" #The (output/input) location of your markdown files
    md_entrypoint_path_str: "" #The (output/input) location of your markdown entrypoint file
    """
    plugin_name = "obsidian_loader"
    default_input = "obsidian_loader_input"
    default_output = "obsidian_loader_output"

    setup_opts = (
        ("input_folder", default_input),
        ("output_folder", default_output),
        ("plugin_config", "plugin_config.yaml"),
        ("root_dir", "C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog")
    )
    run_first = True

    """create empty entities"""

    run_after = "after_callback"

    def __str__(self):
        return self.plugin_name

    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config
        print("loaded obsidian loader")

        for item in self.setup_opts:
            v = config.get_option(self.plugin_name, item[0], return_default=item[1])
            setattr(self, item[0], v)

    def after_callback(self):
        print(self)
        # root_path, item_path, config_obj, site_obj, obj
        check_files("C:\\Users\\reedj\\Documents\\DrupanBlog\\drupan-template-blog\\site",
                    root_path=os.path.join(getattr(self, "root_dir"), "site"),
                    item_path=None, config_obj=self.config, site_obj=self.site, obj=self)

    def run(self):
        """run the plugin"""
        print("running loader")
        cmd = f"obsidianhtml convert -i {getattr(self, 'plugin_config')}"
        process = subprocess.Popen(cmd.split(" "),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=getattr(self, "root_dir"))
        stdout, stderr = process.communicate()
        if stderr:
            print(stderr)
            exit(1)
        print(stdout)
        md_target = os.path.join(getattr(self, "root_dir"), "output", "md")
        html_target = os.path.join(getattr(self, "root_dir"), "output", "html")

        entities = get_entities(md_target, html_target, self.config, self.site, getattr(self, "root_dir"))
        self.site.entities += entities

        # entity = Entity(self.config)
        # copy_files(md_target, os.path.join(getattr(self, "root_dir"), "content"))
        # copy_files(html_target, os.path.join(getattr(self, "root_dir"), "site"))


def write(content, path):
    """
    Write an entity to disk

    Arguments:
        content: content to write
        path: path to write to
    """
    if isinstance(content, FileWrapper):
        with open(path, "wb") as output:
            output.write(content.read())
    else:
        with open(path, "w", encoding="utf-8") as output:
            output.write(content)

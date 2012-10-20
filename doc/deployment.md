# Deployment
After running drupan you have a static site in your
```site``` directory. If you do not change your site
on a regular basis you can just copy the folder to
your server using (s)ftp and continue working. But
if you blog on a regular basis I suggest you take a
look at different options.

## Git
Currently the only option integrated as a plugin is 
git. If you stuck to the default directory structure 
go to your path which holds ```config.yaml```, run 
```git init``` and add a remote named ```server```.

On your server you should have a bare repository.

Add ```gitsub``` as last entry to the ```plugins``` 
array in ```config.yaml```. Now every time you run 
drupan without ```--nodeploy``` a commit will be done 
and your repository will be pushed to the remote 
called ```server```.

### Automation
Simple. I assume you push your site to 
```/home/leet/awesomesite``` and that you have write 
access to the document root of your web server. Let 
us say you use ```/home/leet/domain.tld/```.

Create a ```post-receive``` script in 
```/home/leet/awesomesite/.git/hooks``` and add the 
following lines.

    #!/bin/sh
    GIT_WORK_TREE=/home/leet/domain.tld/ git checkout -f

Now you only need to make it executable with 
```chmod +x /home/leet/awesomesite/.git/hooks/post-receive``` 
and you are done.
Every time you now run drupan your site is pushed to your 
server, checked out and the whole world can read what you 
just published.

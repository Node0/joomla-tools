# joomla-tools

### All tooling is currently oriented towards Joomla 4

Joomla tooling scripts to scaffold Components, Plugins, (and maybe one day modules).

PLEASE NOTE: You will need Python 3.6 or later and the `os`, `sh`, and `argparse` libraries installed. Of these only `sh` requires manual installation which can be accomplished as follows: `pip3 install sh`

#### General goals:

- To have a command line configurable J! 4 component skeleton maker (ready)
- To have a command line configurable J! 4 plugin skeleton maker (under construction)
- To have a command line configurable J! 4 module skeleton maker (in backlog)  
   
`07-25-2022:` Updated `pluginMaker.py` and `componentMaker.py` to include the un-joomla (more like express style of single method response within controllers) style of handling REST requests, in `componentMaker.py` that consists of the `--api-controller-design="unjoomla-fast"` argument and in `pluginMaker.py` that consists of the `--plugin-meta="webservices-granular"` argument. Additionally, if you pass the webservices plugin type in the plugin type argument i.e. `--plugin-type="webservices"` you are now required to then specify the relevant component name string that will be responsible for handling your REST routes via the --plugin-webservices-component-name argument i.e. `--plugin-webservices-component-name="com_generichelloworld"`.
After playing around with this and getting some SO feedback, I'll slightly refactor the demo code gen to create a set of extensions that work together and generate an actual working "hello world" response along with some database oriented responses e.g. _getCurrentLoggedInUser_ or some such in order to showcase actual db access logic. That will go a long way towards bootstrapping newcomers into J! 4's webservices REST potential. So hit that star button or follow me on github to stay updated with new developments.
  
  
`04-19-2022:` `componentMaker.py` now takes `--api-controller-names` as either a string, or a comma separated list of controller names and generates a both controller scaffolds and jsonapi view  scaffolds, automatically. You'll have to actually write meaningful PHP within those files but all the Joomla-isms have been satisfies for you to write a plugin (or soon generate one via `pluginMaker.py`) and then go about deciding if you want to follow the Joomla way or go your own path. We follow the rules to spec, before choosing to break them or not, in any case the tools follow the rules.    
  
`04-15-2022:` The plugin maker is nearing completion (check pluginMaker branch for details) initial code-gen template is going to be the webservices code template (there are 25 types of plugins in J! 4, each with specific code template nuances), the webservices template will be completed first, then others will come online. Module maker is in backlog. Useful working features are optional sql support generation, and optional folder generation.  
  
`04-12-2022:` The component maker is ready, the plugin maker is under construction (refactor from component maker) and module maker is in backlog.

## How to use:

### Component maker usage:

```bash
./componentMaker.py \
  --component-name="Generic Hello World" \
  --component-desc="A generic hello world component for J! 4" \
  --vendor-name="joomlaology" \
  --author-name="Joe Hacobian" \
  --author-url="https://algorithme.us" \
  --copyright-holder="Joe Hacobian" \
  --creation-month="April" \
  --creation-year="2022" \
  --component-version="0.0.1" \
  --api-controller-names="users,sports,weather,airlinetickets" \
  --api-controller-design="joomla-bloat"
```
<br>
Note: If you'de like to see comprehensive database and input manipulation examples,
Set the api-controller-design value to "unjoomla-fast" i.e. --api-controller-design="unjoomla-fast"
Enjoy the unfettered REST potential of Joomla 4!

### Plugin maker usage:

```
./pluginMaker.py \
  --plugin-name="Generic Hello World" \
  --plugin-desc="A generic hello world (REST API) plugin for J! 4" \
  --plugin-type="webservices" \
  --plugin-webservices-component-name="com_generichelloworld" \
  --plugin-meta="webservices-granular" \
  --vendor-name="joomlaology" \
  --author-name="Joe Hacobian" \
  --author-url="https://algorithme.us" \
  --copyright-holder="Joe Hacobian" \
  --creation-month="April" \
  --creation-year="2022" \
  --plugin-version="0.0.1" \
  --add-folders="tmpl,lib,src" \
  --add-sql-support
```

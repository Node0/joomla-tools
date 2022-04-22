# joomla-tools

### All tooling is currently oriented towards Joomla 4

Joomla tooling scripts to scaffold components, Modules, and Plugins.

PLEASE NOTE: You will need Python 3.6 or later and the `os`, `sh`, and `argparse` libraries installed. Of these only `sh` requires manual installation which can be accomplished as follows: `pip3 install sh`

#### General goals:

- To have a command line configurable J! 4 component skeleton maker (ready)
- To have a command line configurable J! 4 plugin skeleton maker (under construction)
- To have a command line configurable J! 4 module skeleton maker (in backlog)  
   
`04-19-2022:` componentMaker.py now takes --api-controller-names as either a string, or a comma separated list of controller names and generates a both controller scaffolds and jsonapi view  scaffolds, automatically. You'll have to actually write meaningful PHP within those files but all the Joomla-isms have been satisfies for you to write a plugin (or soon generate one via pluginMaker.py) and then go about deciding if you want to follow the Joomla way or go your own path. We follow the rules to spec, before choosing to break them or not, in any case the tools follow the rules.    
  
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
  --api-controller-names="users,sports,weather,airlinetickets"
```

### Plugin maker usage:

```
./pluginMaker.py \
  --plugin-name="Generic Hello World" \
  --plugin-desc="A generic hello world (REST API) plugin for J! 4" \
  --plugin-type="webservices" \
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

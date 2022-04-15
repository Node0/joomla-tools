# joomla-tools

### All tooling is currently oriented towards Joomla 4

Joomla tooling scripts to scaffold components, Modules, and Plugins.

PLEASE NOTE: You will need Python 3.6 or later and the `os`, `sh`, and `argparse` libraries installed. Of these only `sh` requires manual installation which can be accomplished as follows: `pip3 install sh`

#### General goals:

- To have a command line configurable J! 4 component skeleton maker (ready)
- To have a command line configurable J! 4 plugin skeleton maker (under construction)
- To have a command line configurable J! 4 module skeleton maker (in backlog)

##### 04-12-2022: The component maker is ready, the plugin maker is under construction (refactor from component maker) and module maker is in backlog.

## How to use:

### Component maker usage:

```
./componentMaker.py \
  --component-name="Generic Hello World" \
  --component-desc="A generic hello world component for J! 4" \
  --vendor-name="joomlaology" \
  --author-name="Joe Hacobian" \
  --author-url="https://algorithme.us" \
  --copyright-holder="Joe Hacobian" \
  --creation-month="April" \
  --creation-year="2022" \
  --component-version="0.0.1"
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
  --add-tmpl-dir="tmpl" \
  --add-src-dir="src" \
  --add-lib-dir="lib" \
  --add-sql-dir="True"
```

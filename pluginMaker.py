#!/usr/bin/env python3

# You'll need the sh library for this script to function properly.
# pip3 install sh
import os, sh, sys, argparse

class PluginMaker:
  def __init__(self):
    parser = argparse.ArgumentParser(
    description='Customize your J! 4 Plugin scaffold.',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    allow_abbrev=False,
    epilog="""Please Note:
This script requires python3.6 or later and also requires the sh library.
You may install the sh library via: pip3 install sh

Usage Example in Bash/sh/zsh:
./pluginMaker.py \\
  --plugin-name="Generic Hello World" \\
  --plugin-desc="A generic hello world (REST API) plugin for J! 4" \\
  --plugin-type="webservices" \\
  --plugin-webservices-component-name="genericHelloWorld" \\
  --plugin-meta="webservices-granular" \\
  --vendor-name="joomlaology" \\
  --author-name="Joe Hacobian" \\
  --author-url="https://algorithme.us" \\
  --copyright-holder="Joe Hacobian" \\
  --creation-month="April" \\
  --creation-year="2022" \\
  --plugin-version="0.0.1" \\
  --add-folders="tmpl,lib,src" \\
  --add-sql-support

  From there, test your plugin scaffold by installing the zip file into Joomla.
  You may then copy the generated folder into your git repo and begin development.""")


    # TODO: Make argparse output colorized so this is easier on the eyes.
    parser.add_argument('--plugin-name',       required=True,   metavar='e.g. --plugin-name="Generic Hello World"',
                        help="""The plugin's name""")
    parser.add_argument('--plugin-desc',       required=True,   metavar='e.g. --plugin-desc="A generic hello world plugin for J! 4"',
                        help="""The plugin's description""")
    # Adding mutually exclusive plugin type args
    plgTypeGroup = parser.add_mutually_exclusive_group(required=True)
    plgTypeGroup.add_argument('--plugin-type',                  metavar='e.g. --plugin-type="webservices"',
                              help="""The plugin type, must be one of the following: "actionlog", "authentication", "captcha", "editors", "extension", "filesystem", "media-action", "quickicon", "system", "twofactorauth", "webservices", "api-authentication", "behaviour", "content", "editors-xtd", "fields", "finder", "installer", "privacy", "sampledata", "task", "user", "workflow" this argument is mutually exclusive with --plugin-type-custom (ONLY USE ONE OF THEM)""")
    plgTypeGroup.add_argument('--plugin-type-custom',           metavar='e.g. --plugin-type-custom="my-custom-plugin-type"',
                              help="""The name of your custom plugin type, this is mutually exclusive with --plugin-type (ONLY USE ONE OF THEM)""")
    # Back to our regularly scheduled argparse setup...
    parser.add_argument('--vendor-name',       required=True,   metavar='e.g. --vendor-name="joomlaology"',
                        help="""The vendor name used in configuring namespaces, typically your org or author's name""")
    parser.add_argument('--author-name',       required=True,   metavar='e.g. --author-name="Joe Hacobian"',
                        help="""The code author's name""")
    parser.add_argument('--author-url',        required=True,   metavar='e.g. --author-url="https://algorithme.us"',
                        help="""The code author's website URL""")
    parser.add_argument('--copyright-holder',  required=True,   metavar='e.g. --copyright-holder="Joe Hacobian"',
                        help="""The copyright holder's name""")
    parser.add_argument('--creation-month',    required=True,   metavar='e.g. --creation-month="January"',
                        help="""Month of this plugin's creation""")
    parser.add_argument('--creation-year',     required=True,   metavar='e.g. --creation-year="2022"',
                        help="""Year of this plugin's creation""")
    parser.add_argument('--license-type',      required=False,  metavar='e.g. --license-type="MIT License"',
                        help="""OPTIONAL: Your license type, if argument not passed this defaults to GPL v2""")
    parser.add_argument('--plugin-version',    required=True,   metavar='e.g. --plugin-version="0.0.1"',
                        help="""The plugin's version string""")
    parser.add_argument('--plugin-meta',       required=False,  metavar='e.g. --plugin-meta="webservices-granular"',
                        help="""OPTIONAL: A string to enable special code generation or other feature flags, currently accepted values are: webservices-granular""")
    parser.add_argument('--plugin-webservices-component-name',       required=False,  metavar='e.g. --plugin-webservices-component-name="com_generichelloworld"',
                        help="""CONDITIONALLY OPTIONAL: The name of the J! 4 component that will be used to handle the plugin's webservices. If --plugin-type is 'webservices', this argument is required.""")
    parser.add_argument('--initial-view-name', required=False,  metavar='e.g. --initial-view-name="CanPluginsEvenHaveViews"',
                        help="""OPTIONAL: Set the name of the initial view. If argument not passed this defaults to Main""")
    parser.add_argument('--add-folders',       required=False,  metavar='e.g. --add-folders="tmpl"',
                        help="""OPTIONAL: If the user supplies either a single name or a list of comma separated names. This option creates folders from those names and updates the manifest file accordingly.""")
    parser.add_argument('--add-sql-support',   required=False,  default=False, action='store_true',
                        help="""OPTIONAL: This is a flag that if passed as --add-sql-support will create an sql directory with standard install/uninstall/update sql files and manifest xml hooks.""")
    # The following commented out declarations are for illustration purposes.
    # parser.add_argument('-a', '--author-name',      required=True, help="""The code author's name""")
    # positional arg declaration parser.add_argument('foo', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    self.args = parser.parse_args()

    self.JCorePluginTypes = [ "actionlog", "authentication", "captcha", "editors", "extension", "filesystem", "media-action", "quickicon", "system", "twofactorauth", "webservices", "api-authentication", "behaviour", "content", "editors-xtd", "fields", "finder", "installer", "privacy", "sampledata", "task", "user", "workflow" ] # type: list[str]


    # Basic plugin creation directory location and permissions
    self.currDir = sh.pwd().strip()
    self.folderPermissions = "0755"
    self.filePermissions = "0644"

    # Basic sanity checking for plugin_type against core J! types then if not set, use plugin_type_custom
    if ( self.args.plugin_type is not None ):
      if ( self.args.plugin_type in self.JCorePluginTypes ):
        self.plgType = self.args.plugin_type
    else:
      self.plgType = self.args.plugin_type_custom

    # Add plugin meta flag if set
    if ( self.args.plugin_meta is not None ):
      self.plgMeta = self.args.plugin_meta
    else:
      self.plgMeta = None

    # Add plugin webservices component name if --plugin-type is set to 'webservices' and raise exception if not set
    if ( self.plgType == "webservices" ):
      if ( self.args.plugin_webservices_component_name is not None ):
        self.plgWebSvcComName = self.args.plugin_webservices_component_name.lower()
      else:
        raise Exception(f"""--plugin-type provided was 'webservices' but --plugin-webservices-component-name was not provided.\n
Please provide a component name for the component responsible for handling the webservices routes.
The value passed to --plugin-webservices-component-name MUST match the "com_" name of the component\n
e.g. The folder name of the component under the api folder. An example component such as: [siteroot]/api/components/com_generichelloworld\n
Would result in the value: "com_generichelloworld" being passed to --plugin-webservices-component-name here is a --plugin-type="webservices" example below:\n
e.g. --plugin-type="webservices" --plugin-webservices-component-name="com_generichelloworld"\n """)


    # Plugin specific global details
    self.plgName = self.args.plugin_name
    self.plgNameJoomla = self.plgName.lower().replace(" ","")
    self.plgNameJoomlaDbTblPrfx = self.plgName.lower().replace(" ","_")
    self.plgNameInNamespaces = self.plgName.replace(" ","")
    self.plgManifestNameField = f"plg_{self.plgType}_{self.plgNameJoomla}"
    self.plgDesc = self.args.plugin_desc


    # This pertains to the php namespace configuration
    self.vendorName = self.args.vendor_name

    self.plgAuthor = self.args.author_name
    self.plgAuthorUrl = self.args.author_url
    self.plgCopyRightHolder = self.args.copyright_holder
    self.plgCreationMonth = self.args.creation_month
    self.plgCreationYear = self.args.creation_year
    self.plgCreationMonthAndYear = f"{self.plgCreationMonth} {self.plgCreationYear}"

    # If a custom license type is specified, use it, else GPL v2
    self.plgLicenseType = self.args.license_type if self.args.license_type != None else "GPL v2"


    self.plgVersion = self.args.plugin_version

    # Create the Plugin type folder (transparently if not exists) and then the plugin container folder.
    # within the current directory (where the executing python file resides)
    self.plgFolderName = f"{self.plgNameJoomla}"
    self.plgPackageBaseFolder = f"{self.currDir}/{self.plgFolderName}"


    # Initial language locale to setup
    self.langLocaleCode = "en-GB"


    # If a custom initial view name is specified, use it, else use "Main"
    # self.initialViewName = self.args.initial_view_name if self.args.initial_view_name != None else "Main"

    # self.initialViewNameLower = f"{self.initialViewName.lower()}"
    # self.initialViewMenuItemTitle = f"Menu Item for {self.initialViewName} view"

  # Check for user supplied sql support flag and if set, create sql assets and prepare manifest partial
  def handleSqlSupport(self):
    if ( self.args.add_sql_support ):
      # SQL folder name
      self.sqlDirName = 'sql'
      # SQL Filenames
      self.sqlInstallFilename = "install.mysql.utf8.sql"
      self.sqlUninstallFilename = "uninstall.mysql.utf8.sql"
      self.sqlUpdateFilename = f"{self.plgVersion}.sql"
      # This is simply the first table's name for illustrative purposes
      self.initialTableName = f"{self.plgManifestNameField}_storage_table_1"
      self.sqlDirPath = f"{self.plgPackageBaseFolder}/{self.sqlDirName}"
      self.sqlDirNameManifestPartial = f"<folder>{self.sqlDirName}</folder>"
      self.sqlHooksInManifestPartial = f"""
      <install>
            <sql>
                <file driver="mysql" charset="utf8">sql/{self.sqlInstallFilename}</file>
            </sql>
        </install>
        <uninstall>
            <sql>
                <file driver="mysql" charset="utf8">sql/{self.sqlUninstallFilename}</file>
            </sql>
        </uninstall>
        <update>
            <schemas>
                <schemapath type="mysql">sql/updates/mysql</schemapath>
            </schemas>
        </update>"""[7:]
      self.setupSqlAssetFolder()
      self.setupSqlInstallFile()
      self.setupSqlUninstallFile()
      self.setupSqlUpdateFile()
    else:
      self.sqlDirNameManifestPartial = ""
      self.sqlHooksInManifestPartial = ""

  # Check for any optional folders the user may have specified
  # If there is a comma in the string, split into an array and create a folder named after each element of the array
  # In the event there is no comma, just create one folder from the string
  def handleOptionalFolders(self):
    self.optFolderNameManifestPartial = ""
    if ( self.args.add_folders is not None and type(self.args.add_folders) is str ):
      self.optFolderList = self.args.add_folders
      indexHtmlFile = 'index.html'
      indexHtmlFileContents = "<!DOCTYPE html><title></title>"
      if ( ',' in self.optFolderList ):
        for idx, folder in enumerate(self.optFolderList.split(',')):
          self.createFile(assetType = "d", targetPath = f"{self.plgPackageBaseFolder}/{folder}")
          self.createFile(assetType = "f", targetPath = f"{self.plgPackageBaseFolder}/{folder}/{indexHtmlFile}", fileContents = indexHtmlFileContents)
          # If this is the first time through the loop template the folder element string without pre-padding
          if ( idx == 0):
            self.optFolderNameManifestPartial += f"""<folder>{folder}</folder>\n"""
          else:
            # If this is the 2nd time through the loop, pre-pad the folder element string with
            # indentation relative to the manifest file string.
            self.optFolderNameManifestPartial += f"""          <folder>{folder}</folder>\n"""
      else:
        folder = self.optFolderList
        self.optFolderNameManifestPartial = f"""<folder>{folder}</folder>"""
        self.createFile(assetType = "d", targetPath = f"{self.plgPackageBaseFolder}/{folder}")
        self.createFile(assetType = "f", targetPath = f"{self.plgPackageBaseFolder}/{folder}/{indexHtmlFile}", fileContents = indexHtmlFileContents)

  # Folder asset, file asset, and writer function helper
  def createFile(self, assetType = "f", targetPath = None, fileContents = None):
    filePerms = self.filePermissions if self.filePermissions else "0644"
    folderPerms = self.folderPermissions if self.folderPermissions else "0755"
    fileAsset = None
    directoryAsset = None

    if( assetType == "d" and targetPath == None):
      print("""You have chosen to create a directory WITHOUT providing a target path.\nPlease provide: self.createFileAndWriteContents(targetPath = "/path/of/desired/asset" """)
    elif ( assetType == "f" and targetPath == None):
      print("""You have chosen to create a file WITHOUT providing a target path.\nPlease provide: self.createFileAndWriteContents(targetPath = "/path/of/desired/asset" """)
    elif ( assetType == "f" and targetPath != None and type(targetPath) == str):
      fileAsset = targetPath
    elif ( assetType == "d" and targetPath != None and type(targetPath) == str):
      directoryAsset = targetPath

    # Create directory if not exists ("mkdir -p" will silently desist if dir exists)
    if ( type(directoryAsset) == str ):
      sh.mkdir("-p", f"{directoryAsset}")
      sh.chmod(folderPerms, directoryAsset)

      if ( os.path.exists(directoryAsset) ):
        print( f"Created dir: {directoryAsset}, with 755 permissions" )
      else:
        print( f"ERROR encountered in creating dir: {directoryAsset}" )
      return

    if ( type(fileAsset) == str ):
      # Create containing dir for file first
      targetPathArray = fileAsset.split("/")
      targetPathArray.pop()
      fileAssetContainingDir = "/".join(targetPathArray)
      sh.mkdir("-p", f"{fileAssetContainingDir}")
      # Create file and set perms to 644
      sh.touch(f"{fileAsset}")
      sh.chmod(filePerms, fileAsset)
      if ( os.path.exists(fileAsset) and fileContents != None ):
        with open(fileAsset, "wt") as fileHandle:
          fileHandle.write(fileContents)
          fileHandle.close()

      if ( os.path.exists(fileAsset) ):
        if ( fileContents == None and os.path.getsize(fileAsset) == 0 ):
          print( f"Created file: {fileAsset}, with 644 permissions" )
        elif ( fileContents == None and os.path.getsize(fileAsset) != 0  ):
          print(f"ERROR empty file creation specified, but {fileAsset} is not empty, please verify")
        elif ( fileContents != None and os.path.getsize(fileAsset) > 0 ):
          print( f"""Created file: {fileAsset}, with 644 permissions, and wrote contents:{fileContents[0:85]}...""" )
          return

  def setupPluginFolder(self):
    # Create the base plugin folder
    self.createFile(assetType = "d", targetPath = self.plgPackageBaseFolder)

  # This method handles preparation of the MANY types of plugin php files' contents
  # For now we'll stick to handling the webservices type, but build handling logic to
  # dynamically substitute plugin file contents when other types are introduced.
  def preparePluginPhpFileContents(self):
    pluginPhpFileContents = ""
    plgClassName = f"Plg{self.plgType.capitalize()}{self.plgNameJoomla.capitalize()}"
    # Handle templates for core types.
    if ( self.args.plugin_type is not None ):
      print(self.plgType)

      # Start IF/ELIF cascade to handle template string for each core type and meta variant if applicable.
      # Note: This method MUST `return pluginPhpFileContents` after each if/elif in order to function properly
      if ( self.plgType == "webservices" and self.plgMeta != "webservices-granular" ):
        pluginPhpFileContents = rf"""
        <?php
defined('_JEXEC') or die;

use Joomla\CMS\Plugin\CMSPlugin;
use Joomla\CMS\Router\ApiRouter;

class {plgClassName} extends CMSPlugin
{{
	protected $autoloadLanguage = true;
	public function onBeforeApiRoute(&$router)
	{{
		$router->createCRUDRoutes(
			'v1/<endpointString>', /* An arbitrary route endpoint string */
			'<ControllerName>', /* The controller file's <CONTROLLER_NAME> segment in <SITEROOT>/api/components/{self.plgWebSvcComName}/src/controller/<CONTROLLER_NAME>Controller.php */
			['component' => '{self.plgWebSvcComName}']
		);
		$router->createCRUDRoutes(
			'v1/<endpointString>/categories',
			'categories',
			['component' => 'com_categories', 'extension' => '{self.plgWebSvcComName}']
		);
	}}
}}
        """[9:]
        return pluginPhpFileContents

      elif ( self.plgType == "webservices" and self.plgMeta == "webservices-granular" ):
        print("Executing case 2 (granular Joomla webservices)")
        pluginPhpFileContents = rf"""
        <?php
defined('_JEXEC') or die;
use Joomla\CMS\Plugin\CMSPlugin;
use Joomla\Router\Route;
use Joomla\CMS\Log\Log;

class {plgClassName} extends CMSPlugin
{{
  protected $autoloadLanguage = true;

  public function onBeforeApiRoute(&$router)
  {{
    // A nice granular way to do it.
    // new Route(['HTTP_METHOD'],  'arbitrary/pattern/string',                     '<CONTROLLER_NAME>.<PUBLIC_METHOD_NAME>',               [], $defaults)
    // Obviously substitute the COMPONENTNAME (lowercase no spaces), <CONTROLLER_NAME> as lowercase, & PUBLIC_METHOD_NAME as camelcase.
    // controllers are to be placed in [site_root]/api/components/{self.plgWebSvcComName}/src/Controllers/<CONTROLLER_NAME>Controller.php

    // An 'Airport' component is assumed for the purposes of illustration, please modify this file to match your actual controller class names.
    // So the 'hangars' controller below would in fact be located at:  [site_root]/api/components/{self.plgWebSvcComName}/src/Controllers/HangarsController.php
    // inside of it would be a public method called getHangarsByAirline() etc

    // An obvious example for ease of comprehension
    $defaults    = array_merge(['public' => false], ['component' => '{self.plgWebSvcComName}']);
    $routes = [
      /* My Useful GET routes */
      new Route(['GET'],   'v1/airport/hangars/by/airline/:airLineName',     'hangars.getHangarsByAirline',                ['airLineName'    => '(filter.+validation.+regex)'], $defaults),
      /* No filtration regex allows ALL patterns to pass through into Jinput on the controller side. */
      new Route(['GET'],  'v1/airport/hangar/by/id/:id',                          'hangars.getHangarById',                 ['id' => '(\d{{1,9}})'], $defaults),
      /* No filtration regex allows ALL patterns to pass through into Jinput on the controller side. */
      new Route(['GET'],  'v1/airport/lounges/by/airline/:airLineName',    'lounges.getLoungesByAirline',           [], $defaults),
      /* My Useful POST routes */
      /*
      * If no url parameter is specified then no checking is necessary!
      * Note: same rules apply as for GET routes above if you DID want to have parameters).
      *
      * In the POST example below you need to grab the POST body via: $req = json_decode( $this->input->json->getRaw() ); on the controller side
      * If you want an associative array use: $req = json_decode( $this->input->json->getRaw(), true ); on the controller side
      */
      new Route(['POST'],  'v1/airport/purchase/ticket',                     'tickets.purchaseTicket',               [], $defaults)
    ];
    // Finally, register all specified routes with Joomla's webservices router.
    $router->addRoutes($routes);
  }}
}}
        """[9:]
        return pluginPhpFileContents

      elif ( self.plgType == "user" ):
        pluginPhpFileContents = f"""
        <?php
defined('_JEXEC') or die;

use Joomla\CMS\Plugin\CMSPlugin;
class {plgClassName} extends CMSPlugin
{{
	protected $autoloadLanguage = true;
  public function PLEASE_IMPLEMENT_ME()
  {{
    // Please implement whatever is found inside plugin of type '{self.plgType}';
  }}
}}
        """[9:]
        return pluginPhpFileContents

    if ( self.args.plugin_type_custom is not None ):
      pluginPhpFileContents = f"""
      <?php
defined('_JEXEC') or die;

use Joomla\CMS\Plugin\CMSPlugin;
class {plgClassName} extends CMSPlugin
{{
	protected $autoloadLanguage = true;
  public function PLEASE_IMPLEMENT_ME()
  {{
    // Please implement whatever is found inside plugin of type '{self.plgType}';
  }}
}}
        """[7:]
      return pluginPhpFileContents

  def setupPluginPhpFile(self):
    # Create the plugin php file container
    pluginPhpFile = f"{self.plgPackageBaseFolder}/{self.plgNameJoomla}.php"
    self.createFile( assetType = "f", targetPath = pluginPhpFile, fileContents = self.preparePluginPhpFileContents() )


  def setupPluginManifestFile(self):
    # Create the plugin manifest xml file container
    pluginManifestFile = f"{self.plgPackageBaseFolder}/{self.plgNameJoomla}.xml"
    ##########################################################################################################
    ##########################################################################################################
    ######################################## START Plugin Manifest XML #######################################
    ##########################################################################################################
    ##########################################################################################################
    pluginManifestContents = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <extension type="plugin" group="{self.plgType}" method="upgrade">

        <name>{self.plgManifestNameField}</name>
        <creationDate>{self.plgCreationMonthAndYear}</creationDate>
        <author>{self.plgAuthor}</author>
        <authorUrl>{self.plgAuthorUrl}</authorUrl>
        <copyright>{self.plgCopyRightHolder}</copyright>
        <license>{self.plgLicenseType}</license>
        <version>{self.plgVersion}</version>
        <description>{self.plgDesc}</description>
        <files>
          <filename plugin="{self.plgNameJoomla}">{self.plgNameJoomla}.php</filename>
          <folder>language</folder>
          {self.optFolderNameManifestPartial}
          {self.sqlDirNameManifestPartial}
        </files>

        <!-- While this construct works in components, it appears to cause failure messages in plugin installations
             Language files that exist in properly locale-labelled foldeers will continue to be installed as normal
             this is due to the language folder listed under files above.
        <languages>
          <language tag="{self.langLocaleCode}">{self.langLocaleCode}.{self.plgManifestNameField}.ini</language>
          <language tag="{self.langLocaleCode}">{self.langLocaleCode}.{self.plgManifestNameField}.sys.ini</language>
        </languages>
        -->

        {self.sqlHooksInManifestPartial}

    </extension>
    """[5:]
    ##########################################################################################################
    ##########################################################################################################
    ####################################### END Plugin Manifest XML #######################################
    ##########################################################################################################
    ##########################################################################################################
    self.createFile(assetType = "f", targetPath = pluginManifestFile, fileContents = pluginManifestContents)

    ##########################################################################################################
    ############################################ START i8n setup #############################################
    ##########################################################################################################

  def setupLanguageLangLocalCodeIniFile(self):
    languageLangLocalCodeIniFile = f"{self.plgPackageBaseFolder}/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.plgManifestNameField}.ini"
    #################################### START Admin i8n language strings ###################################
    languageLangLocalCodeIniFileContents = f"""
    ; {self.plgName} Translation Strings
    ; Copyright (C)  {self.plgCreationYear} {self.plgCopyRightHolder}. All Rights Reserved.

    PLG_HELLOWORLD_MSG_HELLO_WORLD="Hello World (i8n translation string)!"
    """[5:]
    ##################################### END Admin i8n language strings ####################################
    self.createFile(assetType = "f", targetPath = languageLangLocalCodeIniFile, fileContents = languageLangLocalCodeIniFileContents)

  def setupLanguageLangLocalCodeSysIniFile(self):
    languageLangLocalCodeSysIniFile = f"{self.plgPackageBaseFolder}/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.plgManifestNameField}.sys.ini"
    #################################### START Admin i8n language strings ###################################
    languageLangLocalCodeSysIniFileContents = f"""
    ; {self.plgName} Sys.ini Translation Strings
    ; Copyright (C)  {self.plgCreationYear} {self.plgCopyRightHolder}. All Rights Reserved.

    PLG_HELLOWORLD_SYS_HELLO_WORLD_TITLE="Hello World (i8n translation string)!"
    PLG_HELLOWORLD_SYS_HELLO_WORLD_DESC="My first Joomla! 4 Plugin!"
    """[5:]
    ##################################### END Admin i8n language strings ####################################
    self.createFile(assetType = "f", targetPath = languageLangLocalCodeSysIniFile, fileContents = languageLangLocalCodeSysIniFileContents)

  ##########################################################################################################
  ############################################# END i8n setup ##############################################
  ##########################################################################################################



  ############################################################################################################################
  ##################################################### START SQL Section ####################################################
  ############################################################################################################################

  def setupSqlAssetFolder(self):
    # Create SQL asset directories
    self.sqlAssetFolder = f"{self.plgPackageBaseFolder}/sql"
    self.sqlAssetUpdatesFolder = f"{self.sqlAssetFolder}/updates/mysql"
    self.createFile(assetType = "d", targetPath = self.sqlAssetFolder)
    self.createFile(assetType = "d", targetPath = self.sqlAssetUpdatesFolder)

  def setupSqlInstallFile(self):
    # Create the Install SQL file (only runs upon installation (not updates i.e. install over existing installation))
    sqlInstallFile = f"{self.sqlAssetFolder}/{self.sqlInstallFilename}"
    #################################### START Install SQL ###################################
    sqlInstallFileContents = f"""
    DROP TABLE IF EXISTS `#__{self.initialTableName}`;

    CREATE TABLE `#__{self.initialTableName}`(
        `id` SERIAL NOT NULL COMMENT "The auto-increment pk of this i.e. {self.initialTableName} table",
        `name` VARCHAR(255) NOT NULL COMMENT "Required (can't be null) name field",
        `address` VARCHAR(255) NULL COMMENT "Example 'Address' field of {self.initialTableName} if no value provided, will be NULL",
        `city` VARCHAR(128) NULL COMMENT "Example 'City' field of {self.initialTableName} if no value provided, will be NULL",
        `state` VARCHAR(128) NULL COMMENT "Example 'State' field of {self.initialTableName} if no value provided, will be NULL",
        `zip_postcode` MEDIUMINT NULL COMMENT "Example 'Postal code' field of {self.initialTableName} if no value provided, will be NULL",
        PRIMARY KEY(`id`)
    ) ENGINE = InnoDB;

    /* Testing insertion into our newly created table */
    INSERT INTO `#__{self.initialTableName}` (`name`) VALUES
        ("Example.com"),
        ("Foo Bar Bat");
    """[5:]
    ##################################### END Install SQL ####################################
    self.createFile(assetType = "f", targetPath = sqlInstallFile, fileContents = sqlInstallFileContents)

  def setupSqlUninstallFile(self):
    # Create the Uninstall SQL file (only runs upon Uninstallation (not updates i.e. Install over existing innstallation))
    sqlUninstallFile = f"{self.sqlAssetFolder}/{self.sqlUninstallFilename}"
    #################################### START Uninstall SQL ###################################
    sqlUninstallFileContents = f"""
    DROP TABLE IF EXISTS `#__{self.initialTableName}`;

    """[5:]
    ##################################### END Uninstall SQL ####################################
    self.createFile(assetType = "f", targetPath = sqlUninstallFile, fileContents = sqlUninstallFileContents)

  def setupSqlUpdateFile(self):
    # Create the Update SQL file (only runs upon update (An update is an install over existing innstallation))
    sqlUpdateFile = f"{self.sqlAssetUpdatesFolder}/{self.sqlUpdateFilename}"
    #################################### START Update SQL ###################################
    sqlUpdateFileContents = f"""
    ALTER TABLE `#__{self.initialTableName}` ADD `new_field_from_update` TEXT NULL DEFAULT NULL AFTER `zip_postcode`,
    ADD FULLTEXT `idx_new_field_from_update` (`new_field_from_update`);
    """[5:]
    ##################################### END Update SQL ####################################
    self.createFile(assetType = "f", targetPath = sqlUpdateFile, fileContents = sqlUpdateFileContents)


  # # Create the Update SQL file (only runs upon Update (not Installs i.e. Installs over existing installation))
  # adminSqlUpdateFile = f"{self.sqlAssetUpdatesFolder}/{self.plgVersion}.sql"
  # #################################### START Update SQL ###################################
  # adminSqlUpdateFileContents = f"""
  # """[5:]
  # ##################################### END Update SQL ####################################
  # self.createFile(assetType = "f", targetPath = adminSqlUpdateFile, fileContents = adminSqlUpdateFileContents)

  ############################################################################################################################
  ###################################################### END SQL Section #####################################################
  ############################################################################################################################


  # # Create the first admin display controller
  # admin__PhpFile = f"{self.adminFolder}/.php"
  # #################################### START Admin services provider.php ###################################
  # admin__PhpFileContents = f"""
  # """
  # ##################################### END Admin services provider.php ####################################
  # self.createFile(assetType = "f", targetPath = admin__PhpFile, fileContents = admin__PhpFileContents)

  def finishAndCreateInstallable(self):
    if ( sh.which("tree") is not None ):
      # Recap the structure of created assets.
      dirStructCreated = sh.tree( self.plgPackageBaseFolder )
      print(dirStructCreated)
    else:
      print("\n\nIf you'd like to see directory tree visualizations (of the generated extension)\nInstall the tree program: yum install tree, or apt-get install tree\n\n")

    # Create the installable package
    sh.zip( "-r", f"{self.plgFolderName}.zip", f"{self.plgFolderName}" )
    print("Generation of extension is finished!")


  def execute(self):
    self.setupPluginFolder()
    self.setupLanguageLangLocalCodeIniFile()
    self.setupLanguageLangLocalCodeSysIniFile()
    self.handleSqlSupport()
    self.handleOptionalFolders()
    self.setupPluginPhpFile()
    self.setupPluginManifestFile()
    self.finishAndCreateInstallable()

PM = PluginMaker()
PM.execute()

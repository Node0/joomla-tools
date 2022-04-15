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
  --plugin-desc="A generic hello world plugin for J! 4" \\
  --vendor-name="joomlaology" \\
  --author-name="Joe Hacobian" \\
  --author-url="https://algorithme.us" \\
  --copyright-holder="Joe Hacobian" \\
  --creation-month="April" \\
  --creation-year="2022" \\
  --plugin-version="0.0.1"

  From there, test your plugin scaffold by installing the zip file into Joomla.
  You may then copy the generated folder into your git repo and begin development.""")

    parser.add_argument('--plugin-name',       required=True,   help="""The plugin's name""")
    parser.add_argument('--plugin-desc',       required=True,   help="""The plugin's description""")
    parser.add_argument('--plugin-type',       required=False,  help="""The plugin type, must be one of the following: "actionlog", "authentication", "captcha", "editors", "extension", "filesystem", "media-action", "quickicon", "system", "twofactorauth", "webservices", "api-authentication", "behaviour", "content", "editors-xtd", "fields", "finder", "installer", "privacy", "sampledata", "task", "user", "workflow" This value is overriden if --plugin-type-custom is passed alone or in tandem.""")
    parser.add_argument('--plugin-type-custom',required=False,  help="""The name of your custom plugin type, this overrides --plugin-type if supplied, and is used if passed alone.""")
    parser.add_argument('--vendor-name',       required=True,   help="""The vendor name used in configuring namespaces, typically your org or author's name""")
    parser.add_argument('--author-name',       required=True,   help="""The code author's name""")
    parser.add_argument('--author-url',        required=True,   help="""The code author's website URL""")
    parser.add_argument('--copyright-holder',  required=True,   help="""The copyright holder's name""")
    parser.add_argument('--creation-month',    required=True,   help="""Month of this plugin's creation""")
    parser.add_argument('--creation-year',     required=True,   help="""Year of this plugin's creation""")
    parser.add_argument('--license-type',      required=False,  help="""OPTIONAL: Your license type, defaults to GPL v2""")
    parser.add_argument('--plugin-version',    required=True,   help="""The plugin's version string""")
    parser.add_argument('--initial-view-name', required=False,  help="""OPTIONAL: Set the name of the initial view. Defaults to Main""")
    # The following commented out declarations are for illustration purposes.
    # parser.add_argument('-a', '--author-name',      required=True, help="""The code author's name""")
    # positional arg declaration parser.add_argument('foo', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    self.args = parser.parse_args()

    self.JCorePluginTypes = [ "actionlog", "authentication", "captcha", "editors", "extension", "filesystem", "media-action", "quickicon", "system", "twofactorauth", "webservices", "api-authentication", "behaviour", "content", "editors-xtd", "fields", "finder", "installer", "privacy", "sampledata", "task", "user", "workflow" ]


    # Basic plugin creation directory location and permissions
    self.currDir = sh.pwd().strip()
    self.folderPermissions = "0755"
    self.filePermissions = "0644"

    # Check for --plugin-type-custom if set, use it, else use --plugin-type
    # If both are empty, exit with error (argparse must allows unset state for both in order to allow this distinction dynamically)
    if ( self.args.plugin_type is None and self.args.plugin_type_custom is None ):
      sys.exit("""ERROR, you must supply either --plugin-type OR --plugin-type-custom, both cannot be left unspecified.\n""")
    elif ( self.args.plugin_type_custom is not None ):
      self.plgType = str( self.args.plugin_type_custom ).lower()
    elif ( self.args.plugin_type is not None and self.args.plugin_type in self.JCorePluginTypes ):
      self.plgType = str( self.args.plugin_type ).lower()
    else:
      sys.exit("""ERROR, invalid core plugin type specified with --plugin-type\nPlease see usage help for details about allowed core types.""")

    # Plugin specific global details
    self.plgName = self.args.plugin_name
    self.plgManifestNameField = f"plg_{self.plgType}_{self.plgName}"
    self.plgDesc = self.args.plugin_desc

    self.plgNameJoomla = self.plgName.lower().replace(" ","")
    self.plgNameInNamespaces = self.plgName.replace(" ","")

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

    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################
    # TODO: This file is under active refactoring, Joomla Plugin construction is vastly simpler than component
    # construction, so large portions of this file will change in order to reflect plugin creation details.
    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################
    ##############################################################################################################

    # Initial language locale to setup
    self.langLocaleCode = "en-GB"

    # SQL Filenames
    # self.sqlInstallFilename = f"install.mysql.utf8.sql"
    # self.sqlUninstallFilename = f"uninstall.mysql.utf8.sql"
    # self.sqlUpdateFilename = f"{self.plgVersion}.sql"
    # This is simply the first table's name for illustrative purposes
    # self.initialTableName = f"storage_table_1"

    # If a custom initial view name is specified, use it, else use "Main"
    # self.initialViewName = self.args.initial_view_name if self.args.initial_view_name != None else "Main"

    # self.initialViewNameLower = f"{self.initialViewName.lower()}"
    # self.initialViewMenuItemTitle = f"Menu Item for {self.initialViewName} view"


    # Create the Plugin type folder (transparently if not exists) and then the plugin container folder.
    # within the current directory (where the executing python file resides)
    self.plgFolderName = f"{self.plgNameJoomla}"
    self.plgPackageBaseFolder = f"{self.currDir}/{self.plgFolderName}"

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

  def setupPluginManifestFile(self):
    # Create the plugin manifest xml file container
    pluginManifestFile = f"{self.plgPackageBaseFolder}/{self.plgNameJoomla}.xml"
    #pluginManifestFile = f"{self.plgPackageBaseFolder}/manifest.xml"
    ##########################################################################################################
    ##########################################################################################################
    ###################################### START Plugin Manifest XML ######################################
    ##########################################################################################################
    ##########################################################################################################
    pluginManifestContents = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <extension type="plugin" method="upgrade">
    <!-- 'version' attribute for extension tag is no longer used -->

        <name>{self.plgName}</name>
        <creationDate>{self.plgCreationMonthAndYear}</creationDate>
        <author>{self.plgAuthor}</author>
        <authorUrl>{self.plgAuthorUrl}</authorUrl>
        <copyright>{self.plgCopyRightHolder}</copyright>
        <license>{self.plgLicenseType}</license>
        <version>{self.plgVersion}</version>
        <description>
            {self.plgDesc}
        </description>

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

  def setupAdminLanguageLangLocalCodeIniFile(self):
    adminLanguageLangLocalCodeIniFile = f"{self.adminFolder}/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.plgFolderName}.ini"
    #################################### START Admin i8n language strings ###################################
    adminLanguageLangLocalCodeIniFileContents = f"""
    ; {self.plgName} Admin Strings
    ; Copyright (C)  {self.plgCreationYear} {self.plgCopyRightHolder}. All Rights Reserved.

    COM_HELLOWORLD_MSG_HELLO_WORLD="Hello World (i8n translation string)!"
    """[5:]
    ##################################### END Admin i8n language strings ####################################
    self.createFile(assetType = "f", targetPath = adminLanguageLangLocalCodeIniFile, fileContents = adminLanguageLangLocalCodeIniFileContents)

  def setupAdminLanguageLangLocalCodeSysIniFile(self):
    adminLanguageLangLocalCodeSysIniFile = f"{self.adminFolder}/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.plgFolderName}.sys.ini"
    #################################### START Admin i8n language strings ###################################
    adminLanguageLangLocalCodeSysIniFileContents = f"""
    ; {self.plgName} Sys.ini Strings
    ; Copyright (C)  {self.plgCreationYear} {self.plgCopyRightHolder}. All Rights Reserved.

    COM_HELLOWORLD_MENU_HELLO_WORLD_TITLE="Hello World (i8n translation string)!"
    COM_HELLOWORLD_MENU_HELLO_WORLD_DESC="My first Joomla! page"
    """[5:]
    ##################################### END Admin i8n language strings ####################################
    self.createFile(assetType = "f", targetPath = adminLanguageLangLocalCodeSysIniFile, fileContents = adminLanguageLangLocalCodeSysIniFileContents)

  ##########################################################################################################
  ############################################# END i8n setup ##############################################
  ##########################################################################################################



  ############################################################################################################################
  ##################################################### START SQL Section ####################################################
  ############################################################################################################################

  def setupSqlAssetFolder(self):
    # Create SQL asset directories
    self.sqlAssetFolder = f"{self.adminFolder}/sql"
    self.sqlAssetUpdatesFolder = f"{self.sqlAssetFolder}/updates/mysql"
    self.createFile(assetType = "d", targetPath = self.sqlAssetFolder)
    self.createFile(assetType = "d", targetPath = self.sqlAssetUpdatesFolder)

  def setupAdminSqlInstallFile(self):
    # Create the Install SQL file (only runs upon installation (not updates i.e. install over existing installation))
    adminSqlInstallFile = f"{self.sqlAssetFolder}/{self.sqlInstallFilename}"
    #################################### START Install SQL ###################################
    adminSqlInstallFileContents = f"""
    DROP TABLE IF EXISTS `#__{self.plgNameJoomla}_{self.initialTableName}`;

    CREATE TABLE `#__{self.plgNameJoomla}_{self.initialTableName}`(
        `id` SERIAL NOT NULL COMMENT "The auto-increment pk of this i.e. {self.initialTableName} table",
        `name` VARCHAR(255) NOT NULL COMMENT "Required (can't be null) name field",
        `address` VARCHAR(255) NULL COMMENT "Example 'Address' field of {self.initialTableName} if no value provided, will be NULL",
        `city` VARCHAR(128) NULL COMMENT "Example 'City' field of {self.initialTableName} if no value provided, will be NULL",
        `state` VARCHAR(128) NULL COMMENT "Example 'State' field of {self.initialTableName} if no value provided, will be NULL",
        `zip_postcode` MEDIUMINT NULL COMMENT "Example 'Postal code' field of {self.initialTableName} if no value provided, will be NULL",
        PRIMARY KEY(`id`)
    ) ENGINE = InnoDB;

    /* Testing insertion into our newly created table */
    INSERT INTO `#__{self.plgNameJoomla}_{self.initialTableName}` (`name`) VALUES
        ("Example.com"),
        ("Foo Bar Bat");
    """[5:]
    ##################################### END Install SQL ####################################
    self.createFile(assetType = "f", targetPath = adminSqlInstallFile, fileContents = adminSqlInstallFileContents)

  def setupAdminSqlUninstallFile(self):
    # Create the Uninstall SQL file (only runs upon Uninstallation (not updates i.e. Install over existing innstallation))
    adminSqlUninstallFile = f"{self.sqlAssetFolder}/{self.sqlUninstallFilename}"
    #################################### START Uninstall SQL ###################################
    adminSqlUninstallFileContents = f"""
    DROP TABLE IF EXISTS `#__{self.plgNameJoomla}_{self.initialTableName}`;

    """[5:]
    ##################################### END Uninstall SQL ####################################
    self.createFile(assetType = "f", targetPath = adminSqlUninstallFile, fileContents = adminSqlUninstallFileContents)

  def setupAdminSqlUpdateFile(self):
    # Create the Update SQL file (only runs upon update (An update is an install over existing innstallation))
    adminSqlUpdateFile = f"{self.sqlAssetUpdatesFolder}/{self.sqlUpdateFilename}"
    #################################### START Update SQL ###################################
    adminSqlUpdateFileContents = f"""
    ALTER TABLE `#__{self.plgNameJoomla}_{self.initialTableName}` ADD `new_field_from_update` TEXT NULL DEFAULT NULL AFTER `zip_postcode`,
    ADD FULLTEXT `idx_new_field_from_update` (`new_field_from_update`);
    """[5:]
    ##################################### END Update SQL ####################################
    self.createFile(assetType = "f", targetPath = adminSqlUpdateFile, fileContents = adminSqlUpdateFileContents)


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
    # Recap the structure of created assets.
    dirStructCreated = sh.tree( self.plgPackageBaseFolder )
    print(dirStructCreated)

    # Create the installable package
    sh.zip( "-r", f"{self.plgFolderName}.zip", f"{self.plgFolderName}" )


  def execute(self):
    self.setupPluginFolder()
    self.setupPluginManifestFile()
    self.setupAdminLanguageLangLocalCodeIniFile()
    self.setupAdminLanguageLangLocalCodeSysIniFile()
    self.setupSqlAssetFolder()
    self.setupAdminSqlInstallFile()
    self.setupAdminSqlUninstallFile()
    self.setupAdminSqlUpdateFile()
    self.finishAndCreateInstallable()

PM = PluginMaker()
PM.execute()

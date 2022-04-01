#!/usr/bin/env python3

# You'll need the sh library for this script to function properly.
# pip3 install sh


import os, sh

# Basic component creation directory location and permissions
currDir = sh.pwd().strip()
folderPermissions = "0755"
filePermissions = "0644"

# Component specific global details
comName = "Generic Hello World"
comDesc = """A Hello World description!"""
comNameJoomla = comName.lower().replace(" ","")
comNameInNamespaces = comName.replace(" ","")

# This pertains to the php namespace configuration
vendorName = "joomlaology"

comAuthor = "Joe Hacobian"
comAuthorUrl = "https://algorithme.us"
comCopyRightHolder = "Joomlaology"
comCreationMonth = "March"
comCreationYear = "2022"
comCreationMonthAndYear = f"{comCreationMonth} {comCreationYear}"
comLicenseType = "GPL v2"
comVersion = "0.0.1"

# Initial language locale to setup
langLocaleCode = "en-GB"

# SQL Filenames
sqlInstallFilename = f"install.mysql.utf8.sql"
sqlUninstallFilename = f"uninstall.mysql.utf8.sql"
sqlUpdateFilename = f"{comVersion}.sql"
# This is simply the first table's name for illustrative purposes
initialTableName = f"storage_table_1"

initialViewName = "Main"
initialViewNameLower = f"{initialViewName.lower()}"
initialViewMenuItemTitle = f"Menu Item for {initialViewName} view"

# Folder asset, file asset, and writer function helper
def createFile(assetType = "f", targetPath = None, fileContents = None):
  filePerms = filePermissions if filePermissions else "0644"
  folderPerms = folderPermissions if folderPermissions else "0755"
  fileAsset = None
  directoryAsset = None

  if( assetType == "d" and targetPath == None):
    print("""You have chosen to create a directory WITHOUT providing a target path.\nPlease provide: createFileAndWriteContents(targetPath = "/path/of/desired/asset" """)
  elif ( assetType == "f" and targetPath == None):
    print("""You have chosen to create a file WITHOUT providing a target path.\nPlease provide: createFileAndWriteContents(targetPath = "/path/of/desired/asset" """)
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
##########################################################################################################


# Form the base component package folder name and create the folder
# within the current directory (where the executing python file resides)
comFolderName = f"com_{comNameJoomla}"
comPackageBaseFolder = f"{currDir}/{comFolderName}"

# Create the site and admin subfolders inside the component base folder
siteFolder  = f"{comPackageBaseFolder}/site"
adminFolder = f"{comPackageBaseFolder}/admin"
createFile(assetType = "d", targetPath = siteFolder)
createFile(assetType = "d", targetPath = adminFolder)

# Create the component manifest xml file container
componentManifestFile = f"{comPackageBaseFolder}/{comNameJoomla}.xml"
#componentManifestFile = f"{comPackageBaseFolder}/manifest.xml"
##########################################################################################################
##########################################################################################################
###################################### START Component Manifest XML ######################################
##########################################################################################################
##########################################################################################################
componentManifestContents = f"""
<?xml version="1.0" encoding="utf-8"?>
<extension type="component" method="upgrade">
<!-- 'version' attribute for extension tag is no longer used -->

    <name>{comName}</name>
    <creationDate>{comCreationMonthAndYear}</creationDate>
    <author>{comAuthor}</author>
    <authorUrl>{comAuthorUrl}</authorUrl>
    <copyright>{comCopyRightHolder}</copyright>
    <license>{comLicenseType}</license>
    <version>{comVersion}</version>
    <description>
        {comDesc}
    </description>

    <!-- This is the PHP namespace under which the extension's
    code is organised. It should follow this format:

    {vendorName}\Component\{comNameJoomla}

    "Vendor" can be your company or your own name

    The "ComponentName" section MUST match the name used
    everywhere else for your component. Whatever the name of
    this XML file is, the namespace must match (ignoring CamelCase).
    -->
    <namespace path="src">{vendorName}\Component\{comNameInNamespaces}</namespace>

    <files folder="site/">
        <folder>language</folder>
        <folder>src</folder>
        <folder>tmpl</folder>
    </files>

    <languages>
        <language tag="{langLocaleCode}">site/language/{langLocaleCode}/{langLocaleCode}.{comFolderName}.ini</language>
    </languages>

    <administration>
        <!-- The link that will appear in the Admin panel's "Components" menu -->
        <!-- NOTE: If we are only going to have a single menu item (under the components menu) appear
                   then the following element is sufficient:
                   <menu link="index.php?option={comFolderName}">{comName}</menu>
                   pay attention to the link url i.e. index.php?option={comFolderName} etc...
                   this structure is changed if we wish to show an expanded submenu underneath the
                   app's menu item (the app here being the component we're developing) then we'll need to
                   use a slightly different menu and submenu element structure as well as removing the index.php?
                   from the link attribute.
                   In all cases any use of query string parameters in the route requires ampersands to be specified as follows:
                   <menu link="option={comFolderName}&amp;view=<name_of_view>">Menu Item Title</menu>
                   See below for the actively used submenu implementation example.
                   -->
        <menu>{comName}</menu>
        <submenu>
          <menu link="option={comFolderName}">Dashboard</menu>
        </submenu>
        <!-- List of files and folders to copy. Note the 'folder' attribute. This is the name of the folder in your component package to copy FROM -->
        <files folder="admin">
            <folder>language</folder>
            <folder>services</folder>
            <folder>src</folder>
            <folder>sql</folder>
            <folder>tmpl</folder>
        </files>

        <languages>
            <language tag="{langLocaleCode}">admin/language/{langLocaleCode}/{langLocaleCode}.{comFolderName}.ini</language>
            <language tag="{langLocaleCode}">admin/language/{langLocaleCode}/{langLocaleCode}.{comFolderName}.sys.ini</language>
        </languages>
    </administration>

    <install>
        <sql>
            <file driver="mysql" charset="utf8">sql/{sqlInstallFilename}</file>
        </sql>
    </install>
    <uninstall>
        <sql>
            <file driver="mysql" charset="utf8">sql/{sqlUninstallFilename}</file>
        </sql>
    </uninstall>
    <update>
        <schemas>
            <schemapath type="mysql">sql/updates/mysql</schemapath>
        </schemas>
    </update>

</extension>
"""[1:]
##########################################################################################################
##########################################################################################################
####################################### END Component Manifest XML #######################################
##########################################################################################################
##########################################################################################################
createFile(assetType = "f", targetPath = componentManifestFile, fileContents = componentManifestContents)


################################### Create admin services provider.php ###################################
adminServicesProviderPhpFile = f"{adminFolder}/services/provider.php"
#################################### START Admin services provider.php ###################################
adminServicesProviderPhpFileContents = f"""
<?php
defined('_JEXEC') or die;

use Joomla\CMS\Dispatcher\ComponentDispatcherFactoryInterface;
use Joomla\CMS\Extension\ComponentInterface;
use Joomla\CMS\Extension\MVCComponent;
use Joomla\CMS\Extension\Service\Provider\ComponentDispatcherFactory;
use Joomla\CMS\Extension\Service\Provider\MVCFactory;
use Joomla\CMS\MVC\Factory\MVCFactoryInterface;
use Joomla\DI\Container;
use Joomla\DI\ServiceProviderInterface;

return new class implements ServiceProviderInterface {{
    public function register(Container $container): void {{
        $container->registerServiceProvider(new MVCFactory('\\\{vendorName}\\\Component\\\{comNameInNamespaces}'));
        $container->registerServiceProvider(new ComponentDispatcherFactory('\\\{vendorName}\\\Component\\\{comNameInNamespaces}'));
        $container->set(
            ComponentInterface::class,
            function (Container $container) {{
                $component = new MVCComponent($container->get(ComponentDispatcherFactoryInterface::class));
                $component->setMVCFactory($container->get(MVCFactoryInterface::class));

                return $component;
            }}
        );
    }}
}};
"""[1:]
##################################### END Admin services provider.php ####################################
createFile(assetType = "f", targetPath = adminServicesProviderPhpFile, fileContents = adminServicesProviderPhpFileContents)


##########################################################################################################
############################################ START i8n setup #############################################
##########################################################################################################

adminLanguageLangLocalCodeIniFile = f"{adminFolder}/language/{langLocaleCode}/{langLocaleCode}.{comFolderName}.ini"
#################################### START Admin i8n language strings ###################################
adminLanguageLangLocalCodeIniFileContents = f"""
; {comName} Admin Strings
; Copyright (C)  {comCreationYear} {comCopyRightHolder}. All Rights Reserved.

COM_HELLOWORLD_MSG_HELLO_WORLD="Hello World (i8n translation string)!"
"""[1:]
##################################### END Admin i8n language strings ####################################
createFile(assetType = "f", targetPath = adminLanguageLangLocalCodeIniFile, fileContents = adminLanguageLangLocalCodeIniFileContents)


adminLanguageLangLocalCodeSysIniFile = f"{adminFolder}/language/{langLocaleCode}/{langLocaleCode}.{comFolderName}.sys.ini"
#################################### START Admin i8n language strings ###################################
adminLanguageLangLocalCodeSysIniFileContents = f"""
; {comName} Sys.ini Strings
; Copyright (C)  {comCreationYear} {comCopyRightHolder}. All Rights Reserved.

COM_HELLOWORLD_MENU_HELLO_WORLD_TITLE="Hello World (i8n translation string)!"
COM_HELLOWORLD_MENU_HELLO_WORLD_DESC="My first Joomla! page"
"""[1:]
##################################### END Admin i8n language strings ####################################
createFile(assetType = "f", targetPath = adminLanguageLangLocalCodeSysIniFile, fileContents = adminLanguageLangLocalCodeSysIniFileContents)


siteLanguageLangLocalCodeIniFile = f"{siteFolder}/language/{langLocaleCode}/{langLocaleCode}.{comFolderName}.ini"
#################################### START site i8n language strings ###################################
siteLanguageLangLocalCodeIniFileContents = f"""
; {comName} site Strings
; Copyright (C)  {comCreationYear} {comCopyRightHolder}. All Rights Reserved.

COM_HELLOWORLD_MSG_HELLO_WORLD="Hello World (i8n translation string)!"
COM_HELLOWORLD_MSG_GREETING="This message is coming from the item model!"
"""[1:]
##################################### END site i8n language strings ####################################
createFile(assetType = "f", targetPath = siteLanguageLangLocalCodeIniFile, fileContents = siteLanguageLangLocalCodeIniFileContents)
##########################################################################################################
############################################# END i8n setup ##############################################
##########################################################################################################




##########################################################################################################
############################################ START ADMIN SIDE ############################################
##########################################################################################################


# Create the first admin display controller
adminSrcControllerDisplayControllerPhpFile = f"{adminFolder}/src/Controller/DisplayController.php"
#################################### START Admin src/Controller/DisplayController.php ###################################
adminSrcControllerDisplayControllerPhpFileContents = f"""
<?php
namespace {vendorName}\Component\{comNameInNamespaces}\Administrator\Controller;
defined('_JEXEC') or die;

use Joomla\CMS\MVC\Controller\BaseController;

/**
 * @package     Joomla.Administrator
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C)  {comCreationYear} {comLicenseType} All rights reserved.
 */

/**
 * Default Controller of {comNameInNamespaces} component
 *
 * @package     Joomla.Administrator
 * @subpackage  {comFolderName}
 */
class DisplayController extends BaseController {{
    /**
     * The default view for the display method.
     *
     * @var string
     */
    protected $default_view = '{initialViewNameLower}';

    public function display($cachable = false, $urlparams = array()) {{
        return parent::display($cachable, $urlparams);

        /* TODO: Configure admin displaycontroller to use this message model.
        $document = Factory::getDocument();
        $viewName = $this->input->getCmd('view', 'login');
        $viewFormat = $document->getType();

        $view = $this->getView($viewName, $viewFormat);
        $view->setModel($this->getModel('Message'), true);

        $view->document = $document;
        $view->display();
        */
    }}

}}
"""[1:]
##################################### END Admin src/Controller/DisplayController.php ####################################
createFile(assetType = "f", targetPath = adminSrcControllerDisplayControllerPhpFile, fileContents = adminSrcControllerDisplayControllerPhpFileContents)


# Create the intial admin view (the name is set at beginning of file in global variables)
adminSrcViewInitialHtmlViewPhpFile = f"{adminFolder}/src/View/{initialViewName}/HtmlView.php"
#################################### START Admin src/View/<initialViewName>/HtmlView.php ###################################
adminSrcViewInitialHtmlViewPhpFileContents = f"""
<?php
namespace {vendorName}\Component\{comNameInNamespaces}\Administrator\View\{initialViewName};

defined('_JEXEC') or die;

use Joomla\CMS\MVC\View\HtmlView as BaseHtmlView;

/**
 * @package     Joomla.Administrator
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C)  {comCreationYear} {comLicenseType} All rights reserved.
 */

/**
 * Main "{comName}" Admin View
 */
class HtmlView extends BaseHtmlView {{

    /**
     * Display the main "{comName}" view, here called {initialViewName}
     *
     * @param   string  $tpl  The name of the template file to parse; automatically searches through the template paths.
     * @return  void
     */
    function display($tpl = null) {{
        parent::display($tpl);
    }}

}}
"""[1:]
##################################### END Admin src/View/<initialViewName>/HtmlView.php ####################################
createFile(assetType = "f", targetPath = adminSrcViewInitialHtmlViewPhpFile, fileContents = adminSrcViewInitialHtmlViewPhpFileContents)


# Create the initial admin view's template
adminTmplInitialViewTemplatePhpFile = f"{adminFolder}/tmpl/{initialViewNameLower}/default.php"
#################################### START Admin tmpl/<initialViewNameLower>/default.php ###################################
adminTmplInitialViewTemplatePhpFileContents = f"""
<?php

use Joomla\CMS\Language\Text;

/**
 * @package     Joomla.Administrator
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C)  {comCreationYear} {comLicenseType} All rights reserved.
 */

 // No direct access to this file
defined('_JEXEC') or die('Restricted Access');
?>
<!-- <h2><?= Text::_('COM_HELLOWORLD_MSG_HELLO_WORLD') ?></h2> -->
<h2>Hello world!</h2>
<h4>This is the initial admin view.</h4>
"""[1:]
# <p><?= $this->getModel()->getItem()->message; ?></p>
##################################### END Admin tmpl/<initialViewNameLower>/default.php ####################################
createFile(assetType = "f", targetPath = adminTmplInitialViewTemplatePhpFile, fileContents = adminTmplInitialViewTemplatePhpFileContents)


# Create the first admin model
adminSrcModelMessageModelPhpFile = f"{adminFolder}/src/Model/MessageModel.php"
#################################### START Admin src/Model/MessageModel.php ###################################
adminSrcModelMessageModelPhpFileContents = f"""
<?php
namespace {vendorName}\Component\{comNameInNamespaces}\Administrator\Model;
defined('_JEXEC') or die;

/* List of availabel model classes
use Joomla\CMS\MVC\Model\AdminModel
use Joomla\CMS\MVC\Model\BaseModel
use Joomla\CMS\MVC\Model\FormModel
use Joomla\CMS\MVC\Model\ItemModel
use Joomla\CMS\MVC\Model\ListModel
*/

use Joomla\CMS\MVC\Model\ItemModel;
use Joomla\CMS\Language\Text;

/**
 * @package     Joomla.Administrator
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C) {comLicenseType} All rights reserved.
 */

/**
 * Hello World Message Model
 * @since 0.0.1
 */
class MessageModel extends ItemModel {{

    /**
     * Returns a message for display
     * @param integer $pk Primary key of the "message item", currently unused
     * @return object Message object
     */
    public function getItem($pk= null): object {{
        $item = new \stdClass();
        $item->message = "A message from the admin message model";
        /* $item->message = Text::_('COM_HELLOWORLD_MSG_GREETING'); */
        return $item;
    }}

}}
"""[1:]
##################################### END Admin src/Controller/DisplayController.php ####################################
createFile(assetType = "f", targetPath = adminSrcModelMessageModelPhpFile, fileContents = adminSrcModelMessageModelPhpFileContents)


##########################################################################################################
############################################# END ADMIN SIDE #############################################
##########################################################################################################


##########################################################################################################
############################################ START SITE SIDE #############################################
##########################################################################################################


# Create the Initial site display controller
siteSrcControllerDisplayControllerPhpFile = f"{siteFolder}/src/Controller/DisplayController.php"
#################################### START Site src/Controller/DisplayController.php ###################################
siteSrcControllerDisplayControllerPhpFileContents = f"""
<?php
namespace {vendorName}\Component\{comNameInNamespaces}\Site\Controller;
defined('_JEXEC') or die;

use Joomla\CMS\MVC\Controller\BaseController;
use Joomla\CMS\Factory;

/**
 * @package     Joomla.Site
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C)  {comCreationYear} {comLicenseType} All rights reserved.
 */

/**
 * {comNameInNamespaces} Component Controller
 * @since  {comVersion}
 */
class DisplayController extends BaseController {{

    public function display($cachable = false, $urlparams = array()) {{
        $document = Factory::getDocument();
        $viewName = $this->input->getCmd('view', 'login');
        $viewFormat = $document->getType();

        $view = $this->getView($viewName, $viewFormat);
        $view->setModel($this->getModel('Message'), true);

        $view->document = $document;
        $view->display();
    }}

}}
"""[1:]
##################################### END Site src/Controller/DisplayController.php ####################################
createFile(assetType = "f", targetPath = siteSrcControllerDisplayControllerPhpFile, fileContents = siteSrcControllerDisplayControllerPhpFileContents)


# Create the Initial site view
siteSrcViewInitialHtmlViewPhpFile = f"{siteFolder}/src/View/{initialViewName}/HtmlView.php"
#################################### START Site src/Controller/DisplayController.php ###################################
siteSrcViewInitialHtmlViewPhpFileContents = f"""
<?php
namespace {vendorName}\Component\{comNameInNamespaces}\Site\View\{initialViewName};
defined('_JEXEC') or die;

use Joomla\CMS\MVC\View\HtmlView as BaseHtmlView;

/**
 * @package     Joomla.Site
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C)  {comCreationYear} {comLicenseType} All rights reserved.
 */

/**
 * View for the user identity validation form
 */
class HtmlView extends BaseHtmlView {{


    /**
     * Display the view
     *
     * @param   string  $template  The name of the layout file to parse.
     * @return  void
     */
    public function display($template = null) {{
        // Call the parent display to display the layout file
        parent::display($template);
    }}

}}
"""[1:]
##################################### END Site src/Controller/DisplayController.php ####################################
createFile(assetType = "f", targetPath = siteSrcViewInitialHtmlViewPhpFile, fileContents = siteSrcViewInitialHtmlViewPhpFileContents)


# Create the initial site view's template
siteTmplInitialViewTemplatePhpFile = f"{siteFolder}/tmpl/{initialViewNameLower}/default.php"
#################################### START Site tmpl/<initialViewNameLower>/default.php ###################################
siteTmplInitialViewTemplatePhpFileContents = f"""
<?php

use Joomla\CMS\Language\Text;

/**
 * @package     Joomla.Administrator
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C)  {comLicenseType} All rights reserved.
 */

 // No direct access to this file
defined('_JEXEC') or die('Restricted Access');
?>
<!-- <h2><?= Text::_('COM_HELLOWORLD_MSG_HELLO_WORLD') ?></h2> -->
<h2>Hello world!</h2>
<h4>This is the initial site view.</h4>
<p><?= $this->getModel()->getItem()->message; ?></p>
"""[1:]
##################################### END Site tmpl/<initialViewNameLower>/default.php ####################################
createFile(assetType = "f", targetPath = siteTmplInitialViewTemplatePhpFile, fileContents = siteTmplInitialViewTemplatePhpFileContents)


# Create the first site model
siteSrcModelMessageModelPhpFile = f"{siteFolder}/src/Model/MessageModel.php"
#################################### START Site src/Model/MessageModel.php ###################################
siteSrcModelMessageModelPhpFileContents = f"""
<?php
namespace {vendorName}\Component\{comNameInNamespaces}\Site\Model;
defined('_JEXEC') or die;

/* List of availabel model classes
use Joomla\CMS\MVC\Model\BaseModel
use Joomla\CMS\MVC\Model\FormModel
use Joomla\CMS\MVC\Model\ItemModel
use Joomla\CMS\MVC\Model\ListModel
*/


use Joomla\CMS\MVC\Model\ItemModel;
use Joomla\CMS\Language\Text;

/**
 * @package     Joomla.Administrator
 * @subpackage  {comFolderName}
 *
 * @copyright   {comCopyRightHolder}
 * @license     Copyright (C) {comLicenseType} All rights reserved.
 */

/**
 * Hello World Message Model
 * @since 0.0.1
 */
class MessageModel extends ItemModel {{

    /**
     * Returns a message for display
     * @param integer $pk Primary key of the "message item", currently unused
     * @return object Message object
     */
    public function getItem($pk= null): object {{
        $item = new \stdClass();
        $item->message = "A message from the site message model";
        /* $item->message = Text::_('COM_HELLOWORLD_MSG_GREETING'); */
        return $item;
    }}

}}
"""[1:]
##################################### END Site src/Controller/DisplayController.php ####################################
createFile(assetType = "f", targetPath = siteSrcModelMessageModelPhpFile, fileContents = siteSrcModelMessageModelPhpFileContents)


# Create the initial site view's menu item xml file
siteTmplInitialViewTemplateXmlFile = f"{siteFolder}/tmpl/{initialViewNameLower}/default.xml"
#################################### START Site tmpl/<initialViewNameLower>/default.xml ###################################
siteTmplInitialViewTemplateXmlFileContents = f"""
<?xml version="1.0" encoding="utf-8"?>
<metadata>
    <!-- <layout title="COM_HELLOWORLD_MENU_HELLO_WORLD_TITLE">
        <message><![CDATA[COM_HELLOWORLD_MENU_HELLO_WORLD_DESC]]></message>
    </layout> -->

    <layout title="{initialViewMenuItemTitle}">
        <message><![CDATA[My first Joomla! page]]></message>
    </layout> 
</metadata>
"""[1:]
##################################### END Site tmpl/<initialViewNameLower>/default.xml ####################################
createFile(assetType = "f", targetPath = siteTmplInitialViewTemplateXmlFile, fileContents = siteTmplInitialViewTemplateXmlFileContents)

##########################################################################################################
############################################# END SITE SIDE ##############################################
##########################################################################################################

































































































############################################################################################################################
##################################################### START SQL Section ####################################################
############################################################################################################################

# Create SQL asset directories
sqlAssetFolder = f"{adminFolder}/sql"
sqlAssetUpdatesFolder = f"{sqlAssetFolder}/updates/mysql"
createFile(assetType = "d", targetPath = sqlAssetFolder)
createFile(assetType = "d", targetPath = sqlAssetUpdatesFolder)


# Create the Install SQL file (only runs upon installation (not updates i.e. install over existing installation))
adminSqlInstallFile = f"{sqlAssetFolder}/{sqlInstallFilename}"
#################################### START Install SQL ###################################
adminSqlInstallFileContents = f"""
DROP TABLE IF EXISTS `#__{comNameJoomla}_{initialTableName}`;

CREATE TABLE `#__{comNameJoomla}_{initialTableName}`(
    `id` SERIAL NOT NULL COMMENT "The auto-increment pk of this i.e. {initialTableName} table",
    `name` VARCHAR(255) NOT NULL COMMENT "Required (can't be null) name field",
    `address` VARCHAR(255) NULL COMMENT "Example 'Address' field of {initialTableName} if no value provided, will be NULL",
    `city` VARCHAR(128) NULL COMMENT "Example 'City' field of {initialTableName} if no value provided, will be NULL",
    `state` VARCHAR(128) NULL COMMENT "Example 'State' field of {initialTableName} if no value provided, will be NULL",
    `zip_postcode` MEDIUMINT NULL COMMENT "Example 'Postal code' field of {initialTableName} if no value provided, will be NULL",
    PRIMARY KEY(`id`)
) ENGINE = InnoDB;

/* Testing insertion into our newly created table */
INSERT INTO `#__{comNameJoomla}_{initialTableName}` (`name`) VALUES
    ("Example.com"),
    ("Foo Bar Bat");
"""[1:]
##################################### END Install SQL ####################################
createFile(assetType = "f", targetPath = adminSqlInstallFile, fileContents = adminSqlInstallFileContents)


# Create the Uninstall SQL file (only runs upon Uninstallation (not updates i.e. Install over existing innstallation))
adminSqlUninstallFile = f"{sqlAssetFolder}/{sqlUninstallFilename}"
#################################### START Uninstall SQL ###################################
adminSqlUninstallFileContents = f"""
DROP TABLE IF EXISTS `#__{comNameJoomla}_{initialTableName}`;

"""[1:]
##################################### END Uninstall SQL ####################################
createFile(assetType = "f", targetPath = adminSqlUninstallFile, fileContents = adminSqlUninstallFileContents)



# Create the Update SQL file (only runs upon update (An update is an install over existing innstallation))
adminSqlUpdateFile = f"{sqlAssetUpdatesFolder}/{sqlUpdateFilename}"
#################################### START Update SQL ###################################
adminSqlUpdateFileContents = f"""
ALTER TABLE `#__{comNameJoomla}_{initialTableName}` ADD `new_field_from_update` TEXT NULL DEFAULT NULL AFTER `zip_postcode`,
ADD FULLTEXT `idx_new_field_from_update` (`new_field_from_update`);
"""[1:]
##################################### END Update SQL ####################################
createFile(assetType = "f", targetPath = adminSqlUpdateFile, fileContents = adminSqlUpdateFileContents)

# # Create the Update SQL file (only runs upon Update (not Installs i.e. Installs over existing installation))
# adminSqlUpdateFile = f"{sqlAssetUpdatesFolder}/{comVersion}.sql"
# #################################### START Update SQL ###################################
# adminSqlUpdateFileContents = f"""
# """[1:]
# ##################################### END Update SQL ####################################
# createFile(assetType = "f", targetPath = adminSqlUpdateFile, fileContents = adminSqlUpdateFileContents)

############################################################################################################################
###################################################### END SQL Section #####################################################
############################################################################################################################




























# # Create the first admin display controller
# admin__PhpFile = f"{adminFolder}/.php"
# #################################### START Admin services provider.php ###################################
# admin__PhpFileContents = f"""
# """
# ##################################### END Admin services provider.php ####################################
# createFile(assetType = "f", targetPath = admin__PhpFile, fileContents = admin__PhpFileContents)

def finishAndCreateInstallable():
  # Recap the structure of created assets.
  dirStructCreated = sh.tree(comPackageBaseFolder)
  print(dirStructCreated)

  # Create the installable package
  sh.zip( "-r", f"{comFolderName}.zip", f"{comFolderName}" )

finishAndCreateInstallable()

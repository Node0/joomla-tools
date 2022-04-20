#!/usr/bin/env python3

# You'll need the sh library for this script to function properly.
# pip3 install sh
import os, sh, argparse

class ComponentMaker:
  def __init__(self):
    parser = argparse.ArgumentParser(
    description='Customize your J! 4 Component scaffold.',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    allow_abbrev=False,
    epilog="""Please Note:
This script requires python3.6 or later and also requires the sh library.
You may install the sh library via: pip3 install sh

Usage Example in Bash/sh/zsh:
./componentMaker.py \\
  --component-name="Generic Hello World" \\
  --component-desc="A generic hello world component for J! 4" \\
  --vendor-name="joomlaology" \\
  --author-name="Joe Hacobian" \\
  --author-url="https://algorithme.us" \\
  --copyright-holder="Joe Hacobian" \\
  --creation-month="April" \\
  --creation-year="2022" \\
  --component-version="0.0.1"

  From there, test your component scaffold by installing the zip file into Joomla.
  You may then copy the generated folder into your git repo and begin development.""")

    parser.add_argument('--component-name', required=True, help="""The Component's name""")
    parser.add_argument('--component-desc', required=True, help="""The Component's description""")
    parser.add_argument('--vendor-name',    required=True, help="""The vendor name used in configuring namespaces, typically your org or author's name""")
    parser.add_argument('--author-name',      required=True, help="""The code author's name""")
    parser.add_argument('--author-url',       required=True, help="""The code author's website URL""")
    parser.add_argument('--copyright-holder', required=True, help="""The copyright holder's name""")
    parser.add_argument('--creation-month',   required=True, help="""Month of this component's creation""")
    parser.add_argument('--creation-year',    required=True, help="""Year of this component's creation""")
    parser.add_argument('--license-type',     required=False, help="""OPTIONAL: Your license type, defaults to GPL v2""")
    parser.add_argument('--component-version',required=True, help="""The component's version string""")
    parser.add_argument('--initial-view-name',required=False, help="""OPTIONAL: Set the name of the initial view. Defaults to Main""")
    # The following commented out declarations are for illustration purposes.
    # parser.add_argument('-a', '--author-name',      required=True, help="""The code author's name""")
    # positional arg declaration parser.add_argument('foo', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    self.args = parser.parse_args()

    # Basic component creation directory location and permissions
    self.currDir = sh.pwd().strip()
    self.folderPermissions = "0755"
    self.filePermissions = "0644"

    # Component specific global details
    self.comName = self.args.component_name
    self.comDesc = self.args.component_desc
    self.comNameJoomla = self.comName.lower().replace(" ","")
    self.comNameInNamespaces = self.comName.replace(" ","")

    # This pertains to the php namespace configuration
    self.vendorName = self.args.vendor_name

    self.comAuthor = self.args.author_name
    self.comAuthorUrl = self.args.author_url
    self.comCopyRightHolder = self.args.copyright_holder
    self.comCreationMonth = self.args.creation_month
    self.comCreationYear = self.args.creation_year
    self.comCreationMonthAndYear = f"{self.comCreationMonth} {self.comCreationYear}"

    # If a custom license type is specified, use it, else GPL v2
    self.comLicenseType = self.args.license_type if self.args.license_type != None else "GPL v2"


    self.comVersion = self.args.component_version

    # Initial language locale to setup
    self.langLocaleCode = "en-GB"

    # SQL Filenames
    self.sqlInstallFilename = f"install.mysql.utf8.sql"
    self.sqlUninstallFilename = f"uninstall.mysql.utf8.sql"
    self.sqlUpdateFilename = f"{self.comVersion}.sql"
    # This is simply the first table's name for illustrative purposes
    self.initialTableName = f"storage_table_1"

    # If a custom initial view name is specified, use it, else use "Main"
    self.initialViewName = self.args.initial_view_name if self.args.initial_view_name != None else "Main"

    self.initialViewNameLower = f"{self.initialViewName.lower()}"
    self.initialViewMenuItemTitle = f"Menu Item for {self.initialViewName} view"


    # Form the base component package folder name and create the folder
    # within the current directory (where the executing python file resides)
    self.comFolderName = f"com_{self.comNameJoomla}"
    self.comPackageBaseFolder = f"{self.currDir}/{self.comFolderName}"

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

  def setupSiteAndAdminFolders(self):
    # Create the site and admin subfolders inside the component base folder
    self.siteFolder  = f"{self.comPackageBaseFolder}/site"
    self.adminFolder = f"{self.comPackageBaseFolder}/admin"
    self.apiFolder   = f"{self.comPackageBaseFolder}/api/src/"
    self.apiViewFolder = f"{self.apiFolder}/view"
    self.apiControllerFolder = f"{self.apiFolder}/controller"

    self.createFile(assetType = "d", targetPath = self.siteFolder)
    self.createFile(assetType = "d", targetPath = self.adminFolder)
    self.createFile(assetType = "d", targetPath = self.apiViewFolder)
    self.createFile(assetType = "d", targetPath = self.apiControllerFolder)

  def setupComponentManifestFile(self):
    # Create the component manifest xml file container
    componentManifestFile = f"{self.comPackageBaseFolder}/{self.comNameJoomla}.xml"
    #componentManifestFile = f"{self.comPackageBaseFolder}/manifest.xml"
    ##########################################################################################################
    ##########################################################################################################
    ###################################### START Component Manifest XML ######################################
    ##########################################################################################################
    ##########################################################################################################
    componentManifestContents = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <extension type="component" method="upgrade">
    <!-- 'version' attribute for extension tag is no longer used -->

        <name>{self.comName}</name>
        <creationDate>{self.comCreationMonthAndYear}</creationDate>
        <author>{self.comAuthor}</author>
        <authorUrl>{self.comAuthorUrl}</authorUrl>
        <copyright>{self.comCopyRightHolder}</copyright>
        <license>{self.comLicenseType}</license>
        <version>{self.comVersion}</version>
        <description>
            {self.comDesc}
        </description>

        <!-- This is the PHP namespace under which the extension's
        code is organised. It should follow this format:

        {self.vendorName}\Component\{self.comNameJoomla}

        "Vendor" can be your company or your own name

        The "ComponentName" section MUST match the name used
        everywhere else for your component. Whatever the name of
        this XML file is, the namespace must match (ignoring CamelCase).
        -->
        <namespace path="src">{self.vendorName}\Component\{self.comNameInNamespaces}</namespace>

        <files folder="site/">
            <folder>language</folder>
            <folder>src</folder>
            <folder>tmpl</folder>
        </files>

        <languages>
            <language tag="{self.langLocaleCode}">site/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.comFolderName}.ini</language>
        </languages>

        <administration>
            <!-- The link that will appear in the Admin panel's "Components" menu -->
            <!-- NOTE: If we are only going to have a single menu item (under the components menu) appear
                      then the following element is sufficient:
                      <menu link="index.php?option={self.comFolderName}">{self.comName}</menu>
                      pay attention to the link url i.e. index.php?option={self.comFolderName} etc...
                      this structure is changed if we wish to show an expanded submenu underneath the
                      app's menu item (the app here being the component we're developing) then we'll need to
                      use a slightly different menu and submenu element structure as well as removing the index.php?
                      from the link attribute.
                      In all cases any use of query string parameters in the route requires ampersands to be specified as follows:
                      <menu link="option={self.comFolderName}&amp;view=<name_of_view>">Menu Item Title</menu>
                      See below for the actively used submenu implementation example.
                      -->
            <menu>{self.comName}</menu>
            <submenu>
              <menu link="option={self.comFolderName}">Dashboard</menu>
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
                <language tag="{self.langLocaleCode}">admin/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.comFolderName}.ini</language>
                <language tag="{self.langLocaleCode}">admin/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.comFolderName}.sys.ini</language>
            </languages>
        </administration>

        <api>
          <files folder="api">
            <folder>src</folder>
          </files>
        </api>

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
        </update>

    </extension>
    """[5:]
    ##########################################################################################################
    ##########################################################################################################
    ####################################### END Component Manifest XML #######################################
    ##########################################################################################################
    ##########################################################################################################
    self.createFile(assetType = "f", targetPath = componentManifestFile, fileContents = componentManifestContents)

  def setupAdminServicesProviderPhpFile(self):
    ################################### Create admin services provider.php ###################################
    adminServicesProviderPhpFile = f"{self.adminFolder}/services/provider.php"
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
            $container->registerServiceProvider(new MVCFactory('\\\{self.vendorName}\\\Component\\\{self.comNameInNamespaces}'));
            $container->registerServiceProvider(new ComponentDispatcherFactory('\\\{self.vendorName}\\\Component\\\{self.comNameInNamespaces}'));
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
    """[5:]
    ##################################### END Admin services provider.php ####################################
    self.createFile(assetType = "f", targetPath = adminServicesProviderPhpFile, fileContents = adminServicesProviderPhpFileContents)

  ##########################################################################################################
  ############################################ START i8n setup #############################################
  ##########################################################################################################

  def setupAdminLanguageLangLocalCodeIniFile(self):
    adminLanguageLangLocalCodeIniFile = f"{self.adminFolder}/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.comFolderName}.ini"
    #################################### START Admin i8n language strings ###################################
    adminLanguageLangLocalCodeIniFileContents = f"""
    ; {self.comName} Admin Strings
    ; Copyright (C)  {self.comCreationYear} {self.comCopyRightHolder}. All Rights Reserved.

    COM_HELLOWORLD_MSG_HELLO_WORLD="Hello World (i8n translation string)!"
    """[5:]
    ##################################### END Admin i8n language strings ####################################
    self.createFile(assetType = "f", targetPath = adminLanguageLangLocalCodeIniFile, fileContents = adminLanguageLangLocalCodeIniFileContents)

  def setupAdminLanguageLangLocalCodeSysIniFile(self):
    adminLanguageLangLocalCodeSysIniFile = f"{self.adminFolder}/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.comFolderName}.sys.ini"
    #################################### START Admin i8n language strings ###################################
    adminLanguageLangLocalCodeSysIniFileContents = f"""
    ; {self.comName} Sys.ini Strings
    ; Copyright (C)  {self.comCreationYear} {self.comCopyRightHolder}. All Rights Reserved.

    COM_HELLOWORLD_MENU_HELLO_WORLD_TITLE="Hello World (i8n translation string)!"
    COM_HELLOWORLD_MENU_HELLO_WORLD_DESC="My first Joomla! page"
    """[5:]
    ##################################### END Admin i8n language strings ####################################
    self.createFile(assetType = "f", targetPath = adminLanguageLangLocalCodeSysIniFile, fileContents = adminLanguageLangLocalCodeSysIniFileContents)

  def setupSiteLanguageLangLocalCodeIniFile(self):
    siteLanguageLangLocalCodeIniFile = f"{self.siteFolder}/language/{self.langLocaleCode}/{self.langLocaleCode}.{self.comFolderName}.ini"
    #################################### START site i8n language strings ###################################
    siteLanguageLangLocalCodeIniFileContents = f"""
    ; {self.comName} site Strings
    ; Copyright (C)  {self.comCreationYear} {self.comCopyRightHolder}. All Rights Reserved.

    COM_HELLOWORLD_MSG_HELLO_WORLD="Hello World (i8n translation string)!"
    COM_HELLOWORLD_MSG_GREETING="This message is coming from the item model!"
    """[5:]
    ##################################### END site i8n language strings ####################################
    self.createFile(assetType = "f", targetPath = siteLanguageLangLocalCodeIniFile, fileContents = siteLanguageLangLocalCodeIniFileContents)

  ##########################################################################################################
  ############################################# END i8n setup ##############################################
  ##########################################################################################################




  ##########################################################################################################
  ############################################ START ADMIN SIDE ############################################
  ##########################################################################################################

  def setupAdminSrcControllerDisplayControllerPhpFile(self):
    # Create the first admin display controller
    adminSrcControllerDisplayControllerPhpFile = f"{self.adminFolder}/src/Controller/DisplayController.php"
    #################################### START Admin src/Controller/DisplayController.php ###################################
    adminSrcControllerDisplayControllerPhpFileContents = f"""
    <?php
    namespace {self.vendorName}\Component\{self.comNameInNamespaces}\Administrator\Controller;
    defined('_JEXEC') or die;

    use Joomla\CMS\MVC\Controller\BaseController;

    /**
    * @package     Joomla.Administrator
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C)  {self.comCreationYear} {self.comLicenseType} All rights reserved.
    */

    /**
    * Default Controller of {self.comNameInNamespaces} component
    *
    * @package     Joomla.Administrator
    * @subpackage  {self.comFolderName}
    */
    class DisplayController extends BaseController {{
        /**
        * The default view for the display method.
        *
        * @var string
        */
        protected $default_view = '{self.initialViewNameLower}';

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
    """[5:]
    ##################################### END Admin src/Controller/DisplayController.php ####################################
    self.createFile(assetType = "f", targetPath = adminSrcControllerDisplayControllerPhpFile, fileContents = adminSrcControllerDisplayControllerPhpFileContents)

  def setupAdminSrcViewInitialHtmlViewPhpFile(self):
    # Create the intial admin view (the name is set at beginning of file in global variables)
    adminSrcViewInitialHtmlViewPhpFile = f"{self.adminFolder}/src/View/{self.initialViewName}/HtmlView.php"
    #################################### START Admin src/View/<self.initialViewName>/HtmlView.php ###################################
    adminSrcViewInitialHtmlViewPhpFileContents = f"""
    <?php
    namespace {self.vendorName}\Component\{self.comNameInNamespaces}\Administrator\View\{self.initialViewName};

    defined('_JEXEC') or die;

    use Joomla\CMS\MVC\View\HtmlView as BaseHtmlView;

    /**
    * @package     Joomla.Administrator
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C)  {self.comCreationYear} {self.comLicenseType} All rights reserved.
    */

    /**
    * Main "{self.comName}" Admin View
    */
    class HtmlView extends BaseHtmlView {{

        /**
        * Display the main "{self.comName}" view, here called {self.initialViewName}
        *
        * @param   string  $tpl  The name of the template file to parse; automatically searches through the template paths.
        * @return  void
        */
        function display($tpl = null) {{
            parent::display($tpl);
        }}

    }}
    """[5:]
    ##################################### END Admin src/View/<self.initialViewName>/HtmlView.php ####################################
    self.createFile(assetType = "f", targetPath = adminSrcViewInitialHtmlViewPhpFile, fileContents = adminSrcViewInitialHtmlViewPhpFileContents)

  def setupAdminTmplInitialViewTemplatePhpFile(self):
    # Create the initial admin view's template
    adminTmplInitialViewTemplatePhpFile = f"{self.adminFolder}/tmpl/{self.initialViewNameLower}/default.php"
    #################################### START Admin tmpl/<self.initialViewNameLower>/default.php ###################################
    adminTmplInitialViewTemplatePhpFileContents = f"""
    <?php

    use Joomla\CMS\Language\Text;

    /**
    * @package     Joomla.Administrator
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C)  {self.comCreationYear} {self.comLicenseType} All rights reserved.
    */

    // No direct access to this file
    defined('_JEXEC') or die('Restricted Access');
    ?>
    <!-- <h2><?= Text::_('COM_HELLOWORLD_MSG_HELLO_WORLD') ?></h2> -->
    <h2>Hello world!</h2>
    <h4>This is the initial admin view.</h4>
    """[5:]
    # <p><?= $this->getModel()->getItem()->message; ?></p>
    ##################################### END Admin tmpl/<self.initialViewNameLower>/default.php ####################################
    self.createFile(assetType = "f", targetPath = adminTmplInitialViewTemplatePhpFile, fileContents = adminTmplInitialViewTemplatePhpFileContents)

  def setupAdminSrcModelMessageModelPhpFile(self):
    # Create the first admin model
    adminSrcModelMessageModelPhpFile = f"{self.adminFolder}/src/Model/MessageModel.php"
    #################################### START Admin src/Model/MessageModel.php ###################################
    adminSrcModelMessageModelPhpFileContents = f"""
    <?php
    namespace {self.vendorName}\Component\{self.comNameInNamespaces}\Administrator\Model;
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
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C) {self.comLicenseType} All rights reserved.
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
    """[5:]
    ##################################### END Admin src/Controller/DisplayController.php ####################################
    self.createFile(assetType = "f", targetPath = adminSrcModelMessageModelPhpFile, fileContents = adminSrcModelMessageModelPhpFileContents)

  ##########################################################################################################
  ############################################# END ADMIN SIDE #############################################
  ##########################################################################################################


  ##########################################################################################################
  ############################################ START SITE SIDE #############################################
  ##########################################################################################################

  def setupSiteSrcControllerDisplayControllerPhpFile(self):
    # Create the Initial site display controller
    siteSrcControllerDisplayControllerPhpFile = f"{self.siteFolder}/src/Controller/DisplayController.php"
    #################################### START Site src/Controller/DisplayController.php ###################################
    siteSrcControllerDisplayControllerPhpFileContents = f"""
    <?php
    namespace {self.vendorName}\Component\{self.comNameInNamespaces}\Site\Controller;
    defined('_JEXEC') or die;

    use Joomla\CMS\MVC\Controller\BaseController;
    use Joomla\CMS\Factory;

    /**
    * @package     Joomla.Site
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C)  {self.comCreationYear} {self.comLicenseType} All rights reserved.
    */

    /**
    * {self.comNameInNamespaces} Component Controller
    * @since  {self.comVersion}
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
    """[5:]
    ##################################### END Site src/Controller/DisplayController.php ####################################
    self.createFile(assetType = "f", targetPath = siteSrcControllerDisplayControllerPhpFile, fileContents = siteSrcControllerDisplayControllerPhpFileContents)

  def setupSiteSrcViewInitialHtmlViewPhpFile(self):
    # Create the Initial site view
    siteSrcViewInitialHtmlViewPhpFile = f"{self.siteFolder}/src/View/{self.initialViewName}/HtmlView.php"
    #################################### START Site src/Controller/DisplayController.php ###################################
    siteSrcViewInitialHtmlViewPhpFileContents = f"""
    <?php
    namespace {self.vendorName}\Component\{self.comNameInNamespaces}\Site\View\{self.initialViewName};
    defined('_JEXEC') or die;

    use Joomla\CMS\MVC\View\HtmlView as BaseHtmlView;

    /**
    * @package     Joomla.Site
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C)  {self.comCreationYear} {self.comLicenseType} All rights reserved.
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
    """[5:]
    ##################################### END Site src/Controller/DisplayController.php ####################################
    self.createFile(assetType = "f", targetPath = siteSrcViewInitialHtmlViewPhpFile, fileContents = siteSrcViewInitialHtmlViewPhpFileContents)

  def setupSiteTmplInitialViewTemplatePhpFile(self):
    # Create the initial site view's template
    siteTmplInitialViewTemplatePhpFile = f"{self.siteFolder}/tmpl/{self.initialViewNameLower}/default.php"
    #################################### START Site tmpl/<self.initialViewNameLower>/default.php ###################################
    siteTmplInitialViewTemplatePhpFileContents = f"""
    <?php

    use Joomla\CMS\Language\Text;

    /**
    * @package     Joomla.Administrator
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C)  {self.comLicenseType} All rights reserved.
    */

    // No direct access to this file
    defined('_JEXEC') or die('Restricted Access');
    ?>
    <!-- <h2><?= Text::_('COM_HELLOWORLD_MSG_HELLO_WORLD') ?></h2> -->
    <h2>Hello world!</h2>
    <h4>This is the initial site view.</h4>
    <p><?= $this->getModel()->getItem()->message; ?></p>
    """[5:]
    ##################################### END Site tmpl/<self.initialViewNameLower>/default.php ####################################
    self.createFile(assetType = "f", targetPath = siteTmplInitialViewTemplatePhpFile, fileContents = siteTmplInitialViewTemplatePhpFileContents)

  def setupSiteSrcModelMessageModelPhpFile(self):
    # Create the first site model
    siteSrcModelMessageModelPhpFile = f"{self.siteFolder}/src/Model/MessageModel.php"
    #################################### START Site src/Model/MessageModel.php ###################################
    siteSrcModelMessageModelPhpFileContents = f"""
    <?php
    namespace {self.vendorName}\Component\{self.comNameInNamespaces}\Site\Model;
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
    * @subpackage  {self.comFolderName}
    *
    * @copyright   {self.comCopyRightHolder}
    * @license     Copyright (C) {self.comLicenseType} All rights reserved.
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
    """[5:]
    ##################################### END Site src/Controller/DisplayController.php ####################################
    self.createFile(assetType = "f", targetPath = siteSrcModelMessageModelPhpFile, fileContents = siteSrcModelMessageModelPhpFileContents)

  def setupSiteTmplInitialViewTemplateXmlFile(self):
    # Create the initial site view's menu item xml file
    siteTmplInitialViewTemplateXmlFile = f"{self.siteFolder}/tmpl/{self.initialViewNameLower}/default.xml"
    #################################### START Site tmpl/<self.initialViewNameLower>/default.xml ###################################
    siteTmplInitialViewTemplateXmlFileContents = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <metadata>
        <!-- <layout title="COM_HELLOWORLD_MENU_HELLO_WORLD_TITLE">
            <message><![CDATA[COM_HELLOWORLD_MENU_HELLO_WORLD_DESC]]></message>
        </layout> -->

        <layout title="{self.initialViewMenuItemTitle}">
            <message><![CDATA[My first Joomla! page]]></message>
        </layout> 
    </metadata>
    """[5:]
    ##################################### END Site tmpl/<self.initialViewNameLower>/default.xml ####################################
    self.createFile(assetType = "f", targetPath = siteTmplInitialViewTemplateXmlFile, fileContents = siteTmplInitialViewTemplateXmlFileContents)

  ##########################################################################################################
  ############################################# END SITE SIDE ##############################################
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
    DROP TABLE IF EXISTS `#__{self.comNameJoomla}_{self.initialTableName}`;

    CREATE TABLE `#__{self.comNameJoomla}_{self.initialTableName}`(
        `id` SERIAL NOT NULL COMMENT "The auto-increment pk of this i.e. {self.initialTableName} table",
        `name` VARCHAR(255) NOT NULL COMMENT "Required (can't be null) name field",
        `address` VARCHAR(255) NULL COMMENT "Example 'Address' field of {self.initialTableName} if no value provided, will be NULL",
        `city` VARCHAR(128) NULL COMMENT "Example 'City' field of {self.initialTableName} if no value provided, will be NULL",
        `state` VARCHAR(128) NULL COMMENT "Example 'State' field of {self.initialTableName} if no value provided, will be NULL",
        `zip_postcode` MEDIUMINT NULL COMMENT "Example 'Postal code' field of {self.initialTableName} if no value provided, will be NULL",
        PRIMARY KEY(`id`)
    ) ENGINE = InnoDB;

    /* Testing insertion into our newly created table */
    INSERT INTO `#__{self.comNameJoomla}_{self.initialTableName}` (`name`) VALUES
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
    DROP TABLE IF EXISTS `#__{self.comNameJoomla}_{self.initialTableName}`;

    """[5:]
    ##################################### END Uninstall SQL ####################################
    self.createFile(assetType = "f", targetPath = adminSqlUninstallFile, fileContents = adminSqlUninstallFileContents)

  def setupAdminSqlUpdateFile(self):
    # Create the Update SQL file (only runs upon update (An update is an install over existing innstallation))
    adminSqlUpdateFile = f"{self.sqlAssetUpdatesFolder}/{self.sqlUpdateFilename}"
    #################################### START Update SQL ###################################
    adminSqlUpdateFileContents = f"""
    ALTER TABLE `#__{self.comNameJoomla}_{self.initialTableName}` ADD `new_field_from_update` TEXT NULL DEFAULT NULL AFTER `zip_postcode`,
    ADD FULLTEXT `idx_new_field_from_update` (`new_field_from_update`);
    """[5:]
    ##################################### END Update SQL ####################################
    self.createFile(assetType = "f", targetPath = adminSqlUpdateFile, fileContents = adminSqlUpdateFileContents)


  # # Create the Update SQL file (only runs upon Update (not Installs i.e. Installs over existing installation))
  # adminSqlUpdateFile = f"{self.sqlAssetUpdatesFolder}/{self.comVersion}.sql"
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
      dirStructCreated = sh.tree( self.comPackageBaseFolder )
      print(dirStructCreated)
    else:
      print("\n\nIf you'd like to see directory tree visualizations (of the generated extension)\nInstall the tree program: yum install tree, or apt-get install tree\n\n")
    
    # Create the installable package
    sh.zip( "-r", f"{self.comFolderName}.zip", f"{self.comFolderName}" )

    print("Generation of extension is finished!")




  def execute(self):
    self.setupSiteAndAdminFolders()
    self.setupComponentManifestFile()
    self.setupAdminServicesProviderPhpFile()
    self.setupAdminLanguageLangLocalCodeIniFile()
    self.setupAdminLanguageLangLocalCodeSysIniFile()
    self.setupSiteLanguageLangLocalCodeIniFile()
    self.setupAdminSrcControllerDisplayControllerPhpFile()
    self.setupAdminSrcViewInitialHtmlViewPhpFile()
    self.setupAdminTmplInitialViewTemplatePhpFile()
    self.setupAdminSrcModelMessageModelPhpFile()
    self.setupSiteSrcControllerDisplayControllerPhpFile()
    self.setupSiteSrcViewInitialHtmlViewPhpFile()
    self.setupSiteTmplInitialViewTemplatePhpFile()
    self.setupSiteSrcModelMessageModelPhpFile()
    self.setupSiteTmplInitialViewTemplateXmlFile()
    self.setupSqlAssetFolder()
    self.setupAdminSqlInstallFile()
    self.setupAdminSqlUninstallFile()
    self.setupAdminSqlUpdateFile()
    self.finishAndCreateInstallable()

CM = ComponentMaker()
CM.execute()

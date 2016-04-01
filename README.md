# Asset IO
Asset IO is a Blender addon that gives an interface to the [Blib&nbsp;library](https://github.com/LucaRood/Blib).

This addon is not supposed to be an advanced asset library manager, but rather a simple import/export interface, to allow preliminary usage of the Blib asset file standard. It is expected that more asset managers in Blender will use the Blib standard in the future, but until then, this simple solution is provided.

For the reasons stated above, this addon's development will be limited to potential bug fixes and minor features at most. On the other hand, the Blib library itself, will see continued development and feature additions.

If you find yourself interested in developing more advanced interfaces using the Blib standard, you may refer to [contributing&nbsp;to&nbsp;Blib](https://github.com/LucaRood/Blib#contributing), for instructions, usage examples, and the full API specification.

**Warning:** The Blib library is currently in beta stage, and thus might contain bugs. Furthermore, breaking changes may occur until the consolidating 1.0.0 release, thus files exported with the current version, might not be importable by future releases. (Though they should be importable by the version they were exported with, so you could import them back into Blender, and re-export them with the newer version)

* [Getting Asset IO](#getting-asset-io)
* [Using Asset IO](#using-asset-io)
  * [Import](#import)
  * [Export](#export)
* [Reporting issues](#reporting-issues)

## Getting Asset IO
Download file entitled **Asset_IO.zip** from the [latest&nbsp;release](../../releases/latest) page. (Do not download the other .zip or .tar.gz provided by GitHub)

To install Asset IO, you can just follow the standard addon installation process in Blender, detailed here:
0. In Blender, go to **File > User Preferences...**
0. Under the **Add-ons** tab, click **Install from File...** and find the downloaded .zip
0. Type "Asset IO" in the search bar at the top left corner of the settings window
0. Click the check-box next to the addon name, to activate it
0. Optionally, click **Save User Settings**, so you don't have to activate it every time you open Blender

## Using Asset IO
### Import
You can access the Asset IO importer, at **File > Import > Blib Assets (.blib)**.  
Then, in the import options, you can choose what type of asset you want to import, and all import options for that type will appear.  
Now, you just set the desired options (defaults are fine in most cases), and select the files to import, and you're set.

### Export
You can access the Asset IO exporter, at **File > Export > Blib Assets (.blib)**.  
Then, in the export options, you can choose what type of asset you want to export, and a list with all exportable assets of that type will appear, wherein you can select all the assets to be exported.  
Now, you just set the desired export options below the asset list (defaults are fine in most cases), and you're set.

## Reporting issues
If you encounter a bug or issue with Blib, before reporting it make sure you are using the latest released version of Asset IO (you can check the latest version on the [latest&nbsp;release&nbsp;page](../../releases/latest)), and Blender version 2.76 or later, as no previous versions are officially supported.

Once you verified all of the above, you can head to the [issues&nbsp;page](../../issues), and click the "New issue" button.  
Start by giving it a short and descriptive title. Then you write your report in the following format, replacing the fields with the appropriate info:
```
* **Platform:** Linux/OSX/Windows
* **Blender version:** 2.76
* **Steps to reproduce:**
  0. Do this
  0. Do that
  0. Do this other thing
* **Expected behavior:** This is what should actually happen.

If you feel like the title and the above info are not enough to describe the issue,
here you can write a more thorough description of the issue.
```
Note that the list of steps to reproduce, should be numbered with zeroes ("0"), and will automatically be replaced by the correct numbers.
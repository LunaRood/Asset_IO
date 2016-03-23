# ##### BEGIN GPL LICENSE BLOCK #####
#
# Part of the Asset_IO package.
# Properties: Definition of all custom properties used by Asset_IO.
# Copyright (C) 2016  Luca Rood
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty, PointerProperty

try:
    import blib as ext_blib
except ImportError:
    from .blib.cycles import bexport as export_cycles
    from .blib.cycles import bimport as import_cycles
    from .blib.cycles.utils import check_asset as is_cycles_asset
    from .blib.cycles.utils import check_file as is_cycles_file
    from .blib.utils import gen_resource_path
else:
    from . import blib as loc_blib
    loc_ver = loc_blib.utils.Version(loc_blib.__version__.split()[0])
    ext_ver = loc_blib.utils.Version(ext_blib.__version__.split()[0])
    if loc_ver >= ext_ver:
        from .blib.cycles import bexport as export_cycles
        from .blib.cycles import bimport as import_cycles
        from .blib.cycles.utils import check_asset as is_cycles_asset
        from .blib.cycles.utils import check_file as is_cycles_file
        from .blib.utils import gen_resource_path
    else:
        from blib.cycles import bexport as export_cycles
        from blib.cycles import bimport as import_cycles
        from blib.cycles.utils import check_asset as is_cycles_asset
        from blib.cycles.utils import check_file as is_cycles_file
        from blib.utils import gen_resource_path

#Generic item for single asset
class AssetItem(bpy.types.PropertyGroup):
    name = StringProperty()
    state = BoolProperty(
           description="Toggle export",
           default=False)


### PER ASSET TYPE EXPORT/IMPORT PROPERTIES ###

#Properties for Cycles export
class CyclesExportProps(bpy.types.PropertyGroup):
    imgi_export = BoolProperty(
        name="Export packed images",
        description="Include images/textures that are packed in the .blend file",
        default=True
    )
    
    imge_export = BoolProperty(
        name="Export external images",
        description="Include images/textures that are separately saved on disc",
        default=True
    )
    
    seq_export = BoolProperty(
        name="Export image sequences",
        description="Include image sequences within the .blib file",
        default=True
    )
    
    mov_export = BoolProperty(
        name="Export movies",
        description="Include movies within the .blib file",
        default=True
    )
    
    txti_export = BoolProperty(
        name="Export packed texts",
        description="Include text blocks that are packed in the .blend file",
        default=True
    )
    
    txte_export = BoolProperty(
        name="Export external texts",
        description="Include text blocks that are separately saved on disc",
        default=True
    )
    
    script_export = BoolProperty(
        name="Export external scripts",
        description='Include scripts that are only referenced by their path in a "script" node',
        default=True
    )
    
    optimize_file = BoolProperty(
        name="Optimize file",
        description='Reduce file size slightly, by not including "blank" variables (Increases risk of broken or incompatible files)',
        default=False
    )

#Properties for Cycles import
class CyclesImportProps(bpy.types.PropertyGroup):
    imgi_import = BoolProperty(
        name="Import packed images",
        description="Import images/textures that were packed in the .blend file",
        default=True
        )
    
    imge_import = BoolProperty(
        name="Import external images",
        description="Import images/textures that were separately saved on disc",
        default=True
        )
    
    seq_import = BoolProperty(
        name="Import image sequences",
        description="Import image sequences",
        default=True
        )
    
    mov_import = BoolProperty(
        name="Import movies",
        description="Import movies",
        default=True
        )
    
    txti_import = BoolProperty(
        name="Import packed texts",
        description="Import text blocks that were packed in the .blend file",
        default=True
        )
    
    txte_import = BoolProperty(
        name="Import external texts",
        description="Import text blocks that were separately saved on disc",
        default=True
        )
    
    script_import = BoolProperty(
        name="Import external scripts",
        description='Import scripts that are only referenced by their path in a "script" node',
        default=True
        )
    
    img_embed = EnumProperty(
        name="Pack Images",
        items=(
            ("True", "Yes", "Pack all images into .blend file"),
            ("False", "No", "Store all images externally"),
            ("None", "Auto", "Maintain setup from exported material")
            ),
        default="False"
        )
    
    txt_embed = EnumProperty(
        name="Pack Texts",
        items=(
            ("True", "Yes", "Pack all texts into .blend file"),
            ("False", "No", "Store all texts externally"),
            ("None", "Auto", "Maintain setup from exported material")
            ),
        default="None"
        )
    
    img_merge = BoolProperty(
        name="Reuse existing images",
        description="For duplicate images, use those already in your resource library instead of creating new a instance",
        default=True
        )
    
    resource_path = StringProperty(
        name="Resource path",
        description="Directory to save external resources (images, texts...)",
        default=gen_resource_path(),
        subtype='DIR_PATH'
        )
    
    skip_sha1 = BoolProperty(
        name="Skip checksum",
        description="Skip file corruption verification (only use if you manually edited the file, and know what you're doing)",
        default=False
        )


### ASSET TYPE CONTAINERS ###

#Container for Cycles assets
class CyclesType(bpy.types.PropertyGroup):
    export_props = PointerProperty(type=CyclesExportProps)
    import_props = PointerProperty(type=CyclesImportProps)
    assets = CollectionProperty(type=AssetItem)


### GENERIC BLIB CONTAINERS ###

#Container for all asset types
class AssetList(bpy.types.PropertyGroup):
    cycles_mat = PointerProperty(type=CyclesType)
    cycles_grp = PointerProperty(type=CyclesType)

#Root blib property containing assets and the export type enum
class BlibThings(bpy.types.PropertyGroup):
    export_type = EnumProperty(
        name = "Asset type",
        description = "The kind of data to be exported",
        items = [("cycles_mat", "Cycles Material", "Cycles renderer materials"),
                 ("cycles_grp", "Cycles Node Group", "Node groups for Cycles renderer materials")]
    )
    
    import_type = EnumProperty(
        name = "Asset type",
        description = "The kind of data to be imported",
        items = [("cycles_mat", "Cycles Material", "Cycles renderer materials"),
                 ("cycles_grp", "Cycles Node Group", "Node groups for Cycles renderer materials")]
    )
    
    assets = PointerProperty(type=AssetList)
    
    asset_types = {
        "cycles_mat": {
            "name": "Cycles Material",
            "data": "materials",
            "check_asset_func": is_cycles_asset,
            "check_file_func": is_cycles_file,
            "exp_func": export_cycles,
            "imp_func": import_cycles,
            "exp_props": ["imgi_export", "imge_export", "seq_export", "mov_export", "txti_export", "txte_export", "script_export", "optimize_file"],
            "imp_props": ["imgi_import", "imge_import", "seq_import", "mov_import", "txti_import", "txte_import",
                             "script_import", "img_embed", "txt_embed", "img_merge", "resource_path", "skip_sha1"],
            "list_type": "EXPORT_UL_cycles_mat"
        },
        "cycles_grp": {
            "name": "Cycles Node Group",
            "data": "node_groups",
            "check_asset_func": is_cycles_asset,
            "check_file_func": is_cycles_file,
            "exp_func": export_cycles,
            "imp_func": import_cycles,
            "exp_props": ["imgi_export", "imge_export", "seq_export", "mov_export", "txti_export", "txte_export", "script_export", "optimize_file"],
            "imp_props": ["imgi_import", "imge_import", "seq_import", "mov_import", "txti_import", "txte_import",
                             "script_import", "img_embed", "txt_embed", "img_merge", "resource_path", "skip_sha1"],
            "list_type": "EXPORT_UL_cycles_grp"
        }
    }

props = [
    #Cycles items
    CyclesExportProps, CyclesImportProps, CyclesType,
]

# ##### BEGIN GPL LICENSE BLOCK #####
#
# Asset_IO: Import and export assets using the Blib package.
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

bl_info = {
    "name": "Asset IO",
    "description": "Import and export blender assets (.blib)",
    "author": "Luca Rood",
    "version": (0, 1, 0),
    "blender": (2, 76, 0),
    "location": "File > Import-Export > Export Assets (.blib)",
    "warning": "Beta version, might contain bugs.",
    "category": "Import-Export"
    }

import bpy

from os import path
from bpy.props import StringProperty, CollectionProperty, IntProperty, PointerProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from .ops import BLIB_OT_select_all, BLIB_OT_select_none
from .props import AssetItem, AssetList, BlibThings
from .props import props
from .lists import lists

try:
    import blib as ext_blib
except ImportError:
    from .blib.exceptions import BlibException
else:
    from . import blib as loc_blib
    loc_ver = loc_blib.utils.Version(loc_blib.__version__.split()[0])
    ext_ver = loc_blib.utils.Version(ext_blib.__version__.split()[0])
    if loc_ver >= ext_ver:
        from .blib.exceptions import BlibException
    else:
        from blib.exceptions import BlibException

def uniquify_name(filepath):
    num = 1
    newpath = filepath
    parts = path.splitext(filepath)
    while path.isfile(newpath):
        newpath = parts[0] + str(num) + parts[1]
        num += 1
    return newpath

class ExportConfirmation(bpy.types.Operator):
    bl_idname = "blib.export_confirm"
    bl_label = "Some files to be exported already exist"
    bl_description = "Select what to do with duplicate files"
    
    directory = StringProperty()
    filename = StringProperty()
    
    ### All the code commented out in this class is not working because of a Blender bug, and shall be reactivated once fixed ###
    # dup_assets = CollectionProperty(type=AssetItem)
    # asset_index = IntProperty(default=0)
    
    def draw(self, context):
        layout = self.layout
        
        layout.label("Action to be taken:")
        layout.prop(context.scene.blib, "action", expand=True)
        
        # layout.template_list(asset_info["list_type"], "", self, "dup_assets", self, "asset_index")
    
    def invoke(self, context, event):
        asset_type = context.scene.blib.export_type
        asset = getattr(context.scene.blib.assets, asset_type)
        assets = asset.assets
        
        for asset in assets:
            if asset.state == True:
                filepath = path.join(self.directory, "{}_{}.blib".format(path.splitext(self.filename)[0], asset.name))
                if path.isfile(filepath):
                    return context.window_manager.invoke_props_dialog(self)
        
        # for asset in assets:
        #     if asset.state == True:
        #         filepath = path.join(self.directory, "{}_{}.blib".format(path.splitext(self.filename)[0], asset.name))
        #         if path.isfile(filepath):
        #             dup_asset = self.dup_assets.add()
        #             dup_asset.name = asset.name
        #             dup_asset.state = True
        
        return self.execute(context)
    
    def execute(self, context):
        asset_type = context.scene.blib.export_type
        asset_info = context.scene.blib.asset_types[asset_type]
        asset = getattr(context.scene.blib.assets, asset_type)
        assets = asset.assets
        props = asset.export_props
        data = getattr(bpy.data, asset_info["data"])
        
        success = 0
        failed = 0
        
        print()
        
        for asset in assets:
            if asset.state == True:
                filepath = path.join(self.directory, "{}_{}.blib".format(path.splitext(self.filename)[0], asset.name))
                if context.scene.blib.action == "rename":
                    filepath = uniquify_name(filepath)
                elif context.scene.blib.action == "ignore":
                    if path.isfile(filepath):
                        continue
                
                print()
                print("Initiating export of '{}'".format(asset.name))
                try:
                    asset_info["exp_func"](data[asset.name], filepath, **{prop: getattr(props, prop) for prop in asset_info["exp_props"]})
                except BlibException as e:
                    failed += 1
                    self.report({'WARNING'}, "'{}' failed to export.".format(asset.name))
                    print("'{}' failed to export, with the following error:".format(asset.name))
                    print(e)
                else:
                    success += 1
                    print("'{}' exported successfully.".format(asset.name))
        
        self.report({'INFO'}, "{} of {} successful exports. Check system console for more info".format(success, success + failed))
        print()
        print("{} of {} successful exports.".format(success, success + failed))
        return {'FINISHED'}

class ExportBlib(bpy.types.Operator, ExportHelper):
    bl_idname = "blib.export"
    bl_label = "Export BLIB"
    bl_description = "Save assets to .blib files"

    filename_ext = ".blib"
    filter_glob = StringProperty(default="*.blib")
    directory = StringProperty()
    filepath = StringProperty()
    filename = StringProperty(default="untitled")
    
    asset_index = IntProperty(default=0)
    
    def draw(self, context):
        asset_type = context.scene.blib.export_type
        asset = getattr(context.scene.blib.assets, asset_type)
        layout = self.layout
        
        layout.prop(context.scene.blib, "export_type")
        
        asset_info = context.scene.blib.asset_types[asset_type]
        
        if asset_info["list_type"] is not None:
            layout.template_list(asset_info["list_type"], "", asset, "assets", self, "asset_index")
            row = layout.row(align=True)
            row.operator("blib.sel_all").asset_type = asset_type
            row.operator("blib.sel_none").asset_type = asset_type
        
        for prop in asset_info["exp_props"]:
            layout.prop(asset.export_props, prop)
    
    def invoke(self, context, event):
        self.filepath = "untitled.blib"
        
        for a_type, asset_info in context.scene.blib.asset_types.items():
            data = getattr(bpy.data, asset_info["data"])
            assets = getattr(context.scene.blib.assets, a_type).assets
            assets.clear()
            
            for item in data:
                if asset_info["check_asset_func"](item):
                    asset = assets.add()
                    asset.name = item.name
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        return bpy.ops.blib.export_confirm('INVOKE_DEFAULT', directory=self.directory, filename=self.filename)

class ImportBlib(bpy.types.Operator, ImportHelper):
    bl_idname = "blib.import"
    bl_label = "Import BLIB"
    bl_description = "Load assets from .blib files"

    filename_ext = ".blib"
    filter_glob = StringProperty(default="*.blib")
    directory = StringProperty()
    files = CollectionProperty(type=bpy.types.PropertyGroup)
    
    def draw(self, context):
        asset_type = context.scene.blib.import_type
        asset = getattr(context.scene.blib.assets, asset_type)
        layout = self.layout
        
        layout.prop(context.scene.blib, "import_type")
        
        asset_info = context.scene.blib.asset_types[asset_type]
        
        for prop in asset_info["imp_props"]:
            layout.prop(asset.import_props, prop)
    
    def execute(self, context):
        asset_type = context.scene.blib.import_type
        asset_info = context.scene.blib.asset_types[asset_type]
        asset = getattr(context.scene.blib.assets, asset_type)
        props = asset.import_props
        sub = asset_type.split("_")[-1]
        
        success = 0
        failed = 0
        incompatible = 0
        
        print()
        
        if len(self.files) == 1 and self.files[0].name == "":
            self.report({'WARNING'}, "No file selected.")
            print("No file selected.")
            return {'CANCELLED'}
        
        for filename in self.files:
            if filename.name == "":
                continue
            filepath = path.join(self.directory, filename.name)
            
            if not asset_info["check_file_func"](filepath, sub):
                incompatible += 1
                self.report({'WARNING'}, "{} is not of type '{}'.".format(filename.name, asset_info["name"]))
                print("{} is not of type '{}'.".format(filename.name, asset_info["name"]))
                continue
            
            print()
            print("Initiating import of {}".format(filename.name))
            try:
                asset_info["imp_func"](filepath, **{prop: getattr(props, prop) for prop in asset_info["imp_props"]})
            except BlibException as e:
                failed += 1
                self.report({'WARNING'}, "{} failed to import.".format(filename.name))
                print("{} failed to import, with the following error:".format(filename.name))
                print(e)
            else:
                success += 1
                print("'{}' imported successfully.".format(filename.name))
        
        if incompatible == 0:
            self.report({'INFO'}, "{} of {} successful imports. Check system console for more info".format(success, success + failed))
            print()
            print("{} of {} successful imports.".format(success, success + failed))
        else:
            self.report({'INFO'}, "{} of {} successful imports. {} files were not of type '{}'. Check system console for more info".format(success, success + failed, incompatible, asset_info["name"]))
            print()
            print("{} of {} successful imports. {} files were not of type '{}'.".format(success, success + failed, incompatible, asset_info["name"]))
        return {'FINISHED'}

def menu_func_export(self, context):
    self.layout.operator(ExportBlib.bl_idname, text="Blib Assets (.blib)")

def menu_func_import(self, context):
    self.layout.operator(ImportBlib.bl_idname, text="Blib Assets (.blib)")

def register():
    #Generic asset item
    bpy.utils.register_class(AssetItem)
    
    for l in lists:
        bpy.utils.register_class(l)
    
    for p in props:
        bpy.utils.register_class(p)
    
    #Generic Blib properties
    bpy.utils.register_class(AssetList)
    bpy.utils.register_class(BlibThings)
    
    #Operator registration
    bpy.utils.register_class(ExportBlib)
    bpy.utils.register_class(ImportBlib)
    bpy.utils.register_class(ExportConfirmation)
    bpy.utils.register_class(BLIB_OT_select_all)
    bpy.utils.register_class(BLIB_OT_select_none)
    
    #Assignments
    bpy.types.Scene.blib = PointerProperty(type=BlibThings)
    bpy.types.INFO_MT_file_export.append(menu_func_export)
    bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
    #Unassignments
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    del bpy.types.Scene.blib
    
    #Generic Blib properties
    bpy.utils.unregister_class(AssetList)
    bpy.utils.unregister_class(BlibThings)
    
    for l in lists:
        bpy.utils.unregister_class(l)
    
    for p in reversed(props):
        bpy.utils.unregister_class(p)
    
    #Generic asset item
    bpy.utils.unregister_class(AssetItem)
    
    #Operator unregistration
    bpy.utils.unregister_class(ExportBlib)
    bpy.utils.unregister_class(ImportBlib)
    bpy.utils.unregister_class(ExportConfirmation)
    bpy.utils.unregister_class(BLIB_OT_select_all)
    bpy.utils.unregister_class(BLIB_OT_select_none)

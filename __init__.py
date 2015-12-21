bl_info = {
    "name": "x templates",
    "author": "Dealga McArdle",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Text Editor"
}

import itertools
import os
import bpy
from bpy_extras.io_utils import ExportHelper


''' consumeables, variables '''

xtemp_classes = []
submenus = []
subdict = {}
current_dir = os.path.dirname(__file__)


''' utility functions '''


def sanitize_name(pyfile):
    return pyfile.replace('_', ' ').replace('.py', '')


def get_subdirs(current_dir):
    for f in os.listdir(current_dir):
        if f in {'__pycache__', '.git'}:
            continue

        joined = os.path.join(current_dir, f)
        if os.path.isdir(joined):
            yield joined


def path_iterator(path_name):
    for fp in os.listdir(path_name):
        if fp.endswith(".py") and not (fp == '__init__.py'):
            yield fp


def make_menu(name, draw):
    overwrites = {
        'bl_idname': 'TEXT_MT_xtemplates_' + name,
        'bl_label': name,
        'draw': draw,
    }
    return type(name, (bpy.types.Menu,), overwrites)


def make_menu2(name, draw):
    overwrites = {
        'bl_idname': 'TEXT_MT_xtemplates_' + name,
        'bl_label': "x templates",
        'draw': draw,
    }
    return type(name, (bpy.types.Menu,), overwrites)


''' UI classes / Operators / Preferences '''


class XTemplatesDirectorySelector(bpy.types.Operator, ExportHelper):
    ''' this is used on the button beside the string box in user prefs '''

    bl_idname = "wm.xtemplates_folder_selector"
    bl_label = "some folder"

    filename_ext = ''
    use_filter_folder = True

    def execute(self, context):
        # even if you pick a file i'll strip it and get the dirname
        fdir = self.properties.filepath
        dp = os.path.dirname(fdir)

        try:
            addon = bpy.context.user_preferences.addons.get(__name__)
            if addon:
                prefs = addon.preferences
                prefs['full_directory'] = dp

                # here be dragons.

                global submenus

                # this pops current menus
                bpy.utils.unregister_class(XTemplatesHeadMenu)
                # print(submenus)
                for menu in reversed(submenus):
                    bpy.utils.unregister_class(menu)
                    # del menu

                del XTemplatesHeadMenu

                def modified_draw(self, context):
                    for name, long_name in get_submenu_names():
                        self.layout.menu(long_name, text=sanitize_name(name))

                XTemplatesHeadMenu = make_menu2("headmenu", modified_draw)

                # this builds up new menus
                submenus = []
                current_dir = dp
                make_subdirs(current_dir)

                for menu in submenus:
                    bpy.utils.register_class(menu)
                bpy.utils.register_class(XTemplatesHeadMenu)

            else:
                print('no addon data found')

        except:
            XK = 'add-on not registered yet.. reload with f8'
            self.report({'INFO'}, XK)

        return {'FINISHED'}


class XTemplatesPreferences(bpy.types.AddonPreferences):

    bl_idname = __name__

    full_directory = bpy.props.StringProperty(name="")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "full_directory", text="")
        row.operator("wm.xtemplates_folder_selector", icon="FILE_FOLDER", text="")


class XTemplatesLoader(bpy.types.Operator):

    bl_idname = 'wm.script_template_loader'
    bl_label = 'load templates into TE'

    script_path = bpy.props.StringProperty(default='')

    def execute(self, context):
        if self.script_path:
            bpy.ops.text.open(filepath=self.script_path, internal=True)
        return {'FINISHED'}


def make_subdirs(current_dir):
    for subdir in get_subdirs(current_dir):

        submenu_name = os.path.basename(subdir)
        subdict[submenu_name] = []

        for pyfile in path_iterator(subdir):
            pyfile_path = os.path.join(subdir, pyfile)
            subdict[submenu_name].append([submenu_name, pyfile, pyfile_path])

        if not subdict[submenu_name]:
            continue

        def sub_draw(self, context):
            layout = self.layout
            t = "wm.script_template_loader"
            this_menu_name = self.bl_idname.replace("TEXT_MT_xtemplates_", "")
            for _, _pyfile, _path in subdict[this_menu_name]:
                file_name_to_show = sanitize_name(_pyfile)
                layout.operator(t, text=file_name_to_show).script_path = _path

        dynamic_class = make_menu(submenu_name, sub_draw)
        submenus.append(dynamic_class)


def get_submenu_names():
    for k, v in sorted(subdict.items()):
        yield k, 'TEXT_MT_xtemplates_' + k


# class XTemplatesHeadMenu(bpy.types.Menu):
#     bl_idname = "TEXT_MT_xtemplates_headmenu"
#     bl_label = "x templates"
#     def draw(self, context):
#         for name, long_name in get_submenu_names():
#             self.layout.menu(long_name, text=sanitize_name(name))

def sub_draw(self, context):
    for name, long_name in get_submenu_names():
        self.layout.menu(long_name, text=sanitize_name(name))


XTemplatesHeadMenu = make_menu("headmenu", sub_draw)


def menu_draw(self, context):
    self.layout.menu("TEXT_MT_xtemplates_headmenu")

xtemp_classes.append(XTemplatesDirectorySelector)
xtemp_classes.append(XTemplatesPreferences)
xtemp_classes.append(XTemplatesLoader)
xtemp_classes.append(XTemplatesHeadMenu)


def register():

    try:
        addon = bpy.context.user_preferences.addons.get(__name__)
        if addon:
            prefs = addon.preferences
            user_dir = prefs['full_directory']
            make_subdirs(user_dir)
            print('xtemplates: using custom directory')
        else:
            print('addon prefs not found yet')
    except:
        print('xtemplates: using default directory')
        make_subdirs(current_dir)

    for menu in itertools.chain.from_iterable([submenus, xtemp_classes]):
        bpy.utils.register_class(menu)
    bpy.types.TEXT_MT_templates.append(menu_draw)


def unregister():
    bpy.types.TEXT_MT_templates.remove(menu_draw)
    items = list(itertools.chain.from_iterable([submenus, xtemp_classes]))
    for menu in reversed(items):
        bpy.utils.unregister_class(menu)

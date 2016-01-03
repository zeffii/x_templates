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

import os
import bpy


current_dir = os.path.dirname(__file__)


def get_subdirs(current_dir):
    for f in os.listdir(current_dir):
        if f in {'__pycache__', '.git'}:
            continue

        joined = os.path.join(current_dir, f)

        if os.path.isdir(joined):

            # skip empty dirs
            if os.listdir(joined) == []:
                continue

            yield joined


def make_menu(name, path):

    def draw(self, context):
        layout = self.layout
        self.path_menu([path], "text.open", {"internal": True})

    overwrites = {
        'bl_idname': 'TEXT_MT_xtemplates_' + name,
        'bl_label': name,
        'draw': draw,
    }
    return type(name, (bpy.types.Menu,), overwrites)


submenus = []
menu_names = []

for subdir in get_subdirs(current_dir):

    submenu_name = os.path.basename(subdir)
    menu_names.append(submenu_name)

    dynamic_class = make_menu(submenu_name, subdir)
    submenus.append(dynamic_class)


def get_submenu_names():
    for k in sorted(menu_names):
        yield k, 'TEXT_MT_xtemplates_' + k


class XTemplatesHeadMenu(bpy.types.Menu):
    bl_idname = "TEXT_MT_xtemplates_headmenu"
    bl_label = "x templates"

    def draw(self, context):
        for name, long_name in get_submenu_names():
            self.layout.menu(long_name, text=name.replace('_', ' '))


def menu_draw(self, context):
    self.layout.menu("TEXT_MT_xtemplates_headmenu")


def register():
    for menu in submenus:
        bpy.utils.register_class(menu)

    bpy.utils.register_class(XTemplatesHeadMenu)
    bpy.types.TEXT_MT_templates.append(menu_draw)


def unregister():
    bpy.types.TEXT_MT_templates.remove(menu_draw)
    bpy.utils.unregister_class(XTemplatesHeadMenu)

    for menu in reversed(submenus):
        bpy.utils.unregister_class(menu)

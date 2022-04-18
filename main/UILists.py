import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

# ======== Custom Metadata Fields UIList ======== #

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------

class CUSTOM_OT_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.custom_index

        try:
            item = scn.custom[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.custom) - 1:
                item_next = scn.custom[idx + 1].name
                scn.custom.move(idx, idx + 1)
                scn.custom_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.custom[idx - 1].name
                scn.custom.move(idx, idx - 1)
                scn.custom_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.custom_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.custom[idx].name)
                scn.custom_index -= 1
                scn.custom.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            if context.object:
                item = scn.custom.add()
                item.name = "Custom Metadata Field"  # The name of each object
                scn.custom_index = len(scn.custom) - 1
                info = '"%s" added to list' % (item.name)
                self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}


class CUSTOM_OT_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "custom.clear_list"
    bl_label = "Clear Custom Fields"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.custom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.custom):
            context.scene.custom.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return {'FINISHED'}


# UIList class
class CUSTOM_UL_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.1)
        split.label(text=f"{index + 1}")
        row = split.row()
        row.label(text=item.name)  # avoids renaming the item by accident
        row.prop(item, "field_name", text="")
        row.prop(item, "field_value", text="")

    def invoke(self, context, event):
        pass

# -------------------------------------------------------------------
#   Collection
# -------------------------------------------------------------------

class CUSTOM_objectCollection(PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    obj_type: StringProperty()
    obj_id: IntProperty()
    field_name: StringProperty(default="Name")
    field_value: StringProperty(default="Value")


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes_UILists = (
    CUSTOM_OT_actions,
    CUSTOM_OT_clearList,
    CUSTOM_UL_items,
    CUSTOM_objectCollection,
)

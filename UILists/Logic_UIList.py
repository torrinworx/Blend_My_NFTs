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

# ======== Operators ======== #
class CUSTOM_OT_logic_actions(Operator):
    """Move items up and down, add and remove"""
    bl_idname = "logic_uilist.logic_list_action"
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
        idx = scn.logic_fields_index

        try:
            item = scn.logic_fields[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(scn.logic_fields) - 1:
                item_next = scn.logic_fields[idx + 1].name
                scn.logic_fields.move(idx, idx + 1)
                scn.logic_fields_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.logic_fields_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'UP' and idx >= 1:
                item_prev = scn.logic_fields[idx - 1].name
                scn.logic_fields.move(idx, idx - 1)
                scn.logic_fields_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scn.logic_fields_index + 1)
                self.report({'INFO'}, info)

            elif self.action == 'REMOVE':
                info = 'Item "%s" removed from list' % (scn.logic_fields[idx].name)
                scn.logic_fields_index -= 1
                scn.logic_fields.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
            if context.object:
                item = scn.logic_fields.add()
                item.name = "Rule"  # The name of each object
                scn.logic_fields_index = len(scn.logic_fields) - 1
                info = '"%s" added to list' % (item.name)
                self.report({'INFO'}, info)
            else:
                self.report({'INFO'}, "Nothing selected in the Viewport")
        return {"FINISHED"}


class CUSTOM_OT_logic_clearList(Operator):
    """Clear all items of the list"""
    bl_idname = "logic_uilist.logic_clear_list"
    bl_label = "Clear Logic Rules"
    bl_description = "Clear all items of the list"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.logic_fields)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.logic_fields):
            context.scene.logic_fields.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return {'FINISHED'}


# ======== UILists ======== #
class CUSTOM_UL_logic_items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.1)
        split.label(text=f"{index + 1}")
        row = split.row()
        row.label(text=item.name)  # avoids renaming the item by accident
        row.prop(item, "item_list1", text="")

        row.prop(item, "rule_type", text="")
        row.prop(item, "item_list2", text="")

    def invoke(self, context, event):
        pass


# ======== Property Collection ======== #
class CUSTOM_logic_objectCollection(PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    obj_type: StringProperty()
    obj_id: IntProperty()

    item_list1: StringProperty(default="Item List 1")
    rule_type: EnumProperty(
        name="Rule Type",
        description="Select the Rule Type",
        items=[
            ('Never With', "Never With", ""),
            ('Only With', "Only With", ""),
            ('Always With', "Always With", ""),

        ]
    )
    item_list2: StringProperty(default="Item List 2")


# ======== Register/Unregister Classes (Passed to __init__.py for operation) ======== #
classes_Logic_UIList = (
    CUSTOM_OT_logic_actions,
    CUSTOM_OT_logic_clearList,
    CUSTOM_UL_logic_items,
    CUSTOM_logic_objectCollection,
)

bl_info = {
    "name": "Woow Gold",
    "blender": (3, 0, 0),
    "category": "Object",
}



import bpy
from bpy.types import Menu


def bevel_depth(number,context):
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if not selected_objects:
        print("No objects are selected.")
    else:
        for obj in selected_objects:   
                # Replace "Curve" with the name of your curve object
                if obj and obj.type == 'CURVE': 
                        obj = bpy.data.objects.get(obj.name)
                        # Set the bevel depth to 3 meters
                        obj.data.bevel_depth = number/2  # Blender uses units based on the scene's unit settings (default is meters)
                        # Set the bevel resolution for a round bevel
                        obj.data.bevel_resolution = 12  # You can adjust this value for smoother roundness
                else:
                        mod = obj.modifiers.get("Solidify")  # البحث عن معدل Solidify
                        if mod and mod.type == 'SOLIDIFY':  # التأكد من أن المعدل موجود ونوعه صحيح
                            mod.thickness = number
                        else:
                            # إضافة معدل Solidify إذا لم يكن موجودًا
                            mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
                            mod.thickness = number

                    
                        



class VIEW3D_PIE_depth(Menu):
    bl_label = "Depth woow"
    bl_idname = "VIEW3D_PIE_depth"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # ستة خيارات في القائمة النقطية
        pie.operator("wm.depth_number", text="0.0").number = 0
        pie.operator("wm.depth_number", text="0.2").number = 1
        pie.operator("wm.depth_number", text="0.25").number =2
        pie.operator("wm.depth_number", text="0.3").number = 3
        pie.operator("wm.depth_number", text="0.35").number =4
        pie.operator("wm.depth_number", text="0.4").number = 5
        pie.operator("wm.depth_number", text="0.45").number =6
        pie.operator("wm.depth_number", text="0.6").number = 7
        pie.operator("wm.depth_number", text="1.0").number = 8


# عامل (Operator) لطباعة الرقم
class WM_OT_depth_number(bpy.types.Operator):
    bl_idname = "wm.depth_number"
    bl_label = "Depth Number"
    number: bpy.props.IntProperty()  # خاصية لتخزين الرقم
    def execute(self, context):
        print(f"Selected Option: {self.number}")  # طباعة الرقم في وحدة التحكم
        self.report({'INFO'}, f"Selected Option: {self.number}")  # عرض الرسالة في واجهة المستخدم
        selected_object = bpy.context.active_object
        name=selected_object.name
        bike =self.number
        if bike == 1:
            bevel_depth(0.2, context)
        elif bike == 2:
            bevel_depth(0.25,context)
        elif bike == 3:
            bevel_depth(0.3, context)
        elif bike == 4:
            bevel_depth(0.35, context)
        elif bike == 5:
             bevel_depth(0.4,context)
        elif bike == 6:
            bevel_depth(0.45,context)
        elif bike == 7:
            bevel_depth(0.6,context)
        elif bike ==8:            
            bevel_depth(1.0,context)
        
        return {'FINISHED'}

# عامل (Operator) لفتح القائمة النقطية
class OBJECT_OT_call_pie_depth(bpy.types.Operator):
    bl_idname = "wm.call_depth_pie_menu"
    bl_label = "Call Depth Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_PIE_depth")
        return {'FINISHED'}

# تسجيل الوظائف الإضافية
addon_keymaps = []
def register():
    bpy.utils.register_class(VIEW3D_PIE_depth)
    bpy.utils.register_class(WM_OT_depth_number)
    bpy.utils.register_class(OBJECT_OT_call_pie_depth)
    # إعداد اختصار لوحة المفاتيح
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_depth_pie_menu", type='E', value='PRESS', shift=True)
    addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(VIEW3D_PIE_template)
    bpy.utils.unregister_class(WM_OT_depth_number)
    bpy.utils.unregister_class(OBJECT_OT_call_pie_depth)

if __name__ == "__main__":
    register()
bl_info = {
    "name": "Woow Gold",
    "blender": (3, 0, 0),
    "category": "Object",
}



import bpy
from bpy.types import Menu




def sep_curve(obj):
    if obj is None or obj.type != 'CURVE':
        print("يجب أن يكون الكائن النشط منحنى (Curve)")
        return
    curve_data = obj.data
    connected_points = []
    for spline in curve_data.splines:
        if spline.type == 'BEZIER':
            points = spline.bezier_points
        else:
            points = spline.points
        connected_group = []
        for i, point in enumerate(points):
            connected_group.append(point.co[:3])
        connected_points.append(connected_group)
    return connected_points



def separate_curve():
    obj = bpy.context.active_object
    name=obj.name
    sd = sep_curve(obj)
    xd=enumerate(sd)
    for i, group in xd :
            print (f" {i}  {len}")
            tolerance = 1e-5
            def is_close(v1, v2, tol):
                return all(abs(a - b) < tol for a, b in zip(v1, v2))
            obj = bpy.context.active_object
            if obj and obj.type == 'CURVE':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='DESELECT')
                for spline in obj.data.splines:
                    if spline.type == 'BEZIER':
                        for point in spline.bezier_points:
                            for target_coords in group:
                                if is_close(point.co, target_coords, tolerance):  # Check if the point matches any of the target coordinates
                                    point.select_control_point = True
                    elif spline.type in {'NURBS', 'POLY'}:
                        for point in spline.points:
                            for target_coords in group:
                                if is_close(point.co.xyz, target_coords, tolerance):  # Check if the point matches any of the target coordinates
                                    point.select = True
            bpy.ops.curve.separate()
    bpy.ops.object.editmode_toggle()
    if name in bpy.data.objects:
                bpy.ops.object.select_all(action='DESELECT')
               
                bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
                
    bpy.ops.object.delete() 
    
def Threed(context):
    print(1)

def separate_by_loose_parts():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    
def boolean(object_a_name,object_b_name):
    # Get the objects
    object_a = bpy.data.objects.get(object_a_name)
    object_b = bpy.data.objects.get(object_b_name)
    if object_a and object_b:
        # Add a Boolean modifier to object_a
        bool_modifier = object_a.modifiers.new(name="Boolean", type='BOOLEAN')
        # Set the operation type (DIFFERENCE, UNION, INTERSECT)
        bool_modifier.operation = 'DIFFERENCE'  # Change to 'UNION' or 'INTERSECT' as needed
        # Set the target object for the Boolean modifier
        bool_modifier.object = object_b
        # Set the solver to 'FAST'
        bool_modifier.solver = 'FAST'
        # Optionally, apply the modifier
       # bpy.context.view_layer.objects.active = object_a
       # bpy.ops.object.modifier_apply(modifier=bool_modifier.name)
    else:
        print(f"Object '{object_a_name}' or '{object_b_name}' not found.")

def boolean_all(context):
    selected_object = bpy.context.active_object
    Select_name=selected_object.name
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if not selected_objects:
            print("No objects are selected.")
    else:
            for obj in selected_objects:
                if  obj.name !=Select_name  : 
                    obj.hide_viewport = True    
                    boolean(Select_name,obj.name)
def mrror(target_object_name,context): 
    #bpy add Empty and set name fixd and location in object name and set Empty mode moveing
    empty_names="Em."+target_object_name
    print(empty_names)
    if target_object_name in bpy.data.objects:
        target_obj = bpy.data.objects[target_object_name]
        # Create a new empty object
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        # Get the newly created empty object
        new_empty = bpy.context.active_object
        # Set the name of the empty object
        new_empty.name = empty_names
        # Set the location of the empty object to the location of the target object
        new_empty.location = target_obj.location
        # Set the empty object's mode to 'MOVE'
        bpy.context.view_layer.objects.active = new_empty
        bpy.ops.object.mode_set(mode='OBJECT')  # Ensure we are in object mode
        if target_object_name in bpy.data.objects and new_empty.name in bpy.data.objects:
            obj = bpy.data.objects[target_object_name]
            mirror_obj = bpy.data.objects[new_empty.name]
            # Add mirror modifier
            modifier = obj.modifiers.new(name="Mirror", type='MIRROR')
            # Set the mirror object
            modifier.mirror_object = mirror_obj
        new_empty.select_set(True)
        bpy.ops.transform.translate('INVOKE_DEFAULT')  # Sets the mode to move 
    else:
        print(f"The object named '{target_object_name}' does not exist in the current scene.")



def copy_snap(original_name,target_name,context):
    # Ensure the objects exist
    if original_name in bpy.data.objects and target_name in bpy.data.objects:
        # Reference to the original and target objects
        original_obj = bpy.data.objects[original_name]
        target_obj = bpy.data.objects[target_name]
        # Duplicate the original object
        new_obj = original_obj.copy()
        new_obj.data = original_obj.data.copy()  # Ensure mesh data is also duplicated
        bpy.context.collection.objects.link(new_obj)
        new_obj.location = target_obj.location
        return new_obj.name
    else:
        print(f"One or both objects {new_obj.name}")
        return 0

def array(object_name,curve_name):
    obj = bpy.data.objects.get(object_name)
    curve = bpy.data.objects.get(curve_name)
    if obj is None:
        print(f"Object '{object_name}' not found.")
    elif curve is None:
        print(f"Curve '{curve_name}' not found.")
    else:
        # Add an array modifier to the object
        array_modifier = obj.modifiers.new(name="Array", type='ARRAY')
        # Set the fit type to 'FIT_CURVE'
        array_modifier.fit_type = 'FIT_CURVE'
        array_modifier.curve = curve
        print(f"Array modifier added to '{obj.name}' with fit type 'FIT_CURVE' and curve '{curve.name}'.")

def curve(object_name,curve_name):
        # Get the objects
        obj = bpy.data.objects.get(object_name)
        curve = bpy.data.objects.get(curve_name)
        if obj is None:
            print(f"Object '{object_name}' not found.")
        elif curve is None:
            print(f"Curve '{curve_name}' not found.")
        else:
            # Add a Curve modifier to the object
            curve_modifier = obj.modifiers.new(name="Curve", type='CURVE')
            curve_modifier.object = curve
            print(f"Curve modifier added to '{obj.name}' and set to use curve '{curve.name}'.")
def Arry_Fit(context):
    selected_object = bpy.context.active_object
    Select_name=selected_object.name
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if not selected_objects:
            print("No objects are selected.")
    else:
            for obj in selected_objects:
                if  obj.name !=Select_name  :
                    copy_snaps=copy_snap(obj.name,Select_name,context)
                    if  copy_snap!=0: 
                        Scale(copy_snaps)                   
                        array(copy_snaps,Select_name)
                        curve(copy_snaps,Select_name)
def Scale(name):
    obj = bpy.data.objects.get(name)
    if obj:
        # Select the object
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        

def bevel_depth(number,context):
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if not selected_objects:
        print("No objects are selected.")
    else:
        for obj in selected_objects:   
                # Replace "Curve" with the name of your curve object
                if obj.type=='CURVE': 
                    obj = bpy.data.objects.get(obj.name)
                    if obj and obj.type == 'CURVE':
                        # Set the bevel depth to 3 meters
                        obj.data.bevel_depth = number  # Blender uses units based on the scene's unit settings (default is meters)
                        # Set the bevel resolution for a round bevel
                        obj.data.bevel_resolution = 12  # You can adjust this value for smoother roundness
                        
                
def convert(context):
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if not selected_objects:
        print("No objects are selected.")
    else:
        for obj in selected_objects:   
                # Replace "Curve" with the name of your curve object 
            obj = bpy.data.objects.get(obj.name)
            if obj and obj.type == 'MESH':
                # Select the object
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                # Ensure the object is in object mode
                bpy.ops.object.mode_set(mode='OBJECT')
                # Convert the mesh object to a curve
                bpy.ops.object.convert(target='CURVE')
                
                
                
def Solidify_gold(numbers,context):
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if not selected_objects:
        print("No objects are selected.")
    else:
        for obj in selected_objects:                          
                Scale(obj.name)
                obj = bpy.data.objects.get(obj.name)
                if obj:
                    # Select the object
                    bpy.context.view_layer.objects.active = obj
                    obj.select_set(True)
                    solidify_modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
                    solidify_modifier.thickness =numbers        # Adjust the thickness as needed
                    solidify_modifier.offset = 0.0               # Adjust the offset as needed
                    solidify_modifier.use_rim = True             # Create caps at the ends of the solidified mesh
                    solidify_modifier.use_even_offset = True     # Maintain even thickness
                    solidify_modifier.use_quality_normals = True # Improve quality of normals
                    solidify_modifier.thickness_clamp = 0.0      # Clamp the maximum thickness
                    if  obj.type=="MESH" :     
                        # Create new vertex groups named "Shell", "Rim", and "Pin"
                        for group_name in ["Shell", "Rim", "Pin"]:
                            vertex_group = obj.vertex_groups.new(name=group_name)
                        # Set the Solidify modifier to use the "Shell" vertex group for output
                        solidify_modifier.shell_vertex_group = "Shell"
                        solidify_modifier.rim_vertex_group = "Rim"
                        #solidify_modifier.use_vertex_group = True

               
def curve_obj(context):
    selected_object = bpy.context.active_object
    Select_name=selected_object.name
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if not selected_objects:
            print("No objects are selected.")
    else:
            for obj in selected_objects:
                if  obj.name !=Select_name  :                 
                    curve(obj.name,Select_name)  











class VIEW3D_PIE_template(Menu):
    bl_label = "Pie Menu"
    bl_idname = "VIEW3D_PIE_template"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # ستة خيارات في القائمة النقطية
        pie.operator("wm.print_number", text="Solidify", icon='MOD_SOLIDIFY').number = 1
        pie.operator("wm.print_number", text="Curve", icon='OUTLINER_OB_CURVE').number = 2
        pie.operator("wm.print_number", text="Join", icon='SNAP_VOLUME').number = 3
        pie.operator("wm.print_number", text="Split", icon='FACE_MAPS').number = 4
        pie.operator("wm.print_number", text="Boolean", icon='MOD_BOOLEAN').number = 5
        pie.operator("wm.print_number", text="to Curve",icon='MOD_CURVE').number = 6
        pie.operator("wm.print_number", text="Mrror",icon='MOD_MIRROR').number = 7
        
        pie.operator("wm.print_number", text="Curve Array",icon='PARTICLE_POINT').number = 8

# عامل (Operator) لطباعة الرقم
class WM_OT_print_number(bpy.types.Operator):
    bl_idname = "wm.print_number"
    bl_label = "Print Number"
    number: bpy.props.IntProperty()  # خاصية لتخزين الرقم
    def execute(self, context):
        print(f"Selected Option: {self.number}")  # طباعة الرقم في وحدة التحكم
        self.report({'INFO'}, f"Selected Option: {self.number}")  # عرض الرسالة في واجهة المستخدم
        selected_object = bpy.context.active_object
        name=selected_object.name
        bike =self.number
        if bike == 1:
            Solidify_gold(0.0,context)         
        elif bike == 2:
            if selected_object.type=='CURVE':
               bevel_depth(0.0,context)
            else:
               convert(context) 
        elif bike == 3:            
             bpy.ops.object.join()
        elif bike == 4:  
             if selected_object.type=='CURVE':
                separate_curve()
             else:
                separate_by_loose_parts()
        elif bike == 5:
             boolean_all(context)
        elif bike == 6:
            curve_obj(context) 
        elif bike == 7:
            mrror(name,context)  
        elif bike ==8:            
           Arry_Fit(context)       
        
        return {'FINISHED'}

# عامل (Operator) لفتح القائمة النقطية
class OBJECT_OT_call_pie_menu(bpy.types.Operator):
    bl_idname = "wm.call_pie_menu"
    bl_label = "Call Pie Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_PIE_template")
        return {'FINISHED'}

# تسجيل الوظائف الإضافية
addon_keymaps = []

def register():
    bpy.utils.register_class(VIEW3D_PIE_template)
    bpy.utils.register_class(WM_OT_print_number)
    bpy.utils.register_class(OBJECT_OT_call_pie_menu)
    
    # إعداد اختصار لوحة المفاتيح
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_pie_menu", type='Q', value='PRESS', shift=True)
    addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(VIEW3D_PIE_template)
    bpy.utils.unregister_class(WM_OT_print_number)
    bpy.utils.unregister_class(OBJECT_OT_call_pie_menu)

if __name__ == "__main__":
    register()
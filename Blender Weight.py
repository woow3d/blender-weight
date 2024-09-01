bl_info = {
    "name": "Mesh Weight Calculator Addon",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
import bmesh

# Known densities in grams per cubic centimeter (g/c
def get_dimensions(obj):
    # Initialize max and min coordinates
    min_coords = [float('inf')] * 3
    max_coords = [-float('inf')] * 3
    # Iterate through vertices to find max and min coordinates
    for vertex in obj.data.vertices:
        world_vertex = obj.matrix_world @ vertex.co
        for i in range(3):
            min_coords[i] = min(min_coords[i], world_vertex[i])
            max_coords[i] = max(max_coords[i], world_vertex[i])
    # Calculate dimensions
    dimensions = [max_coords[i] - min_coords[i] for i in range(3)]
    return dimensions

def mesh_volume(mesh):
        bm = bmesh.new()
        bm.from_mesh(mesh)
        volume = bm.calc_volume()
        bm.free()
        return volume
def Weight(densitys,obj):
    # Density of gold in grams per cubic centimeter
    # Scale factor to convert cubic meters to cubic millimeters
    m3_to_mm3 = 1e+15 # Function to calculate the volume of a mesh in cubic meters
    # Get the active object (assumed to be the mesh you want to measure)
    if obj and obj.type == 'MESH': # Get the mesh data
        mesh = obj.data  # Calculate the volume of the mesh
        mesh_volume_m3 = mesh_volume(mesh)# Convert volume to cubic millimeters
        mesh_volume_mm3 = mesh_volume_m3 * m3_to_mm3# Calculate the weight of gold in grams
        weight_grams = (mesh_volume_mm3 * densitys )/ 1000000000000000000  # Convert from milligrams to grams
        print("Weight of the mesh in gold: {:.2f} grams".format( weight_grams))
        return weight_grams
    else:
        print("No active mesh object found.")
        return weight_grams
def All_Weight(densitys,context):
    weights=0.0
    # Iterate through all selected objects
    selected_objects = bpy.context.selected_objects
    if not selected_objects:
        print("No objects selected")
    else:
        for obj in selected_objects:
            if obj.type=="MESH":
               weights =weights+Weight(densitys,obj)
            print(f"Object: {obj.name}, Type: {obj.type}     ")
    return weights            
class DensityCalculatorProperties(bpy.types.PropertyGroup):
    material: bpy.props.EnumProperty(
        name="Material",
        description="Choose the material",
        items=[
            ('19.32', "Gold : 19.32 g/cm³", ""),
            ('17.80', "Gold : 17.80 g/cm³", ""),
            ('15.42', "Gold : 15.42 g/cm³", ""),
            ('13.5336', "Mercury : 13.5336 g/cm³", ""),
            ('10.49', "Silver : 10.49 g/cm³", ""),
            ('8.96', "Copper : 8.96 g/cm³", ""),
            ('7.874', "Iron : 7.874 g/cm³", ""),
            ('2.7', "Minim : 2.7 g/cm³", ""),
            ('1.05', "Resins Zero : 15.42 g/cm³", ""),
            ('1.20', "Polycarbonate (PC): 1.20 g/cm³", ""),
            ('1.04', "Polystyrene (PS): 1.04 g/cm³", ""),
            ('0.91', "polyethylene (LDPE): 0.91 g/cm³", ""),
            ('0.90', "Polypropylene (PP): 0.90 g/cm³", ""),    
            ('0.90', "Paraffin Wax: 0.90 g/cm³", ""),
            ('0.958',"Bees Wax: 0.958 g/cm³", ""),
            ('0.97', "Carnauba Wax: 0.97 g/cm³", ""),
            ('0.99822',"Water : 0.99822g/cm³", ""),
            ('0.999972',"Water : 0.999972 g/cm³", ""),
            ('0',"Custom", ""),
        ]
    )
    
    float_value: bpy.props.FloatProperty(
        name="Density Value",
        default=0.00,
        description="Enter a Density value",
        min=0.00,
        max=100.00
    )


class OBJECT_OT_CalculateDensityAndWeight(bpy.types.Operator):
    bl_idname = "object.calculate_density_weight"
    bl_label = "Calculate Density and Weight"
    bl_description = "Calculate the density and weight of the selected object or all objects in the collection based on their material"

    def calculate_volume(self, obj):
        # Create a bmesh from the object
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.transform(obj.matrix_world)
        volume = bm.calc_volume()
        bm.free()
        return volume

    def calculate_density_and_weight(self, obj, material):
        volume = self.calculate_volume(obj)  # Volume in cubic meters
        volume_cm3 = volume * 1e6  # Convert volume to cubic centimeters (cm³)
        density = densities[material]
        mass = density * volume_cm3  # Mass in grams
        return density, mass

    def execute(self, context):
        scene = context.scene
        props = scene.density_calculator_props
        material = props.material

        if props.calculate_all:
            collection = bpy.context.view_layer.active_layer_collection.collection
            for obj in collection.objects:
                if obj.type == 'MESH':
                    density, weight = self.calculate_density_and_weight(obj, material)
                    if material == 'Gold':
                        self.report({'INFO'}, f"Weight of {obj.name} (Material: {material}): {weight:.2f} g")
                        print(f"Weight of {obj.name} (Material: {material}): {weight:.2f} g")
                    self.report({'INFO'}, f"Density of {obj.name} (Material: {material}): {density:.2f} g/cm³")
                    print(f"Density of {obj.name} (Material: {material}): {density:.2f} g/cm³")
        else:
            obj = context.object
            if not obj or obj.type != 'MESH':
                self.report({'ERROR'}, "No mesh object selected")
                return {'CANCELLED'}
            
            density, weight = self.calculate_density_and_weight(obj, material)
            if material == 'Gold':
                self.report({'INFO'}, f"Weight of {obj.name} (Material: {material}): {weight:.2f} g")
                print(f"Weight of {obj.name} (Material: {material}): {weight:.2f} g")
            self.report({'INFO'}, f"Density of {obj.name} (Material: {material}): {density:.2f} g/cm³")
            print(f"Density of {obj.name} (Material: {material}): {density:.2f} g/cm³")

        return {'FINISHED'}

class OBJECT_PT_DensityCalculatorPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_density_calculator"
    bl_label = "Density and Weight "
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'W3d Gold'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.density_calculator_props
        obj = context.object
        
        layout.prop(props, "material", text="Material")
        if obj:
            if float(scene.density_calculator_props.material)!=0:
                den = float(scene.density_calculator_props.material)
                layout.label(text=f"Object: {obj.name}")   
                row = layout.row()         
                row.label(text="Weight: {:.2f} g".format(All_Weight(den,context)))
                dimensions = get_dimensions(obj)
                width, length, height = dimensions
                row.label(text="Width: {:.2f} mm".format(width))
                row = layout.row(align=True)
                row.label(text="Height: {:.2f} mm".format(height))
                row.label(text="length: {:.2f} mm".format(length))
            elif  float(scene.density_calculator_props.material)==0:
                den =scene.density_calculator_props.float_value
                layout.prop(props, "float_value")
                layout.label(text=f"Object: {obj.name}")   
                row = layout.row()         
                row.label(text="Weight: {:.2f} g".format(All_Weight(den,context)))
                dimensions = get_dimensions(obj)
                width, length, height = dimensions
                row.label(text="Width: {:.2f} mm".format(width))
                row = layout.row(align=True)
                row.label(text="Height: {:.2f} mm".format(height))
                row.label(text="length: {:.2f} mm".format(length))
        else:
            layout.label(text="No object selected")
        layout.prop(props, "calculate_all", text="Calculate for All Objects")
        

def register():
    bpy.utils.register_class(DensityCalculatorProperties)
    bpy.utils.register_class(OBJECT_OT_CalculateDensityAndWeight)
    bpy.utils.register_class(OBJECT_PT_DensityCalculatorPanel)

    bpy.types.Scene.density_calculator_props = bpy.props.PointerProperty(type=DensityCalculatorProperties)

def unregister():
    bpy.utils.unregister_class(DensityCalculatorProperties)
    bpy.utils.unregister_class(OBJECT_OT_CalculateDensityAndWeight)
    bpy.utils.unregister_class(OBJECT_PT_DensityCalculatorPanel)

    del bpy.types.Scene.density_calculator_props

if __name__ == "__main__":
    register()

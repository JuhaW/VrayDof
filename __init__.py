bl_info = {
	"name": "Vray Preserve exposure using DOF",
	"author": "JuhaW",
	"version": (0, 1, 0),
	"blender": (2, 78, 4),
	"location": "Tools",
	"description": "Vray for Blender, preserve exposure using DOF",
	"warning": "beta",
	"wiki_url": "",
	"category": "",
}


import imp
import sys, os
import bpy
from math import log
from bpy.props import IntProperty, IntVectorProperty, StringProperty, BoolProperty, PointerProperty, BoolVectorProperty, EnumProperty

#os.system('cls')
#print ("reloading files...")
class ExposurePanel():
	
	exposure = 0
	f_number = 8
	shutter_speed = 300
	
def ExposureDraw(self, context):
	
	layout = self.layout

	sce = context.scene

	# Camera, active
	cam = sce.camera.data.vray.CameraPhysical
	#box = layout.box()
	#row = box.row()
	
	if sce.Camera and cam.use:
		row = layout.row()
		#row.prop(sce, "Camera_Preserve_Exposure", "Preserve Exposure")
		row.prop(sce, "f_number")
		row.label("Shutter:" + str(round(cam.shutter_speed,2)))
		row = layout.row()
		row.operator('exposure.get','Use current values',icon = 'HAND')
		row.operator('exposure.set','Restore original values',icon = 'STYLUS_PRESSURE')
		
		row = layout.row(align = False)
		row.alignment = 'LEFT'
		row.label("Based:")
		#row = layout.row(align = True)
		row.label("F-stop: " + str(round(ExposurePanel.f_number,2)))
		row.label("Shutter Speed: " + str(round(ExposurePanel.shutter_speed,2)))
			

			
class ExposureSet(bpy.types.Operator):
	bl_idname = "exposure.set"
	bl_label = "Exposure set original values"
	bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
	bl_description = "Restore F-Stop and Shutter Speed values"
		
	def execute(self, context):
	
		context.scene.camera.data.vray.CameraPhysical.f_number = ExposurePanel.f_number
		context.scene.camera.data.vray.CameraPhysical.shutter_speed = ExposurePanel.shutter_speed
		context.scene.f_number = ExposurePanel.f_number
		return {'FINISHED'}

					
class ExposureGet(bpy.types.Operator):
	bl_idname = "exposure.get"
	bl_label = "Exposure get values"
	bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
	bl_description = "Use current F-Stop and Shutter Speed values as base"
		
	def execute(self, context):
	
		ExposurePanel.f_number = context.scene.camera.data.vray.CameraPhysical.f_number
		ExposurePanel.shutter_speed = context.scene.camera.data.vray.CameraPhysical.shutter_speed
		context.scene.f_number = ExposurePanel.f_number
		return {'FINISHED'}

		
# -------------------------------------------------------------------------------
def exposure(self, context):
	scene = bpy.context.scene
	CameraPhysical = scene.camera.data.vray.CameraPhysical

	
	shutter = CameraPhysical.shutter_speed
	
	CameraPhysical.f_number
	#1 fstop alkuperäinen vertailuarvo = 8
	#2 fstop uusi arvo
	ape1 = round(log(round(pow(ExposurePanel.f_number, 2), 2), 2), 1)
	ape2 = round(log(round(pow(scene.f_number, 2), 2), 2), 1)
	# print ("ape1",ape1)
	# print ("ape2",ape2)
	CameraPhysical.shutter_speed = round(ExposurePanel.shutter_speed * (pow(2, ape1 - ape2)))

	CameraPhysical.f_number = round(scene.f_number, 2)

# -------------------------------------------------------------------------------
def Camera_Preserve_Exposure_update(self, context):
	
	sce = bpy.context.scene
	print ("Camera_Preserve_Exposure_update")
	

def register():
	bpy.utils.register_module(__name__)

	bpy.types.Scene.Camera = bpy.props.BoolProperty(default=True)
	bpy.types.Scene.Camera_Preserve_Exposure = bpy.props.BoolProperty(default=False, update =Camera_Preserve_Exposure_update)
	bpy.types.Scene.shutter_speed = bpy.props.FloatProperty(name="Shutter Speed", default=500.0, precision=2,
		options={'HIDDEN'}, subtype='NONE', unit='NONE')
	bpy.types.Scene.f_number = bpy.props.FloatProperty(name="F-Stop", default=8.0, precision=2, min = 0.1,update=exposure)
	
	#ExposureGet.execute(1,bpy.context)
	
	#bpy.types.VRAY_DP_tools.append(Material.Vray_tools_panel)
	bpy.types.VRAY_DP_physical_camera.append(ExposureDraw)

def unregister():
	bpy.utils.unregister_module(__name__)

	del bpy.types.Scene.Camera
	del bpy.types.Scene.Camera_Preserve_Exposure
	# del bpy.types.Scene.Cam_exposure
	del bpy.types.Scene.f_number
	del bpy.types.Scene.shutter_speed

	#bpy.types.VRAY_DP_tools.remove(Material.Vray_tools_panel)
	bpy.types.VRAY_DP_physical_camera.remove(ExposureDraw)
	
if __name__ == "__main__":
	register()



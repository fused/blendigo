import bpy

from .. core import BL_IDNAME
class INDIGO_PT_ui_render_engine_settings(bpy.types.Panel):
    bl_label = "Indigo Engine"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == BL_IDNAME
    
    def draw(self, context):
        indigo_engine = context.scene.indigo_engine
        layout = self.layout
        col = layout.column()
        col.prop(indigo_engine, 'render_mode')
        
        if indigo_engine.render_mode == 'custom':
            col.label(text="Custom Options:")
            box = col.box()
            sub = box.column()
            row = sub.row()
            
            sc = row.column()
            sc.prop(indigo_engine, 'gpu')
            sc.prop(indigo_engine, 'bidir')
            sc.prop(indigo_engine, 'metro')
            
            if not indigo_engine.gpu:
                box = col.box()
                sub = box.column()
                sub.prop(indigo_engine, 'max_depth')

            if indigo_engine.metro:
                col.label(text="Metropolis Settings:")
                box = col.box()
                sub = box.column()
                sub.prop(indigo_engine, 'large_mutation_prob')
                sub.prop(indigo_engine, 'max_change')
                sub.prop(indigo_engine, 'max_num_consec_rejections')

            sc = row.column()
            sc.prop(indigo_engine, 'shadow')

        if indigo_engine.gpu:
            col.label(text="GPU Settings:")
            box = col.box()
            sub = box.column()
            sub.prop(indigo_engine, 'gpu_max_depth')
            sub.prop(indigo_engine, 'compress_textures')
            
        col.separator()
        
        #### TODO clamping, max contrib
        box = col.box()
        row = box.row()
        row.prop(indigo_engine, 'clamp_contributions')
        sub = row.row()
        if not indigo_engine.clamp_contributions:
            sub.active = False
        sub.prop(indigo_engine, 'max_contribution')
        
        
        col.label(text="Filter Settings:")
        box = col.box()
        sub = box.column()
        sub.prop(indigo_engine, 'supersample')
        sub.prop(indigo_engine, 'filter_preset')
        if indigo_engine.filter_preset == 'custom':
            sub.prop(indigo_engine, 'splat_filter')
            if indigo_engine.splat_filter == 'mitchell':
                sb = sub.row(align=True)
                sb.prop(indigo_engine, 'splat_filter_blur')
                sb.prop(indigo_engine, 'splat_filter_ring')
            sub.prop(indigo_engine, 'ds_filter')
            if indigo_engine.ds_filter == 'mitchell':
                sb = sub.row(align=True)
                sb.prop(indigo_engine, 'ds_filter_blur', text="Blur")
                sb.prop(indigo_engine, 'ds_filter_ring', text="Ring")
                sb.prop(indigo_engine, 'ds_filter_radius', text="Radius")     

        col.label(text="Denoising Settings:")
        box = col.box()
        sub = box.column()
        row = sub.row()
        sc = row.column()
        sc.prop(indigo_engine, 'optimise_for_denoising')
        sc.prop(indigo_engine, 'denoise')

        col.label(text="Misc. Settings:")
        box = col.box()
        sub = box.column()
        row = sub.row()
        sc = row.column()
        sc.prop(indigo_engine, 'motionblur')
        sc.prop(indigo_engine, 'foreground_alpha')    
        
        col = layout.column()
        col.separator()
        
        col.label(text="Halt Settings:")
        box = col.box()
        sub = box.column()
        sr = sub.row(align=True)
        sr.prop(indigo_engine, 'halttime')
        sr.prop(indigo_engine, 'haltspp')
        sr = sub.row()
        sr.prop(indigo_engine, 'period_save')
        
        col = layout.column()
        col.separator()
        
        col.label(text="System Settings:")
        box = col.box()
        sub = box.column()
        sr = sub.row()
        sr.prop(indigo_engine, 'threads_auto')
        rc = sr.column()
        rc.prop(indigo_engine, 'threads')
        rc.enabled = not indigo_engine.threads_auto
        sub.prop(indigo_engine, 'network_mode')
        if indigo_engine.network_mode != 'off':
            sub.prop(indigo_engine, 'network_port')
        
        col.separator()
        row = col.row()
        row.prop(indigo_engine, 'auto_start')
        row.prop(indigo_engine, 'console_output', text="Print to console")
        
        ##
        from .. properties.render_settings import IndigoDevice
        
        col = col.column(align=True)
        col.label(text="Render Devices:")
        for d in indigo_engine.render_devices:
            col.prop(d, 'use', text=d.platform+' '+d.device, toggle=True)
        col.operator('indigo.refresh_computing_devices')
            
class INDIGO_OT_refresh_computing_devices(bpy.types.Operator):
    bl_idname = "indigo.refresh_computing_devices"
    bl_label = "Refresh Computing Devices"
    bl_description = ""
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        from .. properties.render_settings import get_render_devices
        get_render_devices(True)
        context.scene.indigo_engine.refresh_device_collection()
        return {"FINISHED"}
        
            
        
        
class INDIGO_PT_ui_render_export_settings(bpy.types.Panel):
    bl_label = "Export Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == BL_IDNAME
    
    def draw(self, context):
        indigo_engine = context.scene.indigo_engine
        layout = self.layout
        col = layout.column()
        col.prop(indigo_engine, 'use_output_path')
        col = layout.column()
        col.prop(indigo_engine, 'export_path')
        col.enabled = not indigo_engine.use_output_path
        col = layout.column()
        col.prop(indigo_engine, 'install_path')
        col.prop(indigo_engine, 'skip_existing_meshes')
        
        col.separator()
        
        col.label(text="Output Settings:")
        box = col.box()
        sub = box.column()
        row = sub.row()
        
        sc = row.column()
        sc.prop(indigo_engine, 'save_exr_utm')
        sc.prop(indigo_engine, 'save_exr_tm')
        sc.prop(indigo_engine, 'save_igi')
        sc.prop(indigo_engine, 'save_render_channels_exr')
        
        sc = row.column()
        sc.prop(indigo_engine, 'ov_watermark')
        sc.prop(indigo_engine, 'ov_info')
        sc.prop(indigo_engine, 'logging')


        # sub-options

        if indigo_engine.save_igi:
            box = col.box()
            sub = box.column()
            row = sub.row()
            
            sc = row.column()
            sc.prop(indigo_engine, 'igi_timestamp_filename')
        

class INDIGO_PT_ui_render_render_channels(bpy.types.Panel):
    bl_label = "Render Channels"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == BL_IDNAME

    def draw(self, context):
        indigo_engine = context.scene.indigo_engine
        layout = self.layout

        sub = layout.column()
        row = sub.row()

        sc = row.column()
        sc.prop(indigo_engine, 'channel_beauty')
        sc.prop(indigo_engine, 'channel_albedo')
        sc.prop(indigo_engine, 'channel_normals')
        sc.prop(indigo_engine, 'channel_normals_pre_bump')
        sc.prop(indigo_engine, 'channel_depth')
        sc.prop(indigo_engine, 'channel_position')
        sc.prop(indigo_engine, 'channel_material_id')
        sc.prop(indigo_engine, 'channel_object_id')
        sc.prop(indigo_engine, 'channel_alpha')
        sc.prop(indigo_engine, 'channel_material_mask')
        sc.prop(indigo_engine, 'channel_object_mask')

        sc = row.column()
        sc.prop(indigo_engine, 'channel_direct_lighting')
        sc.prop(indigo_engine, 'channel_indirect_lighting')
        sc.prop(indigo_engine, 'channel_specular_reflection_lighting')
        sc.prop(indigo_engine, 'channel_refraction_lighting')
        sc.prop(indigo_engine, 'channel_transmission_lighting')
        sc.prop(indigo_engine, 'channel_emission_lighting')
        sc.prop(indigo_engine, 'channel_participating_media_lighting')
        sc.prop(indigo_engine, 'channel_sss_lighting')
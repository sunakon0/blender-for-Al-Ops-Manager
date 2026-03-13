import bpy
import os

class AIOPS_PT_main_panel(bpy.types.Panel):
    bl_label = "AI-Ops 资产管家"
    bl_idname = "AIOPS_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI-Ops'

    def draw(self, context):
        layout = self.layout
        props = context.scene.ai_ops_props
        pref = context.preferences.addons[__package__].preferences
        
        # --- 1. 常用脚本库 (第一栏) ---
        layout.label(text="📚 常用脚本库", icon='ASSET_MANAGER')
        box = layout.box()
        
        # 获取保存路径
        script_path = bpy.path.abspath(pref.script_save_path)
        
        if os.path.exists(script_path):
            files = [f for f in os.listdir(script_path) if f.endswith(".py")]
            if not files:
                box.label(text="暂无保存的脚本", icon='INFO')
            else:
                col = box.column(align=True)
                for f in files:
                    row = col.row()
                    # 去掉 .py 后缀显示
                    display_name = f.replace(".py", "")
                    row.label(text=display_name)
                    # 运行按钮
                    op = row.operator("aiops.run_library_script", text="", icon='PLAY')
                    op.filename = f
        else:
            box.label(text="路径未配置或不存在", icon='ERROR')
            box.operator("aiops.open_folder", text="创建/打开文件夹")

        layout.separator()

        # --- 2. AI 核心功能 (第二栏) ---
        layout.label(text="🤖 AI 编码助手", icon='SHADING_RENDERED')
        
        # 生成区
        box_gen = layout.box()
        
        # 任务模式选择
        row_mode = box_gen.row()
        row_mode.prop(props, "task_category", text="") 
        
        # 动态提示信息 (根据模式变化)
        if props.task_category == 'MODEL':
            box_gen.label(text="* 专注：选中物体、Mesh数据、坐标变换", icon='MESH_DATA')
        elif props.task_category == 'MATERIAL':
            box_gen.label(text="* 专注：节点连线、材质槽、BSDF", icon='NODETREE')
        elif props.task_category == 'OUTLINER':
            box_gen.label(text="* 专注：集合分类、层级移动、命名", icon='OUTLINER_COLLECTION')
        elif props.task_category == 'ANIMATION':
            box_gen.label(text="* 专注：关键帧、F-Curve、动作", icon='ACTION')
        
        # 输入框
        col = box_gen.column()
        # --- 修复点：移除了 placeholder 参数以兼容 Blender 3.6 ---
        col.prop(props, "ai_prompt", text="") 
        
        # 操作按钮
        row_btns = box_gen.row(align=True)
        row_btns.operator("aiops.generate_code", icon='IMPORT', text="生成脚本")
        row_btns.operator("aiops.run_script", icon='PLAY', text="立即运行")
        
        # --- 3. 报错修复区 (第三栏) ---
        layout.separator()
        box_fix = layout.box()
        box_fix.label(text="🛠️ 报错修复中心", icon='MODIFIER')
        
        row_log = box_fix.row(align=True)
        row_log.prop(props, "error_log_pointer", text="") # 显示选中的文本块
        row_log.operator("aiops.create_error_log", text="", icon='ADD') # 新建按钮
        
        # 修复按钮
        fix_op = box_fix.operator("aiops.fix_code", text="提交报错并智能修复", icon='RECOVER_LAST')
        
        # 提示用户操作
        if not props.error_log_pointer:
            col_tip = box_fix.column(align=True)
            col_tip.scale_y = 0.8
            col_tip.label(text="1. 点击 + 号创建日志块", icon='SMALL_TRI_RIGHT_IND')
            col_tip.label(text="2. 粘贴控制台报错信息", icon='SMALL_TRI_RIGHT_IND')

        layout.separator()

        # --- 4. 保存与管理 (底部) ---
        sub_box = layout.box()
        sub_box.label(text="保存当前脚本:", icon='FILE_TICK')
        row_save = sub_box.row(align=True)
        row_save.prop(props, "script_name_to_save", text="")
        row_save.operator("aiops.save_to_library", text="保存", icon='CHECKMARK')
        
        layout.separator()
        layout.operator("aiops.open_folder", text="打开脚本文件夹", icon='FILE_FOLDER')

# 注册
def register():
    bpy.utils.register_class(AIOPS_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(AIOPS_PT_main_panel)
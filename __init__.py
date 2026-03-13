bl_info = {
    "name": "AI-Ops Manager2",
    "author": "Guo Yuchao & AI",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > AI-Ops",
    "description": "基于 DeepSeek-R1 的智能 Blender 脚本生成与修复工具",
    "category": "System",
}

import bpy
from . import ui, operators

# --- 插件偏好设置 (用于存 API Key) ---
class AIOpsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    api_key: bpy.props.StringProperty(
        name="DeepSeek API Key",
        subtype='PASSWORD',
        description="请输入你的 DeepSeek API Key (sk-...)",
    )
    
    script_save_path: bpy.props.StringProperty(
        name="脚本库保存路径",
        subtype='DIR_PATH',
        default="//ai_scripts_library/",
        description="本地常用脚本的保存位置 (相对路径或绝对路径)"
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="配置中心", icon='PREFERENCES')
        box = layout.box()
        box.prop(self, "api_key")
        box.prop(self, "script_save_path")
        box.label(text="* 建议使用 DeepSeek-reasoner 模型以获得最佳逻辑能力", icon='INFO')

# --- 注册 ---
def register():
    bpy.utils.register_class(AIOpsPreferences)
    ui.register()
    operators.register()

def unregister():
    operators.unregister()
    ui.unregister()
    bpy.utils.unregister_class(AIOpsPreferences)
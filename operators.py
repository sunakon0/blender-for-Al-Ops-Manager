import bpy
import os
import traceback # 引入这个以获取更详细的报错
from . import utils

# --- 0. 专家级防错提示词库 (Context Injection) ---
CONTEXT_PROMPTS = {
    'GENERAL': (
        "Context: General Blender Scripting.\n"
        "Constraint: Ensure the script handles context correctly and imports 'bpy'."
    ),
    'MODEL': (
        "Context: Selected Object Manipulation (Mesh/Curve/Transform).\n"
        "Constraints:\n"
        "1. Iterate through `bpy.context.selected_objects`.\n"
        "2. Check `obj.type` (e.g., if obj.type == 'MESH') before accessing mesh data.\n"
        "3. Ensure `bpy.ops.object.mode_set(mode='OBJECT')` is called at the very start.\n"
        "4. Avoid `bpy.ops` for heavy geometry processing; use `bmesh` if possible."
    ),
    'MATERIAL': (
        "Context: Material & Shader Node Manipulation (Principled BSDF).\n"
        "Constraints:\n"
        "1. Work on `obj.active_material`. Always check `if not obj.active_material: return`.\n"
        "2. Ensure `mat.use_nodes = True`.\n"
        "3. Find the BSDF node by Type `ShaderNodeBsdfPrincipled`, NOT just by name 'Principled BSDF'.\n"
        "4. Use `nodes.new()` and `links.new()` for connections.\n"
        "5. Do NOT use `material.diffuse_color` for nodes; access the BSDF input socket."
    ),
    'OUTLINER': (
        "Context: Outliner, Collections, and Hierarchy Management.\n"
        "Constraints:\n"
        "1. Use `bpy.data.collections` for management.\n"
        "2. When linking/unlinking, check `if obj.name in col.objects` to avoid 'Already in collection' errors.\n"
        "3. Handle recursive hierarchy if moving objects between collections.\n"
        "4. STRICTLY AVOID `bpy.ops.outliner` operators as they require specific mouse context; use direct data API."
    ),
    'ANIMATION': (
        "Context: Animation, F-Curves, and Action Batch Processing.\n"
        "Constraints:\n"
        "1. Check if `obj.animation_data` and `obj.animation_data.action` exist.\n"
        "2. Iterate through `action.fcurves`.\n"
        "3. Use `keyframe_points` for batch editing values.\n"
        "4. If setting frame range, use `bpy.context.scene.frame_start`."
    )
}

# --- 1. 全局属性定义 ---
class AIOpsProperties(bpy.types.PropertyGroup):
    task_category: bpy.props.EnumProperty(
        name="任务类型",
        description="选择脚本针对的领域，AI将自动加载防错规则",
        items=[
            ('GENERAL', "通用模式", "不预设特定规则", 'WORLD', 0),
            ('MODEL', "模型处理", "针对选中物体、网格、变换", 'MESH_CUBE', 1),
            ('MATERIAL', "材质节点", "针对BSDF、贴图连接", 'NODE_MATERIAL', 2),
            ('OUTLINER', "大纲整理", "针对集合、层级、命名", 'OUTLINER', 3),
            ('ANIMATION', "动画批处理", "针对关键帧、动作", 'ACTION', 4),
        ],
        default='GENERAL'
    )
    
    ai_prompt: bpy.props.StringProperty(
        name="AI 指令",
        description="描述具体需求",
        default=""
    )
    
    script_name_to_save: bpy.props.StringProperty(
        name="脚本命名",
        description="保存到库时的名称",
        default="My_New_Tool"
    )
    
    error_log_pointer: bpy.props.PointerProperty(
        name="错误日志",
        type=bpy.types.Text,
        description="选择包含报错信息的文本块"
    )

# --- 2. 核心操作符 ---

class AIOPS_OT_generate_code(bpy.types.Operator):
    """发送指令给 DeepSeek 并生成代码"""
    bl_idname = "aiops.generate_code"
    bl_label = "生成脚本"
    
    def execute(self, context):
        props = context.scene.ai_ops_props
        api_key = utils.get_api_key(context)
        
        if not api_key:
            self.report({'ERROR'}, "请先在插件设置中配置 API Key")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"AI正在根据 [{props.task_category}] 模式思考...")
        
        prefix_prompt = CONTEXT_PROMPTS.get(props.task_category, "")
        final_prompt = (
            f"{prefix_prompt}\n\n"
            f"User Task: {props.ai_prompt}"
        )
        
        raw_response = utils.call_deepseek_api(final_prompt, api_key)
        clean_code = utils.clean_ai_code(raw_response)
        
        text_name = "AI_Generated_Script.py"
        text_block = bpy.data.texts.get(text_name)
        if not text_block:
            text_block = bpy.data.texts.new(text_name)
        
        text_block.clear()
        text_block.write(clean_code)
        
        self.report({'INFO'}, "代码已生成至文本编辑器！")
        return {'FINISHED'}

class AIOPS_OT_fix_code(bpy.types.Operator):
    """读取当前脚本和错误日志，请求 AI 修复"""
    bl_idname = "aiops.fix_code"
    bl_label = "根据报错修复脚本"
    
    def execute(self, context):
        props = context.scene.ai_ops_props
        api_key = utils.get_api_key(context)
        
        script_text = bpy.data.texts.get("AI_Generated_Script.py")
        if not script_text:
            self.report({'ERROR'}, "找不到脚本 AI_Generated_Script.py")
            return {'CANCELLED'}
        bad_code = script_text.as_string()
        
        error_ptr = props.error_log_pointer
        if not error_ptr:
            error_ptr = bpy.data.texts.get("Error_Log")
            
        if not error_ptr or not error_ptr.as_string().strip():
            self.report({'ERROR'}, "请先创建或选择一个包含报错信息的文本块")
            return {'CANCELLED'}
            
        error_log = error_ptr.as_string()
        
        fix_prompt = (
            f"The following Blender Python script produced an error.\n\n"
            f"### BROKEN SCRIPT:\n```python\n{bad_code}\n```\n\n"
            f"### ERROR LOG:\n{error_log}\n\n"
            f"### TASK:\n"
            f"Analyze the traceback. Explain specifically what went wrong, then provide the FIXED full script.\n"
        )
        
        self.report({'INFO'}, "正在请求 AI 修复...")
        
        raw_response = utils.call_deepseek_api(fix_prompt, api_key)
        fixed_code = utils.clean_ai_code(raw_response)
        
        script_text.clear()
        script_text.write(fixed_code)
        
        self.report({'INFO'}, "脚本已修复！请再次运行。")
        return {'FINISHED'}

class AIOPS_OT_create_error_log(bpy.types.Operator):
    """创建一个空的 Error_Log 文本块"""
    bl_idname = "aiops.create_error_log"
    bl_label = "新建报错文本块"
    
    def execute(self, context):
        text_name = "Error_Log"
        text = bpy.data.texts.get(text_name)
        if not text:
            text = bpy.data.texts.new(text_name)
        
        context.scene.ai_ops_props.error_log_pointer = text
        self.report({'INFO'}, f"已创建 '{text_name}'，请粘贴报错")
        return {'FINISHED'}

# --- 关键修改区域：运行脚本的逻辑优化 ---

class AIOPS_OT_run_current_script(bpy.types.Operator):
    """运行当前文本编辑器中的 AI_Generated_Script.py"""
    bl_idname = "aiops.run_script"
    bl_label = "运行脚本"
    
    def execute(self, context):
        text_name = "AI_Generated_Script.py"
        text_block = bpy.data.texts.get(text_name)
        
        if text_block:
            try:
                # 1. 准备运行环境 (Namespace)
                # 必须明确指定 __name__ 为 __main__，否则 if __name__ == '__main__': 里的代码不会跑
                namespace = {
                    "__builtins__": __builtins__,
                    "bpy": bpy,
                    "context": context,
                    "__name__": "__main__"  # <--- 这行是修复的核心！
                }
                
                # 2. 执行代码
                exec(text_block.as_string(), namespace)
                
                # 3. 强制刷新视图 (防止脚本跑完了但画面没变)
                if context.view_layer:
                    context.view_layer.update()
                for area in context.screen.areas:
                    area.tag_redraw()
                    
                self.report({'INFO'}, "运行成功")
                
            except Exception as e:
                # 打印详细报错到控制台，方便调试
                traceback.print_exc()
                self.report({'ERROR'}, f"运行失败: {e}")
        else:
            self.report({'WARNING'}, "未找到生成的脚本")
        return {'FINISHED'}

class AIOPS_OT_save_to_library(bpy.types.Operator):
    """保存为本地库文件"""
    bl_idname = "aiops.save_to_library"
    bl_label = "保存为常用功能"
    
    def execute(self, context):
        props = context.scene.ai_ops_props
        pref = context.preferences.addons[__package__].preferences
        
        base_path = bpy.path.abspath(pref.script_save_path)
        if not os.path.exists(base_path):
            try:
                os.makedirs(base_path)
            except OSError:
                self.report({'ERROR'}, "无法创建保存路径")
                return {'CANCELLED'}
            
        filename = f"{props.script_name_to_save}.py"
        filepath = os.path.join(base_path, filename)
        
        text_block = bpy.data.texts.get("AI_Generated_Script.py")
        if text_block:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text_block.as_string())
            self.report({'INFO'}, f"已保存: {filename}")
            context.region.tag_redraw() 
        return {'FINISHED'}

class AIOPS_OT_run_library_script(bpy.types.Operator):
    """运行库里的某个脚本"""
    bl_idname = "aiops.run_library_script"
    bl_label = "运行库脚本"
    
    filename: bpy.props.StringProperty()
    
    def execute(self, context):
        pref = context.preferences.addons[__package__].preferences
        base_path = bpy.path.abspath(pref.script_save_path)
        filepath = os.path.join(base_path, self.filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # 同样应用修复逻辑
                namespace = {
                    "__builtins__": __builtins__,
                    "bpy": bpy,
                    "context": context,
                    "__name__": "__main__" # <--- 同样修复这里
                }
                
                exec(code, namespace)
                
                # 强制刷新
                if context.view_layer:
                    context.view_layer.update()
                for area in context.screen.areas:
                    area.tag_redraw()
                    
                self.report({'INFO'}, f"已执行: {self.filename}")
            except Exception as e:
                traceback.print_exc()
                self.report({'ERROR'}, f"脚本出错: {e}")
        return {'FINISHED'}

class AIOPS_OT_open_folder(bpy.types.Operator):
    """打开脚本保存文件夹"""
    bl_idname = "aiops.open_folder"
    bl_label = "打开外部文件夹"
    
    def execute(self, context):
        pref = context.preferences.addons[__package__].preferences
        path = bpy.path.abspath(pref.script_save_path)
        if not os.path.exists(path):
            os.makedirs(path)
        bpy.ops.wm.path_open(filepath=path)
        return {'FINISHED'}

# --- 注册 ---
classes = (
    AIOpsProperties,
    AIOPS_OT_generate_code,
    AIOPS_OT_fix_code,
    AIOPS_OT_create_error_log,
    AIOPS_OT_run_current_script,
    AIOPS_OT_save_to_library,
    AIOPS_OT_run_library_script,
    AIOPS_OT_open_folder,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ai_ops_props = bpy.props.PointerProperty(type=AIOpsProperties)

def unregister():
    del bpy.types.Scene.ai_ops_props
    for cls in classes:
        bpy.utils.unregister_class(cls)
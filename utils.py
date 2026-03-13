import bpy
import json
import urllib.request
import re
import socket

# --- 关键设置：设置全局超时时间 ---
# 推理模型 (Reasoning Models) 需要更长的思考时间
# 如果不设置这个，Blender 默认 socket 可能会在 AI 回复前断开
socket.setdefaulttimeout(120) 

def get_api_key(context):
    preferences = context.preferences.addons[__package__].preferences
    return preferences.api_key

def clean_ai_code(response_text):
    """
    从 AI 回复中提取 python 代码块。
    DeepSeek-R1 可能会在代码前后包含推理过程或 Markdown 标记，
    此函数只提取 ```python ... ``` 之间的纯代码。
    """
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    if matches:
        # 如果找到代码块，返回第一个（通常是最终代码）
        return matches[0].strip()
    
    # 兜底：如果 AI 没有使用 markdown 包裹，尝试清洗首尾空白直接返回
    # 但对于 reasoner 模型，通常建议严格匹配代码块
    return response_text.strip()

def call_deepseek_api(user_prompt, api_key):
    url = "https://api.deepseek.com/chat/completions"
    
    # 获取当前 Blender 版本，让 AI 写出兼容的代码
    bl_version = bpy.app.version
    ver_str = f"{bl_version[0]}.{bl_version[1]}"
    
    # --- 构造 Prompt ---
    # 由于 deepseek-reasoner 不支持 System Role，我们将所有要求放入 User Role
    full_prompt = (
        f"You are an expert Blender Python (bpy) developer.\n"
        f"Target Blender Version: {ver_str}+\n\n"
        "STRICT REQUIREMENTS:\n"
        "1. Write a COMPLETE, runnable script.\n"
        "2. Do NOT use markdown for explanations outside the code block.\n"
        "3. Only output the Python code wrapped in ```python ... ```.\n"
        "4. Prioritize direct data access (bpy.data) over operators (bpy.ops).\n\n"
        f"TASK:\n{user_prompt}"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "deepseek-reasoner",  # 使用推理模型
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 8192, # 给予足够的推理空间
        # 注意：deepseek-reasoner 不支持 temperature 参数，请勿添加
    }

    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'), 
            headers=headers
        )
        
        # 发送请求 (这会阻塞 UI 线程，直到 AI 返回)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # --- 解析 DeepSeek 返回结构 ---
            # reasoner 模型可能会返回 'reasoning_content' (思考过程)
            # 我们只需要最终的 content
            choices = result.get('choices', [])
            if not choices:
                return "# Error: No choices in response"
                
            message = choices[0].get('message', {})
            content = message.get('content', "")
            
            if not content:
                return "# Error: Empty content from AI"
                
            return content

    except urllib.error.URLError as e:
        return f"# Network Error: {e.reason}"
    except json.JSONDecodeError:
        return "# Error: Invalid JSON response"
    except Exception as e:
        return f"# Error: {str(e)}"
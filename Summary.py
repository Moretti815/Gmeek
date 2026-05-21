import os
import requests
import json
import random
"""
在仓库的 Settings > Secrets and variables > Actions 中添加密钥：
"""
def generate_summary(text):
    # 配置参数
    api_url = os.environ.get("API_URL")
    api_key = os.environ.get("API_KEY")
    api_model = os.environ.get("API_MODEL")

    # 调试信息：检查环境变量
    print(f"[AI Summary] API_URL: {'已配置' if api_url else '未配置'}")
    print(f"[AI Summary] API_KEY: {'已配置' if api_key else '未配置'}")
    print(f"[AI Summary] API_MODEL: {api_model if api_model else '未配置'}")

    if not api_url or not api_model:
        print("[AI Summary] 配置不完整，跳过 AI 摘要生成")
        return ""

    # 支持配置多个api_key和api_model
    if api_key and ',' in api_key:
        api_key = random.choice(api_key.split(','))

    if api_model and ',' in api_model:
        api_model = random.choice(api_model.split(','))

    print(f"[AI Summary] 使用模型: {api_model}")
    print(f"[AI Summary] 文本长度: {len(text)} 字符")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = "你是总结生成器。你的任务是以简洁、完整的语句总结用户提供的文本，捕捉主要要点，并指出改进建议，不使用Markdown格式，直接返回内容，避免空话或截断，以'本文介绍了'开头。"

    payload = {
        "model": f"{api_model}",
        "messages": [
            {"role": "system", "content": f"{prompt}"},
            {"role": "user", "content": f"{text}"}
        ],
        "temperature": 0.5,
        "max_tokens": 1500
    }

    try:
        print(f"[AI Summary] 正在发送请求到: {api_url}")
        response = requests.post(
            url=api_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            print(f"[AI Summary] 生成成功，摘要长度: {len(result)} 字符")
            print(f"[AI Summary] 摘要预览: {result[:100]}...")
            return result
        else:
            print(f"[AI Summary] 请求失败：{response.status_code} - {response.text}")
            return ""

    except Exception as e:
        print(f"[AI Summary] 发生异常：{str(e)}")
        return ""

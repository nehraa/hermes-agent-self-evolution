---
category: software-development
name: tianshu-wan-video
description: 使用阿里云通义万相 2.6 模型生成视频，支持文字转视频 (t2v) 和图片转视频 (i2v)。纯 Node.js 实现，无需 Python 环境。
metadata:
  openclaw:
    primaryEnv: DASHSCOPE_API_KEY
    requires:
      env:
        - DASHSCOPE_API_KEY
---

# 通义万相视频生成 (tianshu-wan-video)

通过阿里云 DashScope API 调用通义万相 2.6 视频生成模型，支持文字描述生成视频和图片驱动生成视频。

## 环境配置

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API 密钥，从阿里云百炼平台获取 |

## 使用方法

### 文字转视频 (t2v)

根据文本描述生成视频片段：

bash
node scripts/generate_video.js t2v --prompt "电影感特写镜头，缓慢推进" --duration 5 --resolution 720P
### 图片转视频 (i2v)

基于图片生成视频动画：

bash
node scripts/generate_video.js i2v --prompt "镜头缓慢旋转" --image-url "https://example.com/image.jpg" --duration 4
## 参数说明

| 参数 | 类型 | 说明 | 可选值 |
|------|------|------|--------|
| `--prompt` | string | 视频描述文本，建议使用中文 | - |
| `--duration` | number | 视频时长（秒） | 4, 5, 10 |
| `--resolution` | string | 输出分辨率 | 540P, 720P, 1080P |

## 输出格式

执行成功后，脚本输出：

VIDEO_URL: https://xxx.aliyuncs.com/xxx.mp4
直接提取该 URL 即可使用生成的视频。

## 示例场景

bash
# 生成5秒720P产品展示视频
node scripts/generate_video.js t2v --prompt "产品360度旋转展示" --duration 5 --resolution 720P

# 将静态图片转换为动态场景
node scripts/generate_video.js i2v --prompt "微风轻拂，花瓣缓缓飘落" --image-url "https://example.com/flower.jpg" --duration 4
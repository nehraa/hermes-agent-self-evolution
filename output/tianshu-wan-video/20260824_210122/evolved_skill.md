---
category: software-development
name: tianshu-wan-video
description: 使用通义万相 2.6 生成视频，支持文生视频和图生视频。Node.js 实现，无需 Python。
metadata:
  openclaw:
    primaryEnv: DASHSCOPE_API_KEY
    requires:
      env:
        - DASHSCOPE_API_KEY
---

# 通义万相视频 (tianshu-wan-video)

调用阿里云通义万相 Wan2.6 视频生成模型，通过 Node.js 脚本生成视频。无需 Python 环境。

## 前置要求

### 环境变量

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key，从[阿里云百炼控制台](https://bailian.console.aliyun.com/)获取 |

## 用法

### 文生视频 (Text-to-Video)

根据文本描述生成视频片段。

bash
node scripts/generate_video.js t2v --prompt "电影感特写镜头，缓慢推进" --duration 5 --resolution 720P
### 图生视频 (Image-to-Video)

基于参考图片生成视频动画。

bash
node scripts/generate_video.js i2v --prompt "镜头缓慢旋转" --image-url "https://example.com/image.jpg" --duration 4
## 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--prompt` | 视频描述提示词 | 文本字符串 |
| `--duration` | 视频时长（秒） | 5（默认）、4 |
| `--resolution` | 输出分辨率 | `720P`（默认）、`1080P` |
| `--image-url` | 参考图片 URL（仅 i2v） | 有效的图片 URL |

## 输出格式

脚本执行成功后输出：

VIDEO_URL: <视频下载链接>
提取 `VIDEO_URL:` 后的链接即可下载或嵌入使用。

## 示例场景

bash
# 生成电影风格特写
node scripts/generate_video.js t2v --prompt "一位老人在老式咖啡馆窗边沉思，电影质感，暖色调光线" --duration 5 --resolution 1080P

# 动态产品展示
node scripts/generate_video.js i2v --prompt "产品 360 度旋转展示" --image-url "https://cdn.example.com/product.jpg" --duration 4
## 注意事项

- 视频生成可能需要等待数秒至数十秒
- 确保 `--image-url` 指向可公开访问的图片资源
- API 调用受阿里云 DashScope 配额限制
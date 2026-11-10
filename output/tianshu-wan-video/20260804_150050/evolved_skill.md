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

# 通义万相视频生成 (tianshu-wan-video)

调用阿里云通义万相 2.6 视频生成模型，通过简单的命令行接口生成视频。支持文生视频 (Text-to-Video) 和图生视频 (Image-to-Video) 两种模式。

## 前置要求

### 环境变量

| 变量名 | 说明 |
|--------|------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API 密钥 |

获取方式：在 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/) 开通视频生成服务并获取 API Key。

## 用法

bash
node scripts/generate_video.js <模式> [选项]
### 模式

| 模式 | 说明 |
|------|------|
| `t2v` | 文生视频 - 根据文本描述生成视频 |
| `i2v` | 图生视频 - 根据图片和文本描述生成视频 |

### 选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 视频描述文本 | 必填 |
| `--duration` | 视频时长（秒） | `5` |
| `--resolution` | 视频分辨率 | `720P` |
| `--image-url` | 参考图片 URL（仅 i2v 模式） | 必填 |

### 示例

**文生视频**

bash
node scripts/generate_video.js t2v \
  --prompt "电影感特写镜头，缓慢推进" \
  --duration 5 \
  --resolution 720P
**图生视频**

bash
node scripts/generate_video.js i2v \
  --prompt "镜头缓慢旋转" \
  --image-url "https://example.com/image.jpg" \
  --duration 4
## 输出

脚本执行成功后返回以下格式：

VIDEO_URL: https://<video-url>
提取返回的 URL 即可在播放器中预览或嵌入使用。

## 常见问题

- **API 配额**：确保账户有足够的 API 调用配额
- **图片要求**：图生视频模式需提供可访问的图片 URL，支持 JPEG、PNG 格式
- **描述优化**：详细的文本描述可获得更符合预期的视频效果
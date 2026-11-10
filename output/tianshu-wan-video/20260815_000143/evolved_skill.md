---
category: software-development
description: 使用通义万相 2.6 生成视频，支持文生视频和图生视频。Node.js 实现，无需 Python。
name: tianshu-wan-video
metadata:
  openclaw:
    primaryEnv: DASHSCOPE_API_KEY
    requires:
      env:
        - DASHSCOPE_API_KEY
---

# 通义万相视频 (tianshu-wan-video)

调用阿里云通义万相 2.6 模型生成视频。Node.js 脚本实现，无需 Python 环境。

## 支持功能

| 模式 | 说明 |
|------|------|
| `t2v` | 文生视频：根据文本描述生成视频 |
| `i2v` | 图生视频：基于图片生成动态视频 |

## 前置要求

### 环境变量

bash
export DASHSCOPE_API_KEY=your_api_key_here
在 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/) 获取 API Key。

## 使用方法

bash
# 文生视频
node scripts/generate_video.js t2v --prompt "电影感特写镜头，缓慢推进" --duration 5 --resolution 720P

# 图生视频
node scripts/generate_video.js i2v --prompt "镜头缓慢旋转" --image-url "https://example.com/image.jpg" --duration 4
## 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--duration` | 视频时长（秒） | `5`（5秒）、`10`（10秒） |
| `--resolution` | 输出分辨率 | `480P`、`720P` |
| `--prompt` | 视频描述词 | 文本描述，建议 50 字以内 |
| `--image-url` | 图片 URL（仅 i2v 模式必需） | 有效的图片 URL |

## 输出格式

脚本执行成功后输出：

VIDEO_URL: https://xxx.vfile.com/video/xxx.mp4
提取 `VIDEO_URL:` 后的 URL 即可下载或使用生成的视频。

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 缺少 `DASHSCOPE_API_KEY` | 脚本报错退出，设置环境变量后重试 |
| API 调用失败 | 脚本输出错误信息，根据提示调整参数后重试 |
| 图片 URL 无效（i2v） | 确保图片可公开访问，支持 JPG/PNG/WebP 格式 |

## 示例场景

bash
# 生成10秒720P文生视频
node scripts/generate_video.js t2v --prompt "一只橘猫在阳光下的窗台上打盹" --duration 10 --resolution 720P

# 基于产品图片生成展示视频
node scripts/generate_video.js i2v --prompt "镜头从左侧缓慢平移展示产品" --image-url "https://example.com/product.jpg" --duration 5 --resolution 720P
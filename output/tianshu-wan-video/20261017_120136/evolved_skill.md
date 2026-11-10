---
name: tianshu-wan-video
description: 使用阿里云通义万相 2.6 模型生成视频，支持文生视频（T2V）和图生视频（I2V）两种模式。基于 Node.js 实现，无需 Python 环境。
metadata:
  openclaw:
    primaryEnv: DASHSCOPE_API_KEY
    requires:
      env:
        - DASHSCOPE_API_KEY
---

# 通义万相视频生成 (tianshu-wan-video)

调用阿里云通义万相 2.6 视频生成模型，通过 Node.js 脚本直接生成视频。支持文本生成视频和图片生成视频两种模式。

## 环境配置

### 必需环境变量

| 变量名 | 说明 |
|--------|------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key，用于认证和计费 |

在阿里云百炼平台获取 API Key：[dashscope.console.aliyun.com](https://dashscope.console.aliyun.com)

## 使用方法

### 文生视频 (Text-to-Video)

根据文本描述生成视频内容。

bash
node scripts/generate_video.js t2v --prompt "电影感特写镜头，缓慢推进，阳光透过窗户" --duration 5 --resolution 720P
### 图生视频 (Image-to-Video)

基于参考图片生成视频动画。

bash
node scripts/generate_video.js i2v --prompt "镜头缓慢旋转，背景虚化" --image-url "https://example.com/image.jpg" --duration 4
## 参数说明

### 模式参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `t2v` | 文生视频 | 根据文本描述生成视频 |
| `i2v` | 图生视频 | 基于图片生成视频 |

### 视频参数

| 参数 | 默认值 | 可选值 | 说明 |
|------|--------|--------|------|
| `--prompt` | 必填 | - | 视频内容描述文本，建议使用中文 |
| `--duration` | 5 | 5, 10 | 视频时长（秒） |
| `--resolution` | 720P | 720P, 1080P | 视频分辨率 |
| `--image-url` | - | - | 仅 i2v 模式必需，参考图片的 URL 地址 |

## 输出格式

脚本执行成功后输出：

VIDEO_URL: https://your-video-url.mp4
从输出中提取 `VIDEO_URL:` 后面的 URL 即可获取生成的视频。

## 注意事项

- **计费**：视频生成按照通义万相 API 标准收费，参考阿里云定价页
- **异步处理**：视频生成可能需要数分钟，请耐心等待任务完成
- **图片要求**：图生视频模式支持的图片格式和尺寸请参考官方文档
- **Prompt 优化**：描述越具体详细，生成的视频效果越好

## 错误处理

常见错误及解决方案：

| 错误类型 | 可能原因 | 解决方法 |
|----------|----------|----------|
| `AuthenticationError` | API Key 无效或过期 | 检查 `DASHSCOPE_API_KEY` 配置 |
| `RateLimitError` | 请求频率超限 | 降低请求频率，等待后重试 |
| `InvalidParameter` | 参数值不合法 | 检查 duration、resolution 是否在有效范围内 |
| `NetworkError` | 网络连接问题 | 检查网络状态和代理配置 |

## 完整示例

bash
# 设置环境变量
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxx"

# 文生视频示例 - 生成一段日落海景视频
node scripts/generate_video.js t2v \
  --prompt "壮丽的日落海景，金色阳光洒在海面上，海浪轻轻拍打礁石" \
  --duration 5 \
  --resolution 1080P

# 图生视频示例 - 将静态图片转换为动态视频
node scripts/generate_video.js i2v \
  --prompt "镜头从左向右缓慢平移" \
  --image-url "https://example.com/landscape.jpg" \
  --duration 10
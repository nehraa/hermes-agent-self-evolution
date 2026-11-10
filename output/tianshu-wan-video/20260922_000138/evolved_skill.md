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

调用阿里云通义万相 2.6 API 生成视频，支持**文生视频** (text-to-video) 和**图生视频** (image-to-video) 两种模式。纯 Node.js 实现，无需 Python 环境。

## 功能模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `t2v` | 文生视频，根据文字描述生成视频 | 创意内容、快速原型 |
| `i2v` | 图生视频，基于图片生成动态视频 | 素材动画、静态转动态 |

## 前置配置

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `DASHSCOPE_API_KEY` | 是 | 阿里云 DashScope API Key |

获取方式：阿里云 DashScope 控制台 → API-KEY 管理 → 创建或查看密钥。

## 用法

### 文生视频 (t2v)

bash
node scripts/generate_video.js t2v --prompt "电影感特写镜头，缓慢推进" --duration 5 --resolution 720P
**参数说明：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | string | 必需 | 视频内容描述，建议使用中文 |
| `--duration` | number | 5 | 视频时长（秒），支持 5/10 秒 |
| `--resolution` | string | 720P | 分辨率，支持 480P / 720P / 1080P |

### 图生视频 (i2v)

bash
node scripts/generate_video.js i2v --prompt "镜头缓慢旋转" --image-url "https://example.com/image.jpg" --duration 4
**参数说明：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | string | 必需 | 期望的动态效果描述 |
| `--image-url` | string | 必需 | 输入图片 URL，需可公网访问 |
| `--duration` | number | 5 | 视频时长（秒），支持 5/10 秒 |
| `--resolution` | string | 720P | 分辨率，支持 480P / 720P / 1080P |

## 输出

执行成功后，脚本输出：

VIDEO_URL: <视频下载链接>
从输出中提取 `VIDEO_URL` 后的链接即可下载或使用生成的视频。

## 常见问题

**Q: API 请求失败怎么办？**
- 确认 `DASHSCOPE_API_KEY` 已正确设置
- 检查账户余额或配额是否充足
- 确认网络可以访问阿里云 DashScope API

**Q: 生成的视频不符合预期？**
- 优化 `prompt` 描述，使用更具体的动作和场景描述
- 尝试不同的 `duration` 和 `resolution` 组合
- 图生视频模式确保输入图片清晰、主体明确
# B站AI字幕获取工具

让AI能像真人一样理解B站视频内容！

## 🎯 这是什么？

一个让AI读懂B站视频的技能包——通过获取视频的AI字幕文本，让AI理解视频内容后生成真实评论。

**核心优势：**
- 💰 成本极低：约¥0.004/视频（Claude Sonnet 4）
- ⚡ Token友好：3000-4000 tokens/视频
- 🎬 通用工具：支持任意有AI字幕的B站视频
- 🔥 比Whisper音频转录节省100-250倍成本

## 📦 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 获取B站Cookie
1. 浏览器登录 https://www.bilibili.com
2. F12开发者工具 → Network → 复制任意请求的Cookie
3. 保存Cookie备用

### 3. 找到视频信息
**BV号：** 视频URL里的 `BV1xxxxxxx`  
**CID：** 访问 `https://api.bilibili.com/x/web-interface/view?bvid={BV号}` 查看

### 4. 运行脚本
```bash
python get_subtitle.py BV1uyJt61EuT 42951708446 "你的Cookie"
```

## 📖 详细文档

查看 [SKILL.md](SKILL.md) 了解完整使用说明。

## 🎬 使用示例

```bash
# 获取字幕
python get_subtitle.py BV1uyJt61EuT 42951708446 "buvid3=...; SESSDATA=..."

# 输出：
# [SUCCESS] 字幕获取成功！共 143 行，1608 字符
# 已保存到: BV1uyJt61EuT_subtitle.txt
```

然后把字幕文本发给AI，让AI理解内容并生成评论！

## ⚠️ 重要提示

- ✅ 只支持有AI字幕的视频
- ✅ 需要登录Cookie（AI字幕需要登录态）
- ✅ Cookie请妥善保管，不要泄露
- ✅ 遵守B站使用条款，合理使用

## 🤝 贡献

欢迎提交Issue和PR！

---

**作者：** 小克 (Kiro AI Assistant)  
**版本：** 1.0.0  
**开源协议：** MIT License

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B站AI字幕获取工具（通用版）
支持任意B站视频的AI字幕获取
需要提供：BV号、CID、登录Cookie
"""

import json
import requests
import sys
import argparse


def get_subtitle(bvid, cid, cookie):
    """
    获取B站视频的AI字幕
    
    Args:
        bvid: 视频BV号（如 BV1uyJt61EuT）
        cid: 视频CID
        cookie: B站登录Cookie
        
    Returns:
        字幕文本（成功时）或 None（失败时）
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://www.bilibili.com/video/{bvid}/',
        'Origin': 'https://www.bilibili.com',
        'Cookie': cookie
    }
    
    print(f"[1/3] 正在获取视频 {bvid} 的字幕信息...")
    player_url = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
    
    try:
        response = requests.get(player_url, headers=headers, timeout=10)
        data = response.json()
        
        if data['code'] != 0:
            print(f"[ERROR] API返回错误: {data.get('message', 'Unknown')}")
            return None
        
        subtitle_info = data.get('data', {}).get('subtitle', {})
        
        if not subtitle_info or not subtitle_info.get('subtitles'):
            print("[ERROR] 未找到字幕，可能原因：")
            print("  - 该视频没有AI字幕")
            print("  - Cookie已过期或无效")
            print("  - 需要登录才能查看此视频")
            return None
        
        # 获取字幕URL（优先AI中文字幕）
        subtitle_list = subtitle_info['subtitles']
        subtitle_url = None
        
        for sub in subtitle_list:
            lan = sub.get('lan', '')
            lan_doc = sub.get('lan_doc', '')
            print(f"[INFO] 发现字幕: {lan_doc} ({lan})")
            
            if 'ai-zh' in lan.lower() or 'ai' in lan_doc.lower():
                subtitle_url = sub.get('subtitle_url', '')
                break
        
        if not subtitle_url and subtitle_list:
            subtitle_url = subtitle_list[0].get('subtitle_url', '')
        
        if not subtitle_url:
            print("[ERROR] 无法获取字幕URL")
            return None
        
        if subtitle_url.startswith('//'):
            subtitle_url = 'https:' + subtitle_url
        
        print(f"[2/3] 字幕URL: {subtitle_url}")
        
        # 下载字幕JSON
        print("[3/3] 正在下载字幕内容...")
        sub_response = requests.get(subtitle_url, headers=headers, timeout=10)
        sub_data = sub_response.json()
        
        body = sub_data.get('body', [])
        
        if not body:
            print("[ERROR] 字幕内容为空")
            return None
        
        # 提取文本
        subtitle_text = []
        for item in body:
            content = item.get('content', '').strip()
            if content:
                subtitle_text.append(content)
        
        full_text = '\n'.join(subtitle_text)
        
        print(f"\n[SUCCESS] 字幕获取成功！共 {len(body)} 行，{len(full_text)} 字符")
        print("="*60)
        print("字幕预览（前500字符）:")
        print("="*60)
        sys.stdout.buffer.write(full_text[:500].encode('utf-8'))
        sys.stdout.buffer.write(b'\n')
        print("="*60)
        
        return full_text
    
    except Exception as e:
        print(f"[ERROR] 发生异常: {e}")
        return None


def save_subtitle(text, filename):
    """保存字幕到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n[SUCCESS] 已保存到: {filename}")
        return True
    except Exception as e:
        print(f"[ERROR] 保存失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='获取B站视频的AI字幕',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python get_subtitle.py BV1uyJt61EuT 42951708446 "your_cookie_here"
  python get_subtitle.py BV1uyJt61EuT 42951708446 "your_cookie" --output subtitle.txt
        '''
    )
    
    parser.add_argument('bvid', help='视频BV号（如 BV1uyJt61EuT）')
    parser.add_argument('cid', help='视频CID')
    parser.add_argument('cookie', help='B站登录Cookie')
    parser.add_argument('-o', '--output', help='输出文件名（默认: {BVID}_subtitle.txt）')
    
    args = parser.parse_args()
    
    subtitle = get_subtitle(args.bvid, args.cid, args.cookie)
    
    if subtitle:
        output_file = args.output or f'{args.bvid}_subtitle.txt'
        save_subtitle(subtitle, output_file)
        print("\n[DONE] 完成！")
        return 0
    else:
        print("\n[FAILED] 获取字幕失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())

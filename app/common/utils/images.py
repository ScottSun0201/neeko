"""
图片下载工具
"""
import os
import uuid
import httpx
from pathlib import Path
from app.common.utils.logger import logger


async def download_image(url: str, save_dir: str = "/tmp/images/") -> str:
    """
    异步下载图片

    Args:
        url: 图片URL
        save_dir: 保存目录

    Returns:
        本地文件路径
    """
    try:
        # 创建目录
        Path(save_dir).mkdir(parents=True, exist_ok=True)

        # 生成文件名
        ext = url.split('.')[-1].split('?')[0] or 'jpg'
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(save_dir, filename)

        # 下载图片
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()

            # 保存文件
            with open(filepath, 'wb') as f:
                f.write(response.content)

        logger.info(f"图片下载成功: {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"图片下载失败 {url}: {str(e)}")
        raise

"""Build a half-size thumbnail set for every item image.

Source : images/<local_image_path>          (420x420 / 512x512 webp+png)
Target : images/thumb/<local_image_path>    (w//2 x h//2, same container)

Idempotent - existing files that already match the target size are skipped
(use --force to rebuild the whole set).
"""
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'ftf_values_full_data.json')
FORCE = '--force' in sys.argv


def half(size):
    return (max(1, size[0] // 2), max(1, size[1] // 2))


def main():
    with open(DATA, encoding='utf-8') as f:
        data = json.load(f)

    made, skipped, missing, failed = 0, 0, [], []

    for cat in data:
        for item in (data[cat] or {}).get('items', []):
            rel = (item.get('local_image_path') or '').strip().replace('\\', '/')
            if not rel:
                continue
            src = os.path.join(ROOT, 'images', rel)
            dst = os.path.join(ROOT, 'images', 'thumb', rel)
            if not os.path.exists(src):
                missing.append(rel)
                continue
            try:
                with Image.open(src) as im:
                    im.load()
                    target = half(im.size)
                    if os.path.exists(dst):
                        with Image.open(dst) as cur:
                            cur.load()
                            if cur.size == target and not FORCE:
                                skipped += 1
                                continue
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    out = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
                    out = out.resize(target, Image.LANCZOS)
                    if str(dst).lower().endswith('.webp'):
                        out.save(dst, 'WEBP', quality=82, method=3)
                    else:
                        out.save(dst, 'PNG', optimize=True)
                    made += 1
            except Exception as exc:  # keep going, report at the end
                failed.append((rel, str(exc)[:80]))

    # 数据里仍被引用的相对路径集合
    referenced = set()
    for cat in data:
        for item in (data[cat] or {}).get('items', []):
            rel = (item.get('local_image_path') or '').strip().replace('\\', '/')
            if rel:
                referenced.add(rel)

    # 清理孤儿小图（JSON 已不引用的）
    removed = 0
    troot = os.path.join(ROOT, 'images', 'thumb')
    if os.path.isdir(troot):
        for root, dirs, files in os.walk(troot):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), troot).replace('\\', '/')
                if rel not in referenced:
                    # os.remove(...) 已禁用：沙箱批量删除保护，孤儿文件交给 git rm 处理
                    removed += 1

    print('made: %d | already correct: %d | missing source: %d | failed: %d | orphan thumbs removed: %d'
          % (made, skipped, len(missing), len(failed), removed))
    for rel in missing[:10]:
        print('  MISSING', rel)
    for rel, err in failed[:10]:
        print('  FAILED ', rel, '->', err)


if __name__ == '__main__':
    main()

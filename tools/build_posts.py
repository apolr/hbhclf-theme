"""Converts the 14 Elementor posts into clean block markup: content/posts/<id>-<slug>.html.
Input: /tmp/posts_el.json (rows of ID, post_title, post_name, d=_elementor_data) plus THUMBS below."""
import json, re, os, html
from bs4 import BeautifulSoup, NavigableString

THUMBS = {'1727':1729,'1702':1703,'1640':1633,'1577':1604,'1545':1544,'1296':1297,'1237':1253,'1185':1187,
          '1174':1159,'1122':1131,'824':856,'770':707,'938':940,'1486':1487}
OUT = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts')
https = lambda u: re.sub(r'^http://', 'https://', u or '')
e = lambda s: html.escape(s, quote=True)

def walk(n, out):
    if isinstance(n, list):
        for x in n: walk(x, out)
        return
    if n.get('widgetType'):
        s = n.get('settings') or {}
        out.append((n['widgetType'], s if isinstance(s, dict) else {}))
    walk(n.get('elements', []), out)

def img_block(iid, url, alt='', caption='', size='large', cls=''):
    a = {'id': iid, 'sizeSlug': size, 'linkDestination': 'none'} if iid else {'sizeSlug': size, 'linkDestination': 'none'}
    if cls: a['className'] = cls
    cap = f'<figcaption class="wp-element-caption">{e(caption)}</figcaption>' if caption else ''
    ic = f' class="wp-image-{iid}"' if iid else ''
    fc = f'wp-block-image size-{size}' + (f' {cls}' if cls else '')
    return f'<!-- wp:image {json.dumps(a, separators=(",", ":"))} -->\n<figure class="{fc}"><img src="{e(https(url))}" alt="{e(alt)}"{ic}/>{cap}</figure>\n<!-- /wp:image -->'

def gallery(items, title, cols=3, logos=False):
    inner = []
    for i, g in enumerate(items, 1):
        alt = 'Member community logo' if logos else f'{title}, photo {i}'
        inner.append(img_block(g.get('id'), g.get('url'), alt))
    a = {'columns': cols, 'linkTo': 'none'}
    if logos: a.update({'imageCrop': False, 'className': 'hb-member-logos'})
    cls = f'wp-block-gallery has-nested-images columns-{cols}' + ('' if logos else ' is-cropped') + (' hb-member-logos' if logos else '')
    return f'<!-- wp:gallery {json.dumps(a, separators=(",", ":"))} -->\n<figure class="{cls}">' + "\n\n".join(inner) + '</figure>\n<!-- /wp:gallery -->'

def heading(t, level=2):
    a = '' if level == 2 else f' {{"level":{level}}}'
    return f'<!-- wp:heading{a} -->\n<h{level} class="wp-block-heading">{e(t)}</h{level}>\n<!-- /wp:heading -->'

def clean_inline(tag):
    """Return inner HTML keeping only strong/em/a/br, spans unwrapped, attributes stripped (except href)."""
    for t in tag.find_all(True):
        if t.name in ('span', 'div', 'font'):
            t.unwrap()
        elif t.name in ('strong', 'b', 'em', 'i', 'br'):
            t.attrs = {}
        elif t.name == 'a':
            t.attrs = {'href': t.get('href', '')}
        else:
            t.unwrap()
    s = ''.join(str(c) for c in tag.contents)
    s = s.replace('\xa0', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'<(strong|em)>\s*</\1>', '', s)
    s = re.sub(r'<a href="">(.*?)</a>', r'\1', s)
    return s

def para(inner):
    return f'<!-- wp:paragraph -->\n<p>{inner}</p>\n<!-- /wp:paragraph -->'

def text_editor(raw):
    blocks = []
    m = re.search(r'\[caption[^\]]*\](.*?)\[/caption\]', raw, re.S)
    if m:
        cap_soup = BeautifulSoup(m.group(1), 'html.parser')
        im = cap_soup.find('img')
        cap = cap_soup.get_text(' ').strip()
        iid = int(re.search(r'wp-image-(\d+)', ' '.join(im.get('class', []))).group(1))
        blocks.append(img_block(iid, im['src'], im.get('alt', ''), cap, size='full', cls='hb-portrait'))
        raw = raw.replace(m.group(0), '')
    soup = BeautifulSoup(raw, 'html.parser')
    for el in soup.find_all(['p', 'ul', 'ol']):
        if el.find_parent(['ul', 'ol']) or (el.name == 'p' and el.find_parent('li')): continue
        if el.name in ('ul', 'ol'):
            items = [clean_inline(li) for li in el.find_all('li')]
            items = [i for i in items if i]
            lis = "\n\n".join(f'<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->' for i in items)
            o = ' {"ordered":true}' if el.name == 'ol' else ''
            blocks.append(f'<!-- wp:list{o} -->\n<{el.name} class="wp-block-list">{lis}</{el.name}>\n<!-- /wp:list -->')
        else:
            t = clean_inline(el)
            if BeautifulSoup(t, 'html.parser').get_text().strip():
                blocks.append(para(t))
    return blocks

def build(r):
    pid, title = r['ID'], r['post_title'].replace('\xa0', ' ')
    out = []; walk(json.loads(r['d']), out)
    blocks = []
    for w, s in out:
        if w in ('theme-post-title',):
            continue
        if w in ('heading', 'e-heading'):
            t = s.get('title')
            t = t.get('value') if isinstance(t, dict) else t
            if t and t.strip().lower() != title.strip().lower():
                blocks.append(heading(t.strip()))
        elif w == 'image':
            im = s.get('image', {})
            if im.get('id'):
                blocks.append(img_block(im['id'], im['url'], title))
        elif w == 'e-image':
            blocks.append(img_block(1729, 'https://hbhclf.org/wp-content/uploads/2026/07/Nathaneal.jpeg', 'Nathanael Selambi', cls='hb-portrait'))
        elif w == 'text-editor':
            blocks += text_editor(s.get('editor', ''))
        elif w == 'gallery':
            blocks.append(gallery(s.get('gallery', []), title))
        elif w == 'image-gallery':
            blocks.append(gallery(s.get('wp_gallery', []), title, cols=4, logos=True))
        else:
            print('UNHANDLED', pid, w)
    path = os.path.join(OUT, f"{pid}-{r['post_name']}.html")
    open(path, 'w').write("\n\n".join(blocks) + "\n")
    return path, len(blocks)

if __name__ == '__main__':
    for r in json.load(open('/tmp/posts_el.json')):
        p, n = build(r)
        print(os.path.basename(p).ljust(70), n, 'blocks', os.path.getsize(p), 'bytes')

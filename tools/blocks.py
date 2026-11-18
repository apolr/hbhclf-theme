"""Small helpers that emit WordPress block markup (native blocks only)."""
import html as _h

U = 'https://hbhclf.org/wp-content/uploads/'
PAD = lambda s: f'"style":{{"spacing":{{"padding":{{"top":"var:preset|spacing|{s}","bottom":"var:preset|spacing|{s}"}}}}}}'
PADCSS = lambda s: f'padding-top:var(--wp--preset--spacing--{s});padding-bottom:var(--wp--preset--spacing--{s})'
e = lambda t: _h.escape(t, quote=False)

def heading(text, level=2, size=None, align=None, extra_cls=''):
    attrs = {'level': level} if level != 2 else {}
    cls = ['wp-block-heading']
    if align: attrs['textAlign'] = align; cls.append(f'has-text-align-{align}')
    if size: attrs['fontSize'] = size
    if extra_cls: attrs['className'] = extra_cls; cls.append(extra_cls)
    if size: cls.append(f'has-{size}-font-size')
    import json
    a = (' ' + json.dumps(attrs, separators=(',', ':'))) if attrs else ''
    return f'<!-- wp:heading{a} -->\n<h{level} class="{" ".join(cls)}">{e(text)}</h{level}>\n<!-- /wp:heading -->'

def para(text, size=None, bold=False, raw=False, align=None):
    import json
    attrs = {}
    cls = []
    if align: attrs['align'] = align; cls.append(f'has-text-align-{align}')
    if size: attrs['fontSize'] = size; cls.append(f'has-{size}-font-size')
    a = (' ' + json.dumps(attrs, separators=(',', ':'))) if attrs else ''
    c = f' class="{" ".join(cls)}"' if cls else ''
    body = text if raw else e(text)
    if bold: body = f'<strong>{body}</strong>'
    return f'<!-- wp:paragraph{a} -->\n<p{c}>{body}</p>\n<!-- /wp:paragraph -->'

def kicker(text, color='orange'):
    return (f'<!-- wp:paragraph {{"fontSize":"small","style":{{"typography":{{"letterSpacing":"0.12em","textTransform":"uppercase","fontWeight":"600"}}}},"textColor":"{color}"}} -->\n'
            f'<p class="has-{color}-color has-text-color has-small-font-size" style="font-style:normal;font-weight:600;letter-spacing:0.12em;text-transform:uppercase">{e(text)}</p>\n<!-- /wp:paragraph -->')

def button(label, url, orange=False, center=False):
    import json
    battrs = {'backgroundColor': 'orange', 'textColor': 'black'} if orange else {}
    bcls = 'wp-block-button__link has-black-color has-orange-background-color has-text-color has-background wp-element-button' if orange else 'wp-block-button__link wp-element-button'
    ba = (' ' + json.dumps(battrs, separators=(',', ':'))) if battrs else ''
    lay = ' {"layout":{"type":"flex","justifyContent":"center"}}' if center else ''
    return (f'<!-- wp:buttons{lay} -->\n<div class="wp-block-buttons"><!-- wp:button{ba} -->\n'
            f'<div class="wp-block-button"><a class="{bcls}" href="{_h.escape(url)}">{e(label)}</a></div>\n<!-- /wp:button --></div>\n<!-- /wp:buttons -->')

def buttons(items, orange=False):
    import json
    inner = []
    for label, url in items:
        battrs = {'backgroundColor': 'orange', 'textColor': 'black'} if orange else {}
        bcls = 'wp-block-button__link has-black-color has-orange-background-color has-text-color has-background wp-element-button' if orange else 'wp-block-button__link wp-element-button'
        ba = (' ' + json.dumps(battrs, separators=(',', ':'))) if battrs else ''
        inner.append(f'<!-- wp:button{ba} -->\n<div class="wp-block-button"><a class="{bcls}" href="{_h.escape(url)}">{e(label)}</a></div>\n<!-- /wp:button -->')
    return '<!-- wp:buttons -->\n<div class="wp-block-buttons">' + "\n\n".join(inner) + '</div>\n<!-- /wp:buttons -->'

def image(src, alt='', radius=True, size='large'):
    st = ',"style":{"border":{"radius":"16px"}}' if radius else ''
    cb = ' has-custom-border' if radius else ''
    sty = ' style="border-radius:16px"' if radius else ''
    return (f'<!-- wp:image {{"sizeSlug":"{size}","linkDestination":"none"{st}}} -->\n'
            f'<figure class="wp-block-image size-{size}{cb}"><img src="{src}" alt="{_h.escape(alt)}"{sty}/></figure>\n<!-- /wp:image -->')

def lst(items, ordered=False):
    tag = 'ol' if ordered else 'ul'
    a = ' {"ordered":true}' if ordered else ''
    li = "\n\n".join(f'<!-- wp:list-item -->\n<li>{e(i)}</li>\n<!-- /wp:list-item -->' for i in items)
    return f'<!-- wp:list{a} -->\n<{tag} class="wp-block-list">{li}</{tag}>\n<!-- /wp:list -->'

def column(inner, valign='center', width=None):
    import json
    attrs = {'verticalAlignment': valign}
    cls = f'wp-block-column is-vertically-aligned-{valign}'
    sty = ''
    if width: attrs['width'] = width; sty = f' style="flex-basis:{width}"'
    return f'<!-- wp:column {json.dumps(attrs, separators=(",", ":"))} -->\n<div class="{cls}"{sty}>{inner}</div>\n<!-- /wp:column -->'

def columns(cols, valign='center', stack_reverse=False):
    import json
    attrs = {'verticalAlignment': valign}
    return (f'<!-- wp:columns {json.dumps(attrs, separators=(",", ":"))} -->\n<div class="wp-block-columns are-vertically-aligned-{valign}">'
            + "\n\n".join(cols) + '</div>\n<!-- /wp:columns -->')

def section(inner, bg=None, text=None, content='1200px', pad='50', anchor=None, reveal=True):
    import json
    attrs = {'align': 'full'}
    cls = ['wp-block-group', 'alignfull']
    if reveal: attrs['className'] = 'hb-reveal'; cls.append('hb-reveal')
    if anchor: attrs['anchor'] = anchor
    if bg: attrs['backgroundColor'] = bg
    if text: attrs['textColor'] = text
    attrs['layout'] = {'type': 'constrained', 'contentSize': content}
    attrs['style'] = {'spacing': {'padding': {'top': f'var:preset|spacing|{pad}', 'bottom': f'var:preset|spacing|{pad}'}}}
    if text: cls.append(f'has-{text}-color')
    if bg: cls.append(f'has-{bg}-background-color')
    if text: cls.append('has-text-color')
    if bg: cls.append('has-background')
    idattr = f' id="{anchor}"' if anchor else ''
    return (f'<!-- wp:group {json.dumps(attrs, separators=(",", ":"))} -->\n<div{idattr} class="{" ".join(cls)}" style="{PADCSS(pad)}">'
            + inner + '</div>\n<!-- /wp:group -->')

def page_hero(title, subtitle=None, bg='black'):
    inner = heading(title, 1, 'hero', 'center')
    if subtitle: inner += "\n\n" + para(subtitle, 'large', align='center')
    return section(inner, bg=bg, text='white' if bg == 'black' else 'black', content='1000px', pad='50', reveal=False)

def card_grid(cards, cols=3):
    """cards: list of (title, text). Equal columns in rows of `cols`."""
    rows = []
    for i in range(0, len(cards), cols):
        chunk = cards[i:i + cols]
        cs = [column(heading(t, 3, 'large') + "\n\n" + para(x), valign='top') for t, x in chunk]
        while len(cs) < cols: cs.append(column('', valign='top'))
        rows.append(columns(cs, valign='top'))
    return "\n\n".join(rows)

def html_block(raw):
    return f'<!-- wp:html -->\n{raw}\n<!-- /wp:html -->'

def shortcode(code):
    return f'<!-- wp:shortcode -->\n{code}\n<!-- /wp:shortcode -->'

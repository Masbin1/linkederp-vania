# -*- coding: utf-8 -*-
"""Render FIELDS.md (the field-by-field checklist for Studio) from spec.py.

    python3 vif_sales_incentive/docs/odoo_online/render_fields_md.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = {}
exec(open(os.path.join(HERE, 'spec.py')).read(), spec)

TYPE_LABEL = {
    'char': 'Char (Text)', 'text': 'Text (Multiline)', 'integer': 'Integer',
    'float': 'Float (Decimal)', 'monetary': 'Monetary', 'boolean': 'Boolean (Checkbox)',
    'date': 'Date', 'selection': 'Selection', 'many2one': 'Many2one',
    'one2many': 'One2many', 'many2many': 'Many2many',
}


def detail(ftype, opts):
    bits = []
    if opts.get('relation'):
        bits.append('Model: `%s`' % opts['relation'])
    if opts.get('relation_field'):
        bits.append('Field relasi: `%s`' % opts['relation_field'])
    if ftype == 'many2one':
        bits.append('On Delete: %s' % (opts.get('ondelete') or (
            'restrict' if opts.get('required') else 'set null')).title())
    if opts.get('selection') and not opts.get('related'):
        bits.append('Nilai: ' + ', '.join('`%s`=%s' % (v, n) for v, n in opts['selection']))
    if opts.get('related'):
        bits.append('Related: `%s`%s' % (opts['related'], ' (Stored)' if opts.get('store') else ''))
    if opts.get('compute'):
        bits.append('**Compute** `compute/%s`, Depends `%s`, %s%s' % (
            opts['compute'], opts.get('depends', ''),
            'Stored' if opts.get('store') else 'Not stored',
            ', editable (Readonly OFF)' if opts.get('readonly') is False else ''))
    if opts.get('required'):
        bits.append('Required')
    if opts.get('readonly') and not opts.get('compute'):
        bits.append('Readonly')
    if opts.get('index'):
        bits.append('Indexed')
    if ftype == 'monetary':
        bits.append('Currency field: `x_currency_id`')
    if opts.get('tracking'):
        bits.append('Tracking: %d' % opts['tracking'])
    if opts.get('help'):
        bits.append('Help: %s' % opts['help'])
    return '; '.join(bits)


out = ['# Daftar Field -- VIF Sales Incentive di Odoo Online', '',
       '> File ini DIGENERATE dari `spec.py` (`python3 render_fields_md.py`). '
       'Jangan edit manual -- ubah `spec.py` lalu generate ulang.', '',
       'Urutan di bawah = urutan pembuatan. Many2one hanya bisa menunjuk model '
       'yang sudah ada, jadi ikuti urutannya.', '',
       '**`x_name` dibuat otomatis oleh Odoo** di setiap model baru. Jangan '
       'buat lagi. Jika tabel meminta `x_name` dengan Compute, EDIT field '
       '`x_name` yang sudah ada.', '',
       '**Field Monetary** butuh `x_currency_id` sudah ada lebih dulu di model yang sama.', '']

models = {m[0]: m for m in spec['MODELS']}
std = dict(spec['STANDARD_FIELDS'])
for n, name in enumerate(spec['BUILD_ORDER'], 1):
    if name in models:
        _m, label, flds = models[name]
        out.append('## %d. `%s` -- %s (model baru)' % (n, name, label))
        if name in spec['MAIL_MODELS']:
            out += ['', '**Chatter:** saat membuat model, centang **Has Mail Thread** '
                    'dan **Has Mail Activity** (tidak bisa dimatikan lagi). Field '
                    'dengan *Tracking* diisi di **Enable Ordered Tracking**.']
    else:
        flds = std[name]
        out.append('## %d. `%s` (model standar -- tambah field)' % (n, name))
    out += ['', '| # | Field Name | Label | Type | Detail |', '|---|---|---|---|---|']
    for i, (fname, ftype, flabel, opts) in enumerate(flds, 1):
        out.append('| %d | `%s` | %s | %s | %s |' % (
            i, fname, flabel, TYPE_LABEL[ftype], detail(ftype, opts)))
    out.append('')

out += ['## One2many & field yang membacanya (buat SETELAH semua model di atas ada)', '',
        'Buat berurutan dari atas: field Compute di bawah membaca One2many di atasnya.', '',
        '| Model | Field Name | Label | Type | Detail |', '|---|---|---|---|---|']
for model, fname, ftype, flabel, opts in spec['EXTRA_FIELDS']:
    out.append('| `%s` | `%s` | %s | %s | %s |' % (
        model, fname, flabel, TYPE_LABEL[ftype], detail(ftype, opts)))
out += ['', '## Default Value', '',
        'Studio: klik field -> Properties -> Default Value. Atau Settings -> '
        'Technical -> User-defined Defaults.', '',
        '| Model | Field | Default |', '|---|---|---|']
for model, fname, value in spec['DEFAULTS']:
    out.append('| `%s` | `%s` | `%s` |' % (model, fname, value))
out += ['| `x_incentive_branch`, `x_incentive_rule`, `x_incentive_period` | '
        '`x_company_id` | company Anda |', '']

open(os.path.join(HERE, 'FIELDS.md'), 'w').write('\n'.join(out))
print('FIELDS.md written')

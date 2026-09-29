# -*- coding: utf-8 -*-
"""Build the Odoo Online (Studio) version of VIF Sales Incentive in a TEST
database, from spec.py + the code files, exactly as the manual steps do.

NOT for Odoo Online itself (there is no shell there). Run it in `odoo shell`
against a COPY of the client database to prove the server-action code works
before anybody clicks through Studio:

    odoo-bin shell -c odoo.conf -d vaniaeut_online --no-http \
        < vif_sales_incentive/docs/odoo_online/build_test_db.py

Idempotent: models / fields / actions that already exist are left alone.
"""
import os

from odoo import Command

BASE = os.path.join(os.getcwd(), 'vif_sales_incentive', 'docs', 'odoo_online')
if not os.path.isdir(BASE):
    BASE = '/Users/muhammadbintang/linkederp/linkederp-vania/vif_sales_incentive/docs/odoo_online'
spec = {}
exec(open(os.path.join(BASE, 'spec.py')).read(), spec)


def code(sub, name):
    return open(os.path.join(BASE, sub, name)).read()


IrModel = env['ir.model']
IrField = env['ir.model.fields']


def model_rec(model):
    rec = IrModel.search([('model', '=', model)], limit=1)
    assert rec, 'model %s missing' % model
    return rec


def field_vals(model, name, ftype, label, opts):
    vals = {
        'model_id': model_rec(model).id,
        'name': name,
        'field_description': label,
        'ttype': ftype,
        'state': 'manual',
        'required': opts.get('required', False),
        'readonly': opts.get('readonly', False),
        'index': opts.get('index', False),
        'help': opts.get('help', False),
        'tracking': opts.get('tracking', 0),
    }
    if 'relation' in opts:
        vals['relation'] = opts['relation']
    if ftype == 'many2one':
        vals['on_delete'] = opts.get(
            'ondelete', 'restrict' if opts.get('required') else 'set null')
    if ftype == 'one2many':
        vals['relation_field'] = opts['relation_field']
    if ftype == 'many2many':
        vals['relation_table'] = '%s_%s_rel' % (opts['relation'].replace('.', '_'),
                                                model.replace('.', '_'))
        vals['column1'] = '%s_id' % model.replace('.', '_')
        vals['column2'] = '%s_id' % opts['relation'].replace('.', '_')
    if ftype == 'selection' and 'selection' in opts and not opts.get('related'):
        vals['selection_ids'] = [
            Command.create({'value': v, 'name': n, 'sequence': i})
            for i, (v, n) in enumerate(opts['selection'])]
    if ftype == 'monetary':
        vals['currency_field'] = 'x_currency_id'
    if opts.get('related'):
        vals['related'] = opts['related']
        vals['store'] = opts.get('store', False)
        vals['readonly'] = True
    if opts.get('compute'):
        vals['compute'] = code('compute', opts['compute'])
        vals['depends'] = opts.get('depends', '')
        vals['store'] = opts.get('store', False)
        vals['readonly'] = opts.get('readonly', True)
    return vals


def ensure_field(model, name, ftype, label, opts):
    existing = IrField.search([('model', '=', model), ('name', '=', name)], limit=1)
    if existing:
        # Odoo creates x_name on every new model by itself: a computed x_name
        # is set by EDITING that field, not by adding a second one.
        if opts.get('compute') and not existing.compute:
            existing.write({'compute': code('compute', opts['compute']),
                            'depends': opts.get('depends', ''),
                            'store': opts.get('store', False),
                            'readonly': opts.get('readonly', True)})
        if opts.get('tracking') and existing.tracking != opts['tracking']:
            existing.write({'tracking': opts['tracking']})
        return
    IrField.create(field_vals(model, name, ftype, label, opts))


models_by_name = {m[0]: m for m in spec['MODELS']}
std_by_name = dict(spec['STANDARD_FIELDS'])

for name in spec['BUILD_ORDER']:
    if name in models_by_name:
        _n, label, flds = models_by_name[name]
        mail = name in spec['MAIL_MODELS']
        activity = bool(spec['MAIL_MODELS'].get(name))
        rec = IrModel.search([('model', '=', name)], limit=1)
        if not rec:
            IrModel.create({'name': label, 'model': name, 'state': 'manual',
                            'is_mail_thread': mail, 'is_mail_activity': activity})
        elif (mail and not rec.is_mail_thread) or (activity and not rec.is_mail_activity):
            rec.write({'is_mail_thread': True, 'is_mail_activity': activity})
    else:
        flds = std_by_name[name]
    for fname, ftype, flabel, opts in flds:
        ensure_field(name, fname, ftype, flabel, opts)
    print('model ready:', name)

for model, fname, ftype, flabel, opts in spec['EXTRA_FIELDS']:
    ensure_field(model, fname, ftype, flabel, opts)

# default sort order, once every field it names exists
for model, order in spec['MODEL_ORDER'].items():
    rec = model_rec(model)
    if rec.order != order:
        rec.write({'order': order})

company = env.company
for model, fname, value in spec['DEFAULTS']:
    env['ir.default'].set(model, fname, value)
for model in ('x_incentive_branch', 'x_incentive_rule', 'x_incentive_period'):
    env['ir.default'].set(model, 'x_company_id', company.id)

if not env['ir.sequence'].search_count([('code', '=', 'x_incentive_target_movement')]):
    env['ir.sequence'].create({
        'name': 'Incentive Target Movement', 'code': 'x_incentive_target_movement',
        'prefix': 'TMV/%(year)s/', 'padding': 5})

Server = env['ir.actions.server']
for aname, model, fname in spec['SERVER_ACTIONS']:
    act = Server.search([('name', '=', aname)], limit=1)
    vals = {'name': aname, 'model_id': model_rec(model).id, 'state': 'code',
            'code': code('actions', fname)}
    if act:
        act.write(vals)
    else:
        Server.create(vals)

Automation = env['base.automation']
for aname, model, trigger, trig_fields, fname in spec['AUTOMATIONS']:
    rule = Automation.search([('name', '=', aname)], limit=1)
    if rule:
        rule.action_server_ids.write({'code': code('automations', fname)})
        continue
    mrec = model_rec(model)
    Automation.create({
        'name': aname,
        'model_id': mrec.id,
        'trigger': trigger,
        'trigger_field_ids': [Command.set(IrField.search([
            ('model', '=', model), ('name', 'in', trig_fields)]).ids)],
        'action_server_ids': [Command.create({
            'name': aname, 'model_id': mrec.id, 'state': 'code',
            'usage': 'base_automation', 'code': code('automations', fname)})],
    })

env.cr.commit()
print('BUILD DONE')

# ------------------------------------------------------------------ views
import re

View = env['ir.ui.view']
act_ids = {a.name: a.id for a in Server.search([('name', 'like', 'VIF: %')])}


def arch_of(fname):
    xml = open(os.path.join(BASE, 'views', fname)).read()
    return re.sub(r'\[ID ([^\]]+)\]', lambda m: str(act_ids[m.group(1)]), xml)


for vname, model, vtype, fname, inherit in spec['VIEWS']:
    vals = {'name': vname, 'model': model, 'type': vtype, 'arch': arch_of(fname),
            'priority': 99 if inherit else 16}
    if inherit:
        vals['inherit_id'] = env.ref(inherit).id
    view = View.search([('name', '=', vname), ('model', '=', model)], limit=1)
    if view:
        view.write(vals)
    else:
        View.create(vals)

Act = env['ir.actions.act_window']
acts = {}
for aname, model, mode, domain, ctx in spec['WINDOW_ACTIONS']:
    act = Act.search([('name', '=', aname), ('res_model', '=', model)], limit=1)
    vals = {'name': aname, 'res_model': model, 'view_mode': mode,
            'domain': domain, 'context': ctx}
    if act:
        act.write(vals)
    else:
        act = Act.create(vals)
    acts[aname] = act

Menu = env['ir.ui.menu']
menus = {}
for mname, parent, aname, seq, _grp in spec['MENUS']:
    vals = {'name': mname, 'sequence': seq,
            'parent_id': menus[parent].id if parent else False,
            'action': 'ir.actions.act_window,%d' % acts[aname].id if aname else False}
    menu = Menu.search([('name', '=', mname),
                        ('parent_id', '=', vals['parent_id'])], limit=1)
    if menu:
        menu.write(vals)
    else:
        menu = Menu.create(vals)
    menus[mname] = menu

# every view must render
for vname, model, vtype, fname, inherit in spec['VIEWS']:
    env[model].get_view(view_type=vtype)
env.cr.commit()
print('VIEWS DONE')

# ------------------------------------------------------------------ security
Group = env['res.groups']
groups = {}
for gname, implied in spec['GROUPS']:
    grp = Group.search([('name', '=', gname)], limit=1)
    vals = {'name': gname}
    if implied:
        vals['implied_ids'] = [Command.link(groups[implied].id)]
    if grp:
        grp.write(vals)
    else:
        grp = Group.create(vals)
    groups[gname] = grp

Access = env['ir.model.access']
admin = groups['VIF Incentive / Administrator']
user_grp = groups['VIF Incentive / Salesperson']
for name in spec['BUILD_ORDER']:
    if not name.startswith('x_'):
        continue
    mid = model_rec(name).id
    for grp, full in ((admin, True), (user_grp, False)):
        if not full and name not in spec['READ_MODELS']:
            continue
        if Access.search_count([('model_id', '=', mid), ('group_id', '=', grp.id)]):
            continue
        Access.create({'name': '%s %s' % (name, 'admin' if full else 'user'),
                       'model_id': mid, 'group_id': grp.id, 'perm_read': True,
                       'perm_write': full, 'perm_create': full, 'perm_unlink': full})

for mname, parent, aname, seq, gname in spec['MENUS']:
    menus[mname].write({'group_ids': [Command.set(groups[gname].ids if gname else [])]})

Rule = env['ir.rule']
for rname, model, gname, domain in spec['RECORD_RULES']:
    if Rule.search_count([('name', '=', rname)]):
        continue
    Rule.create({'name': rname, 'model_id': model_rec(model).id,
                 'groups': [Command.link(groups[gname].id)], 'domain_force': domain})
env.cr.commit()
print('SECURITY DONE')

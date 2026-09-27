# -*- coding: utf-8 -*-
"""Project split: a sale on a project is credited to the people ON the
project -- PM (user_id), Salesperson 2, Salesperson 3 -- by their commission
shares, not to the sale order's salesperson.

* A salesperson who is not on the project earns nothing from it.
* No shares filled in -> the PM takes 100%.
* A share with nobody in its slot goes to the PM.
* A share whose person is not in the scheme (no sales branch, or no target
  in the invoice's period) goes to the PM.
* No project at all -> the invoice salesperson keeps 100% (old behaviour).

Salesperson 2/3 and the share fields are Odoo Studio fields that only exist
in the client database; the tests that need them skip elsewhere.

Runs in 2028 so it never collides with seeded or other test periods.
"""
from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

STUDIO_FIELDS = (
    'x_studio_salesperson_2', 'x_studio_salesperson_3',
    'x_studio_komisi_pm', 'x_studio_komisi_salesperson_2',
    'x_studio_komisi_salesperson_3',
)


@tagged('post_install', '-at_install')
class TestProjectSplit(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        branch = cls.env.ref('vif_sales_incentive.branch_jkt')
        team = cls.env.ref('vif_sales_incentive.designation_team')

        def person(name):
            user = cls.env['res.users'].create({
                'name': name, 'login': 'split_%s' % name.lower(),
                'email': 'split.%s@example.com' % name.lower(),
            })
            employee = cls.env['hr.employee'].create({
                'name': name, 'user_id': user.id,
                'incentive_branch_id': branch.id,
                'incentive_business_type': 'b2b',
                'incentive_designation_id': team.id,
            })
            return user, employee

        cls.seller_user, cls.seller = person('Seller')
        cls.pm_user, cls.pm = person('Manager')
        cls.sp2_user, cls.sp2 = person('Second')
        cls.sp3_user, cls.sp3 = person('Third')

        cls.period = cls.env['incentive.period'].create({
            'name': 'Split Mar 2028',
            'date_start': fields.Date.to_date('2028-03-01'),
            'date_end': fields.Date.to_date('2028-03-31'),
            'company_id': cls.company.id,
        })
        for employee in (cls.seller, cls.pm, cls.sp2, cls.sp3):
            cls.env['incentive.target'].create({
                'period_id': cls.period.id,
                'employee_id': employee.id,
                'target_type': 'incentive',
                'amount': 1_000_000.0,
            })
        cls.partner = cls.env['res.partner'].create({'name': 'Split Customer'})
        cls.product = cls.env['product.product'].create({
            'name': 'Split Widget', 'type': 'consu',
            'invoice_policy': 'order', 'list_price': 1000.0,
            'taxes_id': [(5, 0, 0)],
        })
        cls.has_studio = all(
            f in cls.env['project.project']._fields for f in STUDIO_FIELDS)

    # -- helpers ---------------------------------------------------------
    def _project(self, **vals):
        return self.env['project.project'].create(dict(
            name='Split Project', allow_billable=True,
            partner_id=self.partner.id, user_id=self.pm_user.id, **vals))

    def _invoice(self, project=None, amount=1000.0):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'user_id': self.seller_user.id,
            'project_id': project.id if project else False,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': amount,
                'tax_ids': [(5, 0, 0)],
            })],
        })
        order.action_confirm()
        invoice = order._create_invoices()
        invoice.invoice_date = fields.Date.to_date('2028-03-10')
        invoice.action_post()
        return invoice

    def _credit(self, invoice):
        Tx = self.env['incentive.transaction']
        Tx._generate_for_period(self.period)
        rows = Tx.search([('move_id', '=', invoice.id)])
        return {tx.employee_id: tx.base_amount for tx in rows}

    def _require_studio(self):
        if not self.has_studio:
            self.skipTest('Studio split fields are not in this database.')

    # -- tests -----------------------------------------------------------
    def test_no_project_keeps_salesperson(self):
        invoice = self._invoice()
        self.assertEqual(self._credit(invoice), {self.seller: 1000.0})

    def test_pm_only_project_credits_pm_not_salesperson(self):
        vals = {}
        if self.has_studio:
            vals = {'x_studio_komisi_pm': 0.0}
        invoice = self._invoice(self._project(**vals))
        self.assertEqual(
            self._credit(invoice), {self.pm: 1000.0},
            'the SO salesperson is not on the project and must get nothing')

    def test_three_way_split(self):
        self._require_studio()
        project = self._project(
            x_studio_salesperson_2=self.sp2_user.id,
            x_studio_salesperson_3=self.sp3_user.id,
            x_studio_komisi_pm=0.2,
            x_studio_komisi_salesperson_2=0.4,
            x_studio_komisi_salesperson_3=0.4,
        )
        invoice = self._invoice(project)
        self.assertEqual(self._credit(invoice), {
            self.pm: 200.0, self.sp2: 400.0, self.sp3: 400.0})
        tx = self.env['incentive.transaction'].search([
            ('move_id', '=', invoice.id), ('employee_id', '=', self.sp2.id)])
        self.assertEqual(tx.split_role, 'sp2')
        self.assertAlmostEqual(tx.split_share, 0.4)
        self.assertEqual(tx.project_id, project)

    def test_salesperson_on_project_only_gets_their_share(self):
        self._require_studio()
        project = self._project(
            x_studio_salesperson_2=self.seller_user.id,
            x_studio_komisi_pm=0.7,
            x_studio_komisi_salesperson_2=0.3,
        )
        invoice = self._invoice(project)
        self.assertEqual(self._credit(invoice), {
            self.pm: 700.0, self.seller: 300.0})

    def test_share_without_person_goes_to_pm(self):
        self._require_studio()
        project = self._project(x_studio_komisi_salesperson_3=1.0)
        invoice = self._invoice(project)
        self.assertEqual(self._credit(invoice), {self.pm: 1000.0})

    def test_changed_project_drops_old_rows(self):
        self._require_studio()
        project = self._project(
            x_studio_salesperson_2=self.sp2_user.id,
            x_studio_komisi_pm=0.5,
            x_studio_komisi_salesperson_2=0.5,
        )
        invoice = self._invoice(project)
        self.assertEqual(self._credit(invoice), {
            self.pm: 500.0, self.sp2: 500.0})
        project.write({
            'x_studio_salesperson_2': self.sp3_user.id,
        })
        self.assertEqual(
            self._credit(invoice), {self.pm: 500.0, self.sp3: 500.0},
            'the replaced salesperson must lose the row on recalculation')

    def test_credit_note_is_split_like_the_invoice(self):
        self._require_studio()
        project = self._project(
            x_studio_salesperson_2=self.sp2_user.id,
            x_studio_komisi_pm=0.25,
            x_studio_komisi_salesperson_2=0.75,
        )
        invoice = self._invoice(project)
        self._credit(invoice)
        credit_note = invoice._reverse_moves([{
            'invoice_date': fields.Date.to_date('2028-03-20'),
        }])
        credit_note.action_post()
        refunds = self.env['incentive.transaction'].search([
            ('move_id', '=', credit_note.id)])
        self.assertEqual(
            {tx.employee_id: tx.base_amount for tx in refunds},
            {self.pm: -250.0, self.sp2: -750.0})
        self.assertTrue(all(refunds.mapped('reversal_of_id')))

    def test_salesperson_without_target_share_goes_to_pm(self):
        self._require_studio()
        self.env['incentive.target'].search([
            ('employee_id', '=', self.sp3.id)]).unlink()
        project = self._project(
            x_studio_salesperson_2=self.sp2_user.id,
            x_studio_salesperson_3=self.sp3_user.id,
            x_studio_komisi_pm=0.2,
            x_studio_komisi_salesperson_2=0.4,
            x_studio_komisi_salesperson_3=0.4,
        )
        invoice = self._invoice(project)
        self.assertEqual(self._credit(invoice), {
            self.pm: 600.0, self.sp2: 400.0})

    def test_salesperson_without_branch_share_goes_to_pm(self):
        self._require_studio()
        self.sp2.incentive_branch_id = False
        project = self._project(
            x_studio_salesperson_2=self.sp2_user.id,
            x_studio_komisi_pm=0.3,
            x_studio_komisi_salesperson_2=0.7,
        )
        invoice = self._invoice(project)
        self.assertEqual(self._credit(invoice), {self.pm: 1000.0})

    def test_calculate_refuses_credited_people_without_target(self):
        self.env['incentive.target'].search([
            ('employee_id', '=', self.pm.id)]).unlink()
        self._credit(self._invoice(self._project()))
        with self.assertRaisesRegex(UserError, 'Manager'):
            self.period._check_credited_employees()

    def test_calculate_refuses_credited_people_without_branch(self):
        self.seller.incentive_branch_id = False
        self._credit(self._invoice())
        with self.assertRaisesRegex(UserError, 'No Sales Branch'):
            self.period._check_credited_employees()

    def test_calculate_passes_when_everyone_is_set_up(self):
        self._credit(self._invoice(self._project()))
        self.period._check_credited_employees()

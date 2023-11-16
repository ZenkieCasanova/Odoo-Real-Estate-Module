from odoo import models,fields,api
from odoo.exceptions import UserError
class EstateProperty(models.Model):
    _inherit = "estate.property"
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.user.company_id)
    invoice_id = fields.Many2one('account.invoice')
    product_id = fields.Many2one('product.product')
    @api.model
    def create(self, vals):
        res = super(EstateProperty, self).create(vals)
        product = {
            'name': res.name,
        }
        res.product_id = self.env['product.product'].create(product)
        return res

    def make_property_sold(self):
        res = super(EstateProperty, self).make_property_sold()
        journal_id = self.env['account.move'].sudo().with_context(type='out_invoice',default_journal_type='sale')._get_default_journal()
        journal = self.env['account.journal'].sudo().browse(journal_id)
        account_id = journal.default_credit_account_id.id
        if not journal_id:
            raise UserError('Please define an accounting sales journal for the company')
        invoice_lines = [
            {'product_id': self.product_id.id, 'name': '6% of the selling price', 'quantity': 1, 'price_unit': 0.06*self.selling_price, 'account_id': account_id},
            {'name': 'Administrative fees', 'quantity': 1, 'price_unit': 100.00, 'account_id': account_id}
        ]
        invoice_vals = {
            'company_id': self.env.user.company_id.id,
            'partner_id': self.buyer_id.id,
            'user_id': self.salesman_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0,0,invoice_line_vals) for invoice_line_vals in invoice_lines],
            'journal_id': journal_id,
        }
        self.invoice_id = self.env['account.invoice'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)
        return res

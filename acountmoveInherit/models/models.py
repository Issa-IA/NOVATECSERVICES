from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
class AcountMoveHerit(models.Model):
    _inherit = 'account.move'
    date_de_prelevement  = fields.Date(compute="_compute_date_prelev",string="date de prélèvement")

    @api.depends('invoice_date')
    def _compute_date_prelev(self):
        for rec in self:

            if rec.invoice_date:
                date = rec.invoice_date + relativedelta(months=1)
                rec.date_de_prelevement = date.replace(day=15)

            else:
                rec.date_de_prelevement = False

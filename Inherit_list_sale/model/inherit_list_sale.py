from odoo import models, fields, api


class StockHerit(models.Model):
    _inherit = 'sale.order'

    etiquette_maintenance = fields.Selection([('maintenance', 'Maintenance'), ('autres', 'Autres')], compute='_maintenance_etiquette', store=True)



    def _maintenance_etiquette(self):
        for rec in self:
            if rec.sale_maintnance :
                rec.write({'etiquette_maintenance': "maintenance"})


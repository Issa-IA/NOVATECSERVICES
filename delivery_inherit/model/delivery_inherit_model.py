from odoo import models, fields, api


class StockHerit(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('delivery', 'Bon de livraison'), ('done',)])
    delivery_sign = fields.Binary('Signature')


    def print_delivery(self):
        if self.state != "done":
            self.write({'state': "delivery"})
        return self.env.ref('stock.action_report_delivery').report_action(self)


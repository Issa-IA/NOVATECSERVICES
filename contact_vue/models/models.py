from odoo import models, fields, api


class   Contactinhertit(models.Model):
    _inherit = "res.partner"

    par_count = fields.Integer(string="Factures", compute="compute_mat_count")

    def compute_mat_count(self):
        for rec in self:
            fact_count = self.env['account.move'].search_count(
                [('partner_id', '=', rec.id), ('acount_maintnance', '=', 'True')])
            rec.par_count = fact_count

    def open_action_fact(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Factures maintenances',
            'res_model': 'account.move',
            'view_type': 'form',
            'domain': [('partner_id', '=', self.id), ('acount_maintnance', '=', 'True')],
            'view_mode': 'tree,form',
            'target': 'current',

        }

    parc_count = fields.Integer(string="Matériels", compute="compute_parc_count")

    def compute_parc_count(self):
        for record in self:
            parc_= self.env['fleet.vehicle'].search_count([('partner_id', '=', record.id)])
            record.parc_count = parc_

    def open_action_parc(self):
        return {

            'type': 'ir.actions.act_window',
            'name': 'Matériels',
            'res_model': 'fleet.vehicle',
            'view_type': 'form',
            'domain': [('partner_id', '=', self.id)],
            'view_mode': 'kanban,form',
            'target': 'current',

        }








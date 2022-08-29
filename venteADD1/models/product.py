from odoo import api, fields, models


class ProductProductInherit(models.Model):
    _inherit = "product.template"
    parc_ok = fields.Boolean(default=False, string="Peut être un Parc")
    #serie_number_materiel = fields.Char(string="N° serie")
    product_marque = fields.Many2one("fleet.vehicle.model.brand", string='Marque', related="product_Modele.brand_id")
    product_Modele = fields.Many2one("fleet.vehicle.model", string='Modèle')
    product_type = fields.Char(string='Type', compute="product_type_compute")

    @api.onchange('product_Modele')
    def product_type_compute(self):
        for rec in self:
            if rec.product_Modele.category_id:
                if rec.product_Modele.model_format == 'a3':
                    rec.product_type = str(rec.product_Modele.category_id.name) + ' ' + 'A3'
                elif rec.product_Modele.model_format == 'a4':
                    rec.product_type = str(rec.product_Modele.category_id.name) + ' ' + 'A4'
                else:
                    rec.product_type = str(rec.product_Modele.category_id.name)
            else:
                rec.product_type = False



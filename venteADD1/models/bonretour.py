
from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class Bonretourtable(models.Model):
    _name = 'bonretour'
    _description = 'Cree un bon retour'

    bonretour_montant = fields.Float(string="Montant du rachat")
    bonretour_leaser = fields.Many2one("typeleaser", string='Leaser')
    bonretour_dossier  = fields.Char(string="Dossier N°")
    bonretour_date_rachat_prevue = fields.Date("Date de rachat prévue")
    bonretour_article = fields.Many2one('product.product', string="Matériels rachetés")

    bonretour_serie = fields.Char(string="N° serie")
    bonretour_sale_order = fields.Many2one('sale.order', string="Matériels rachetés")


class SaleOrderbonretour(models.Model):
    _inherit    = 'sale.order'
    sale_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_sale_order')


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
    bonretour_stock_piking = fields.Many2one('stock.picking', string="Matériels rachetés")

    ##########new
    bonretour_stock_move = fields.Many2one('stock.move', string="stock move")

class StockmoveHeritretour(models.Model):
    _inherit = 'stock.move'
    acount_retour_serie = fields.Char(string="N° serie")

    ###########new
    stock_move_bonretour = fields.Many2one('bonretour', string="Bon de retour")

    def write(self, values):
        res = super(StockmoveHeritretour, self).write(values)
        # here you can do accordingly
        return self.create_serienumber()
    def create_serienumber(self):
        for record in self:
            if record.lot_ids:
                for rec in record.lot_ids:
                    if record.stock_move_bonretour:
                        record.stock_move_bonretour.update({'bonretour_serie': rec.name, })



class Stockpikingretour(models.Model):
    _inherit    = 'stock.picking'
    stock_sale = fields.Many2one('sale.order', string="Bon de commande de retour")
    stock_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_stock_piking')


class SaleOrderbonretour(models.Model):
    _inherit    = 'sale.order'

    ########## smart button to stock
    sale_stock = fields.One2many('stock.picking', string="Bon de retour", inverse_name='stock_bonretour')
    par_stock_count = fields.Integer(string="Bon de retour", compute="compute_stock_count")

    def compute_stock_count(self):
        for rec in self:
            order_count = self.env['stock.picking'].search_count([('stock_sale', '=', rec.id)])
            rec.par_stock_count = order_count

    def action_open_stock(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bon de retour',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'domain': [('stock_sale', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',

        }
    ##############################################



    sale_bonretour = fields.One2many('bonretour', string="Bon de retour", inverse_name='bonretour_sale_order')
    move_type = fields.Selection(
        [('direct', 'Aussi vite que possible'), ('one', 'Lorsque tous les articles sont prêts')], default='direct')
    procure_method=fields.Selection([('make_to_stock','Par défaut : prendre dans le stock'),('make_to_order',"	Avancé : appliquer les règles d'approvisionnement")], default='make_to_stock')


    def write(self, values):
        res = super(SaleOrderbonretour, self).write(values)
        # here you can do accordingly
        return self.create_stock_piking()

    def create_stock_piking(self):
        stock_type = self.env['stock.picking.type'].search([])

        for rec in self:
            if len(stock_type) > 1:
                sp_stock = self.env['stock.picking'].search([('stock_sale', '=', rec.id)])
                if sp_stock:
                    for retour in rec.sale_bonretour:
                        if retour not in sp_stock.stock_bonretour:

                            move=self.env['stock.move'].create(
                                {'company_id': rec.company_id.id,
                                 'date': date.today(),
                                 'location_dest_id': 8,
                                 'location_id': 5,
                                 'name': 'new',
                                 'procure_method': rec.procure_method,
                                 'product_id': retour.bonretour_article.id,
                                 'product_uom': retour.bonretour_article.uom_id.id,
                                 'product_uom_qty': 1,
                                 'quantity_done':1,
                                 'picking_id': sp_stock[0].id,
                                 'acount_retour_serie':retour.bonretour_serie,
                                 'stock_move_bonretour':retour.id,

                                 })
                            retour.bonretour_stock_move=move.id

                    #sp_stock[0].update({'state': 'assigned', })


                else:
                    if rec.sale_bonretour:
                        vals = {'name': rec.name,
                                'partner_id': rec.partner_id.id,
                                'move_type': rec.move_type,
                                'location_id': 5,
                                'location_dest_id': 8,
                                'state': 'assigned',
                                'picking_type_id': stock_type[2].id,
                                'stock_sale': rec.id
                                }
                        # self.location_dest_id.id
                        new_reception = self.env['stock.picking'].create(vals)

                        for retour in rec.sale_bonretour:
                           # product_uom = \
                           # self.env['product.template'].search_read([('id', '=', retour.bonretour_article.id)])[0]['uom_id'][0]
                            move_ne=self.env['stock.move'].create(
                                {'company_id': rec.company_id.id,
                                 'date': date.today(),
                                 'location_dest_id': 8,
                                 'location_id': 5,
                                 'name': 'new',
                                 'procure_method': rec.procure_method,
                                 'product_id': retour.bonretour_article.id,
                                 'product_uom': retour.bonretour_article.uom_id.id,
                                 'product_uom_qty': 1,
                                 'quantity_done': 1,
                                 'picking_id': new_reception.id,
                                 'acount_retour_serie': retour.bonretour_serie,
                                 'stock_move_bonretour': retour.id,

                                 })

                            retour.bonretour_stock_move = move_ne.id
                            retour.bonretour_stock_piking = new_reception.id
                        #new_reception.update({'state': 'assigned', })








"""
self.env['stock.move'].create(
                                        { 'product_uom_qty': self.qte_RMA_tr_1, 'product_id': id_article, 'picking_id': new_reception.id,
                                         'company_id':self.company_id.id, 'date': datetime.date.today(), 'location_id':loc_id,
                                          'location_dest_id':des_id, 'procure_method':self.procure_method,
                                          'name':'new','etat':'ok',
                                          'product_uom':product_uom_1
                                         })
"""

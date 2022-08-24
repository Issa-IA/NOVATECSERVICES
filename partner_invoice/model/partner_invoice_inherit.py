from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PartnerInvoiceHerit(models.Model):
    _inherit = 'res.partner'

    pfr = fields.Monetary('PFR', default=20)
    code_service = fields.Char('Code service')
    augmentation_sav = fields.Float(string='Augmentation SAV', default=0.05)
    augmentation_sav_bool= fields.Boolean(string="Augmentation SAV", default=True)
    type_facture = fields.Selection([('par_dossier', 'facture par dossier'),('tout_dossiers', 'facturer tout les dossiers')],default='par_dossier')
    moyen_de_paiement= fields.Selection([('prelevement', 'Prélèvement'),('chorus', 'Chorus'),('autres', 'Autres')],default='prelevement')






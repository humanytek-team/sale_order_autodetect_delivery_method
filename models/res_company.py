# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models


class ResCompany(models.Model):
    _inherit='res.company'

    margin_total_volume_delivery_method = fields.Float(
        'Margin in total volume calculation of delivery method',
        help='Margin in total volume calculation for selection of the delivery method')

    margin_total_weight_delivery_method = fields.Float(
        'Margin in total weight calculation of delivery method',
        help='Margin in total weight calculation for selection of the delivery method')

# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import operator

from openerp import api, models

OPERATORS = {
    '==': operator.eq,
    '<=': operator.le,
    '<': operator.lt,
    '>=': operator.ge,
    '>': operator.gt,
}


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    @api.multi
    def get_price_highest_variable(self, weight, volume):
        """Returns price of delivery"""

        self.ensure_one()
        variables = {'weight': weight, 'volume': volume}

        highest = max(
            variables.iteritems(), key=operator.itemgetter(1))[0]

        rule_items_variable_highest = self.price_rule_ids.filtered(
            lambda rule: rule.variable == highest and
            OPERATORS[rule.operator](variables[highest], rule.max_value))

        prices = list()
        for rule in rule_items_variable_highest:
            price = rule.list_base_price + rule.list_price * \
                variables[rule.variable_factor]
            prices.append(price)

        if prices:
            lowest_price = min(prices)
        else:
            lowest_price = 0

        return lowest_price

    @api.multi
    def get_price_available(self, order):
        self.ensure_one()
        total = weight = volume = quantity = 0
        total_delivery = 0.0
        ProductUom = self.env['product.uom']
        for line in order.order_line:
            if line.state == 'cancel':
                continue
            if line.is_delivery:
                total_delivery += line.price_total
            if not line.product_id or line.is_delivery:
                continue
            qty = ProductUom._compute_qty(
                line.product_uom.id, line.product_uom_qty, line.product_id.uom_id.id)
            weight += (line.product_id.weight or 0.0) * qty
            volume += (line.product_id.volume or 0.0) * qty
            quantity += qty
        total = (order.amount_total or 0.0) - total_delivery

        total = order.currency_id.with_context(date=order.date_order).compute(
            total, order.company_id.currency_id)

        return self.get_price_highest_variable(weight, volume)

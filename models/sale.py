# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import operator
import random

from openerp import api, models

OPERATORS = {
    '==': operator.eq,
    '<=': operator.le,
    '<': operator.lt,
    '>=': operator.ge,
    '>': operator.gt,
}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _get_delivery_carrier_id(self, delivery_carriers_ids=False):
        """Returns carrier selected"""

        DeliveryCarrier = self.env['delivery.carrier']
        if not delivery_carriers_ids:
            all_delivery_carriers = DeliveryCarrier.search([])
            delivery_carriers_customer = all_delivery_carriers.filtered(
                lambda dc: dc.verify_carrier(self.partner_id)
            )
        else:
            delivery_carriers_customer = delivery_carriers_ids

        volume_total = float()
        weight_total = float()
        margin_total_weight_delivery_method = \
            self.env.user.company_id.margin_total_weight_delivery_method
        margin_total_volume_delivery_method = \
            self.env.user.company_id.margin_total_volume_delivery_method

        for line in self.order_line:

            if line.product_id.volume > 0:
                volume_line = (line.product_id.volume *
                               line.product_uom_qty)

                if margin_total_volume_delivery_method > 0:
                    volume_line = volume_line + (
                        volume_line * margin_total_volume_delivery_method / 100)

                volume_total += volume_line

            if line.product_id.weight > 0:
                weight_line = (line.product_id.weight *
                               line.product_uom_qty)

                if margin_total_weight_delivery_method > 0:
                    weight_line = weight_line + (
                        weight_line * margin_total_weight_delivery_method / 100)

                weight_total += weight_line

        highest_value_volume = volume_total if volume_total > weight_total \
            else 0

        highest_value_weight = weight_total if weight_total > volume_total \
            else 0

        delivery_carriers_selected = list()

        if highest_value_volume > 0:

            for dc in delivery_carriers_customer:

                if isinstance(dc, int):
                    delivery_carrier = DeliveryCarrier.browse(dc)
                else:
                    delivery_carrier = dc

                if delivery_carrier.delivery_type == 'base_on_rule':

                    for rule in delivery_carrier.price_rule_ids:

                        if rule.variable == 'volume' and \
                                OPERATORS[rule.operator](
                                    highest_value_volume, rule.max_value):

                            try:

                                dc_in_selected = (
                                    dc_data for dc_data in
                                    delivery_carriers_selected
                                    if dc_data['dc'] == delivery_carrier).next()

                                if rule.list_base_price < \
                                        dc_in_selected['price']:

                                    dc_in_selected['price'] = \
                                        rule.list_base_price

                            except StopIteration:

                                delivery_carriers_selected.append({
                                    'dc': delivery_carrier,
                                    'price': rule.list_base_price,
                                })

        if highest_value_weight > 0:

            for dc in delivery_carriers_customer:

                if isinstance(dc, int):
                    delivery_carrier = DeliveryCarrier.browse(dc)
                else:
                    delivery_carrier = dc

                delivery_carrier = DeliveryCarrier.browse(dc)

                if delivery_carrier.delivery_type == 'base_on_rule':

                    for rule in delivery_carrier.price_rule_ids:

                        if rule.variable == 'weight' and \
                                OPERATORS[rule.operator](
                                    highest_value_weight, rule.max_value):

                            try:

                                dc_in_selected = (
                                    dc_data for dc_data in
                                    delivery_carriers_selected
                                    if dc_data['dc'] == delivery_carrier).next()

                                if rule.list_base_price < \
                                        dc_in_selected['price']:

                                    dc_in_selected['price'] = \
                                        rule.list_base_price

                            except StopIteration:

                                delivery_carriers_selected.append({
                                    'dc': delivery_carrier,
                                    'price': rule.list_base_price,
                                })
        if delivery_carriers_selected:

            min_price = min([
                dc['price']
                for dc in delivery_carriers_selected
            ])

            delivery_carriers_selected = [
                dc['dc']
                for dc in delivery_carriers_selected
                if dc['price'] == min_price]

            carrier_id = random.choice(delivery_carriers_selected)

        else:

            carrier_id = False

        return carrier_id

    @api.multi
    def button_dummy(self):
        super(SaleOrder, self).button_dummy()

        self.carrier_id = self._get_delivery_carrier_id()

# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import tools
from osv import fields,osv

class account_invoice_report(osv.osv):
    _name = "account.invoice.report"
    _description = "Invoices Statistics"
    _auto = False
    _rec_name = 'date'
    _columns = {
        'date': fields.date('Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'month': fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'),
            ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'),
            ('10','October'), ('11','November'), ('12','December')], 'Month', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'product_qty':fields.float('Qty', readonly=True),
        'uom_name': fields.char('Reference UoM', size=128, readonly=True),
        'payment_term': fields.many2one('account.payment.term', 'Payment Term', readonly=True),
        'period_id': fields.many2one('account.period', 'Force Period', domain=[('state','<>','done')], readonly=True),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position', readonly=True),
        'currency_id': fields.many2one('res.currency', 'Currency', readonly=True),
        'categ_id': fields.many2one('product.category','Category of Product', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Journal', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'user_id': fields.many2one('res.users', 'Salesman', readonly=True),
        'price_total': fields.float('Total Without Tax', readonly=True),
        'price_average': fields.float('Average Price', readonly=True, group_operator="avg"),
        'currency_rate': fields.float('Currency Rate', readonly=True),
        'nbr':fields.integer('# of Lines', readonly=True),
        'type': fields.selection([
            ('out_invoice','Customer Invoice'),
            ('in_invoice','Supplier Invoice'),
            ('out_refund','Customer Refund'),
            ('in_refund','Supplier Refund'),
            ],'Type', readonly=True),
        'state': fields.selection([
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('paid','Done'),
            ('cancel','Cancelled')
            ], 'Invoice State', readonly=True),
        'date_due': fields.date('Due Date', readonly=True),
        'address_contact_id': fields.many2one('res.partner.address', 'Contact Address Name', readonly=True),
        'address_invoice_id': fields.many2one('res.partner.address', 'Invoice Address Name', readonly=True),
        'account_id': fields.many2one('account.account', 'Account',readonly=True),
        'account_line_id': fields.many2one('account.account', 'Account Line',readonly=True),
        'partner_bank_id': fields.many2one('res.partner.bank', 'Bank Account',readonly=True),
        'residual': fields.float('Total Residual', readonly=True),
        'delay_to_pay': fields.float('Avg. Delay To Pay', readonly=True, group_operator="avg"),
        'due_delay': fields.float('Avg. Due Delay', readonly=True, group_operator="avg"),
    }
    _order = 'date desc'
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'account_invoice_report')
        view_sql = """
        CREATE or REPLACE VIEW account_invoice_report as (
            %s
            FROM (
                %s %s %s
            ) AS sub
            JOIN res_currency_rate cr ON (cr.currency_id = sub.currency_id)
            WHERE
                cr.id IN (SELECT id
                          FROM res_currency_rate cr2
                          WHERE (cr2.currency_id = sub.currency_id)
                              AND ((sub.date IS NOT NULL AND cr.name <= sub.date)
                                    OR (sub.date IS NULL AND cr.name <= NOW()))
                          ORDER BY name DESC LIMIT 1)
        )
        """ % (self._select(), self._sub_select(), self._from(), self._group_by())
        cr.execute(view_sql)

    def _select(self):
        return """
            SELECT sub.id, sub.date, sub.year, sub.month, sub.day, sub.product_id, sub.partner_id,
                sub.payment_term, sub.period_id, sub.uom_name, sub.currency_id, sub.journal_id,
                sub.fiscal_position, sub.user_id, sub.company_id, sub.nbr, sub.type, sub.state,
                sub.categ_id, sub.date_due, sub.account_id, sub.account_line_id, sub.partner_bank_id,
                sub.product_qty, sub.price_total / cr.rate as price_total, sub.price_average /cr.rate as price_average,
                cr.rate as currency_rate, sub.residual / cr.rate as residual, sub.due_delay,sub.delay_to_pay
        """

    def _sub_select(self):
        return """
               SELECT min(ail.id) as id,
                    ai.date_invoice as date,
                    to_char(ai.date_invoice::timestamp with time zone, 'YYYY'::text) AS year,
                    to_char(ai.date_invoice::timestamp with time zone, 'MM'::text) AS month,
                    to_char(ai.date_invoice::timestamp with time zone, 'YYYY-MM-DD'::text) AS day,
                    ail.product_id, ai.partner_id, ai.payment_term, ai.period_id,
                    CASE
                     WHEN u.uom_type::text <> 'reference'::text
                        THEN ( SELECT product_uom.name
                               FROM product_uom
                               WHERE product_uom.uom_type::text = 'reference'::text
                                AND product_uom.active
                                AND product_uom.category_id = u.category_id LIMIT 1)
                        ELSE u.name
                    END AS uom_name,
                    ai.currency_id, ai.journal_id, ai.fiscal_position, ai.user_id, ai.company_id,
                    count(ail.*) AS nbr,
                    ai.type,ai.state,pt.categ_id,
                    ai.date_due,ai.account_id,ail.account_id AS account_line_id,
                    ai.partner_bank_id,
                    SUM(CASE
                         WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN (- ail.quantity) / u.factor
                            ELSE ail.quantity / u.factor
                        END) AS product_qty,
                    SUM(CASE
                         WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN - ail.price_subtotal
                            ELSE ail.price_subtotal
                        END) AS price_total,
                    CASE
                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN SUM(- ail.price_subtotal)
                        ELSE SUM(ail.price_subtotal)
                    END / CASE
                           WHEN SUM(ail.quantity / u.factor) <> 0::numeric
                               THEN CASE
                                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                                        THEN SUM((- ail.quantity) / u.factor)
                                        ELSE SUM(ail.quantity / u.factor)
                                    END
                               ELSE 1::numeric
                          END AS price_average,
                    CASE
                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN - ai.residual
                        ELSE ai.residual
                    END / CASE
                           WHEN (( SELECT count(l.id) AS count
                                   FROM account_invoice_line l
                                   LEFT JOIN account_invoice a ON a.id = l.invoice_id
                                   WHERE a.id = ai.id)) <> 0
                               THEN ( SELECT count(l.id) AS count
                                      FROM account_invoice_line l
                                      LEFT JOIN account_invoice a ON a.id = l.invoice_id
                                      WHERE a.id = ai.id)
                               ELSE 1::bigint
                          END::numeric AS residual,
                    sum((select extract(epoch from avg(date_trunc('day',aml.date_created)-date_trunc('day',l.create_date)))/(24*60*60)::decimal(16,2)
                        from account_move_line as aml
                        left join account_invoice as a ON (a.move_id=aml.move_id)
                        left join account_invoice_line as l ON (a.id=l.invoice_id)
                        where a.id=ai.id)) as delay_to_pay,
                    sum((select extract(epoch from avg(date_trunc('day',a.date_due)-date_trunc('day',a.date_invoice)))/(24*60*60)::decimal(16,2)
                        from account_move_line as aml
                        left join account_invoice as a ON (a.move_id=aml.move_id)
                        left join account_invoice_line as l ON (a.id=l.invoice_id)
                        where a.id=ai.id)) as due_delay

        """
    
    def _from(self):
        return """                
                FROM account_invoice_line AS ail
                LEFT JOIN account_invoice AS ai ON (ai.id=ail.invoice_id)
                LEFT JOIN product_product pr ON (pr.id=ail.product_id)
                LEFT JOIN product_template pt ON (pt.id=pr.product_tmpl_id)
                LEFT JOIN product_uom u ON (u.id=ail.uos_id)
        """

        
    def _group_by(self):
               return """
                  GROUP BY ail.product_id, ai.date_invoice, ai.id,
                    to_char(ai.date_invoice::timestamp with time zone, 'YYYY'::text),
                    to_char(ai.date_invoice::timestamp with time zone, 'MM'::text),
                    to_char(ai.date_invoice::timestamp with time zone, 'YYYY-MM-DD'::text),
                    ai.partner_id,
                    ai.payment_term,
                    ai.period_id,
                    u.name,
                    ai.currency_id,
                    ai.journal_id,
                    ai.fiscal_position,
                    ai.user_id,
                    ai.company_id,
                    ai.type,
                    ai.state,
                    pt.categ_id,
                    ai.date_due,
                    ai.address_contact_id,
                    ai.address_invoice_id,
                    ai.account_id,
                    ail.account_id,
                    ai.partner_bank_id,
                    ai.residual,
                    ai.amount_total,
                    u.uom_type,
                    u.category_id
               """

account_invoice_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

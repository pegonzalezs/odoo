[![Build Status](http://runbot.odoo.com/runbot/badge/flat/1/9.0.svg)](http://runbot.odoo.com/runbot)
[![Tech Doc](http://img.shields.io/badge/9.0-docs-8f8f8f.svg?style=flat)](http://www.odoo.com/documentation/9.0)
[![Help](http://img.shields.io/badge/9.0-help-8f8f8f.svg?style=flat)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](http://img.shields.io/badge/9.0-nightly-8f8f8f.svg?style=flat)](http://nightly.odoo.com/)

This branch: 9.0.Fernuni
------------------------
It is similar to the base 9.0 branch but with the following patches (required by sett_hr):
 - https://svn.brain-tec.ch/patches/90/90--sett_hr--make_uid_available_in_views.patch
 - https://svn.brain-tec.ch/patches/90/90--sett_hr--send_readonly_field_values_to_server.patch
 - https://svn.brain-tec.ch/patches/90/90--sett_hr--set_attribute_depends_without_bt_swissdec.patch

Odoo
----

Odoo is a suite of web based open source business apps.

The main Odoo Apps include an <a href="https://www.odoo.com/page/crm">Open Source CRM</a>, <a href="https://www.odoo.com/page/website-builder">Website Builder</a>, <a href="https://www.odoo.com/page/e-commerce">eCommerce</a>, <a href="https://www.odoo.com/page/project-management">Project Management</a>, <a href="https://www.odoo.com/page/accounting">Billing &amp; Accounting</a>, <a href="https://www.odoo.com/page/point-of-sale">Point of Sale</a>, <a href="https://www.odoo.com/page/employees">Human Resources</a>, Marketing, Manufacturing, Purchase Management, ...  

Odoo Apps can be used as stand-alone applications, but they also integrate seamlessly so you get
a full-featured <a href="https://www.odoo.com">Open Source ERP</a> when you install several Apps.


Getting started with Odoo
-------------------------
For a standard installation please follow the <a href="https://www.odoo.com/documentation/9.0/setup/install.html">Setup instructions</a>
from the documentation.

If you are a developer you may type the following command at your terminal:

    wget -O- https://raw.githubusercontent.com/odoo/odoo/9.0/odoo.py | python

Then follow <a href="https://www.odoo.com/documentation/9.0/tutorials.html">the developer tutorials</a>


For Odoo employees
------------------

To add the odoo-dev remote use this command:

    $ ./odoo.py setup_git_dev

To fetch odoo merge pull requests refs use this command:

    $ ./odoo.py setup_git_review


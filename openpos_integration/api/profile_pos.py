import base64
import binascii
import json
from urllib.parse import urlencode, urlparse

import frappe
import frappe.client
import frappe.handler
from frappe import _
from frappe.utils.data import sbool
from frappe.utils.response import build_response


@frappe.whitelist()
def get_config_for_unicenta():
    name = None
    parts = frappe.request.path[1:].split("/", 3)
    data = {}
    if len(parts) > 3:
        name = parts[3]

    if(name != None):
        posProfile = frappe.get_doc("POS Profile", name).as_dict()
        data['name'] = posProfile.name
        data['code'] = posProfile.code
        data['selling_price_list'] = posProfile.selling_price_list
        data['warehouse'] = posProfile.warehouse
        data['users'] = get_users(posProfile.applicable_for_users)
        data['payments'] = get_payments(posProfile.payments)

    frappe.local.response.update({"data": data})
    return build_response("json")


def get_users(users):
    data = []

    for user in users:
        userList = {}
        docUser = frappe.get_doc("User", user.user).as_dict()
        userList["full_name"] = docUser.full_name
        userList["role_profile_name"] = docUser.role_profile_name
        userList["name"] = docUser.name
        userList["enabled"] = docUser.enabled
        data.append(userList)
    return data


def get_payments(payments):
    data = []

    for payment in payments:
        paymentList = {}
        docPayment = frappe.get_doc(
            "Mode of Payment", payment.mode_of_payment).as_dict()
        if(docPayment.external_ref):
            if(docPayment.accounts[0]):

                paymentList["name"] = docPayment.name
                paymentList["external_ref"] = docPayment.external_ref
                paymentList["accounts"] = docPayment.accounts[0].default_account

                data.append(paymentList)
    return data

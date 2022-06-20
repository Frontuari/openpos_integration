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
def get_all_products_for_importation():
    items = frappe.db.get_list('Item', filters=[['is_for_unicenta', '=', "1"]])
    data = []
    for item in items:
        docItem = frappe.get_doc("Item", item.name).as_dict()

        docItem["price_list"] = getAllListPriceUnicenta(docItem.item_code)

        data.append(docItem)

    frappe.local.response.update({"data": data})

    return build_response("json")


def getAllListPriceUnicenta(item_code):
    priceList = []

    for currency in ("VES", "USD"):
        for is_sell in (1, 0):

            listPrice = getListPrice(item_code, currency, is_sell)

            if(listPrice != None):
                priceList.append(listPrice)
    return priceList


def getListPrice(item_code, currency, selling):
    result = None
    price_lists = frappe.get_list(
        "Item Price", fields=("currency", "price_list_rate", "selling", "item_code"), filters={"selling": selling, "item_code": item_code, "currency": currency}, order_by="creation desc", limit="1")

    if(price_lists):
        if(price_lists[0]):
            result = price_lists[0]

    return result

import os, sys
import requests


def notify_channel(store_name, in_stock=False):
    message = "PS5 consoles are " + ("" if in_stock else "not ") + "in stock at " + store_name
    requests.post(open('webhook-url.txt').read(), json={"text": message})

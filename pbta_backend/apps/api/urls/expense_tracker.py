from django.urls import path

from ..routes import expense_tracker

expense_tracker_urls = [path("add-transaction/", expense_tracker.add_transaction)]

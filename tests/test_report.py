from unittest.mock import MagicMock

from report import dbParser
from report.service import get_daily_report


def test_get_daily_report():
    report = get_daily_report('2019-08-01')
    assert isinstance(report, dict)
    assert 'items' in report
    assert 'total_discount_amount' in report
    assert 'discount_rate_avg' in report
    assert 'order_total_avg' in report
    assert 'commissions' in report
    assert report['commissions']['total']
    assert report['commissions']['promotions']
    assert report['commissions']['order_average']


def test_get_daily_report_mock(monkeypatch):
    # Mock the database methods called by the function
    total_number_of_items_sold_per_day = MagicMock(return_value=[(10,)])
    total_number_of_customers_per_day = MagicMock(return_value=[(5,)])
    total_discount_per_day = MagicMock(return_value=[(3.50,)])
    avg_discount_per_items_per_day = MagicMock(return_value=[(0.35,)])
    avg_per_items_per_day = MagicMock(return_value=[(2.50,)])
    total_commission_per_day = MagicMock(return_value=[(1.25,)])
    total_avg_commission_per_day = MagicMock(return_value=[(0.25,)])
    get_commission_per_each_promotion = MagicMock(return_value=[("promo1", 0.5), ("promo2", 0.75)])

    # Set the mocked methods to be returned by the corresponding methods in the dbParser module
    monkeypatch.setattr(dbParser.DailyDbReport, "total_number_of_items_sold_per_day",
                        total_number_of_items_sold_per_day)
    monkeypatch.setattr(dbParser.DailyDbReport, "total_number_of_customers_per_day", total_number_of_customers_per_day)
    monkeypatch.setattr(dbParser.DailyDbReport, "total_discount_per_day", total_discount_per_day)
    monkeypatch.setattr(dbParser.DailyDbReport, "AvgDiscountPerItemsPerDay", avg_discount_per_items_per_day)
    monkeypatch.setattr(dbParser.DailyDbReport, "AvgPerItemsPerDay", avg_per_items_per_day)
    monkeypatch.setattr(dbParser.DailyDbReport, "TotalCommissionPerDay", total_commission_per_day)
    monkeypatch.setattr(dbParser.DailyDbReport, "TotalAvgCommissionPerDay", total_avg_commission_per_day)
    monkeypatch.setattr(dbParser.DailyDbReport, "GetCommisionPerEachPromotion", get_commission_per_each_promotion)

    # Call the function with a specific date
    report = get_daily_report("2019-08-01")

    # Assert that the expected dictionary is returned
    assert report == {
        "items": 10,
        "customers": 5,
        "total_discount_amount": 3.50,
        "discount_rate_avg": 0.35,
        "order_total_avg": 2.50,
        "commissions": {
            "promotions": {"promo1": 0.5, "promo2": 0.75},
            "total": 1.25,
            "order_average": 0.25
        }
    }

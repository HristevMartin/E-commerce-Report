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

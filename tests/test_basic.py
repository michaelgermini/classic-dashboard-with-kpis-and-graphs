from services.data_loader import load_sample_data


def test_load_data_smoke():
    df = load_sample_data()
    assert not df.empty
    for col in ["date", "customer_id", "segment", "product", "balance", "delinquent"]:
        assert col in df.columns


def test_intentional_failure():
    # python-ci が失敗を正しく報告できるかを確かめるための、わざと失敗するテスト
    assert 1 + 1 == 3

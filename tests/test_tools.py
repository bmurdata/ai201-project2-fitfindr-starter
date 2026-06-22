from tools import search_listings, suggest_outfit, create_fit_card
from utils import data_loader
def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == [] or "error" in results   # empty list, no exception

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    for item in results:
        if "error" in item:
            assert True
        else:
            assert all(int(item["price"]) <= 10 for item in results)

def test_get_outfit():
    restults=search_listings('vintage graphic tee','M',30)
    testitem=restults[0]
    testwardrobe=data_loader.get_example_wardrobe()
    assert isinstance(suggest_outfit(testitem,testwardrobe),str)
def test_get_fit_card():
    restults=search_listings('vintage graphic tee','M',30)
    testitem=restults[0]
    testwardrobe=data_loader.get_example_wardrobe()
    outfit=suggest_outfit(testitem,testwardrobe)
    assert isinstance(create_fit_card(outfit,testitem),str)
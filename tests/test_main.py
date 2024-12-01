import pytest
from playwright.sync_api import sync_playwright
import agentql
from main import get_response, write_response_to_xlsx, Product, ProductList
import os
import polars as pl


@pytest.fixture
def mock_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = agentql.wrap(browser.new_page())
        yield page
        browser.close()


@pytest.fixture
def sample_data():
    return {
        "products": [
            {
                "product_name": "Test Product 1",
                "product_price": 19.99,
                "product_description": "Test Description 1"
            },
            {
                "product_name": "Test Product 2",
                "product_price": 29.99,
                "product_description": "Test Description 2"
            }
        ]
    }


def test_get_response(mock_page):
    # Navigate to the test site
    mock_page.goto("https://webscraper.io/test-sites/e-commerce/allinone")
    
    # Get the response
    response = get_response(mock_page)
    
    # Validate response structure
    assert isinstance(response, dict)
    assert "products" in response
    assert isinstance(response["products"], list)
    
    # Validate data types using Pydantic model
    model = ProductList(**response)
    assert all(isinstance(product, Product) for product in model.products)


def test_write_response_to_xlsx(sample_data, tmp_path):
    # Create a temporary file path
    test_file = tmp_path / "test_output.xlsx"
    
    # Write sample data to Excel
    write_response_to_xlsx(sample_data["products"], str(test_file))
    
    # Verify file was created
    assert os.path.exists(test_file)
    
    # Read back the data and verify contents
    df = pl.read_excel(test_file)
    
    # Check column names
    expected_columns = ["product_name", "product_price", "product_description"]
    assert all(col in df.columns for col in expected_columns)
    
    # Check data values
    assert df.shape[0] == 2  # Two rows of data
    assert df["product_name"][0] == "Test Product 1"
    assert df["product_price"][0] == 19.99
    assert df["product_description"][0] == "Test Description 1"


def test_product_model():
    # Test valid product data
    product_data = {
        "product_name": "Test Product",
        "product_price": 19.99,
        "product_description": "Test Description"
    }
    product = Product(**product_data)
    assert product.product_name == "Test Product"
    assert product.product_price == 19.99
    assert product.product_description == "Test Description"

    # Test invalid product data
    with pytest.raises(ValueError):
        Product(
            product_name="Test Product",
            product_price="invalid_price",  # Should be float
            product_description="Test Description"
        )


def test_product_list_model():
    # Test valid model data
    model_data = {
        "products": [
            {
                "product_name": "Test Product 1",
                "product_price": 19.99,
                "product_description": "Test Description 1"
            },
            {
                "product_name": "Test Product 2",
                "product_price": 29.99,
                "product_description": "Test Description 2"
            }
        ]
    }
    model = ProductList(**model_data)
    assert len(model.products) == 2
    assert all(isinstance(product, Product) for product in model.products)

    # Test invalid model data (empty products list)
    with pytest.raises(ValueError):
        ProductList(products="not_a_list")  # Should be a list

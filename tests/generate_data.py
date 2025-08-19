import pandas as pd

def generate_data(n=50000):
    return pd.DataFrame({
        'id': range(n),
        'title': [f'Product {i}' for i in range(n)],
        'price': [i % 100 for i in range(n)],
        'category': ['Electronics'] * n,
        'description': ['Test product'] * n
    })

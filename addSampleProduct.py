from website import create_app
from website.models import db, Product

app = create_app()

with app.app_context():
    sample_product = Product(
        name='Gato Product',
        description='This is a gato product.',
        price=19.99,
        quantity=10,
        image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/960px-Cat_August_2010-4.jpg'
    )
    db.session.add(sample_product)
    db.session.commit()
    print('Sample product added to the database.')

    # Fetch and print all products to verify insertion
    products = Product.query.all()
    for product in products:
        print(product.name, product.description, product.price, product.quantity, product.image_url)
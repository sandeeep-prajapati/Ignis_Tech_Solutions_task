To create a Django REST API that displays the data stored in the SQLite database by your Scrapy spider, follow these steps:

### 1. **Set Up Django Project**
   - **Create a Django Project:**
     ```bash
     django-admin startproject nobero_api
     cd nobero_api
     ```

   - **Create an App:**
     ```bash
     python manage.py startapp products
     ```

### 2. **Set Up Models**
   - **Define Models in `products/models.py`:**
     ```python
     from django.db import models

     class Product(models.Model):
         category = models.CharField(max_length=255)
         url = models.URLField()
         title = models.CharField(max_length=255)
         img_url = models.URLField()
         bought = models.CharField(max_length=255, null=True, blank=True)
         description = models.TextField()
         price = models.CharField(max_length=50, null=True, blank=True)
         MPR = models.CharField(max_length=50, null=True, blank=True)
         color = models.CharField(max_length=100, null=True, blank=True)
         size = models.CharField(max_length=255, null=True, blank=True)

         def __str__(self):
             return self.title
     ```

   - **Apply Migrations:**
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

### 3. **Integrate Django with Existing SQLite Database**
   - **Configure Database in `settings.py`:**
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': BASE_DIR / "nobero_products.db",  # Use your existing SQLite DB file
         }
     }
     ```

### 4. **Create Serializers**
   - **Create Serializer in `products/serializers.py`:**
     ```python
     from rest_framework import serializers
     from .models import Product

     class ProductSerializer(serializers.ModelSerializer):
         class Meta:
             model = Product
             fields = '__all__'
     ```

### 5. **Create Views**
   - **Create Views in `products/views.py`:**
     ```python
     from rest_framework import viewsets
     from .models import Product
     from .serializers import ProductSerializer

     class ProductViewSet(viewsets.ModelViewSet):
         queryset = Product.objects.all()
         serializer_class = ProductSerializer
     ```

### 6. **Set Up URLs**
   - **Update `products/urls.py`:**
     ```python
     from django.urls import path, include
     from rest_framework.routers import DefaultRouter
     from .views import ProductViewSet

     router = DefaultRouter()
     router.register(r'products', ProductViewSet)

     urlpatterns = [
         path('', include(router.urls)),
     ]
     ```

   - **Include `products/urls.py` in `nobero_api/urls.py`:**
     ```python
     from django.contrib import admin
     from django.urls import path, include

     urlpatterns = [
         path('admin/', admin.site.urls),
         path('api/', include('products.urls')),
     ]
     ```

### 7. **Test the API**
   - **Run the Django Development Server:**
     ```bash
     python manage.py runserver
     ```
   - **Access the API:**
     Visit `http://127.0.0.1:8000/api/products/` in your browser to see the list of products.








Certainly! Here’s how you can modify the React components to use the `fetch` API instead of Axios.

### 1. **ProductList Component**

This component fetches and displays a list of products:

```jsx
// src/components/ProductList.js
import React, { useState, useEffect } from 'react';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/products/')
            .then(response => response.json())
            .then(data => {
                setProducts(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error loading products!</p>;

    return (
        <div>
            <h1>Product List</h1>
            <ul>
                {products.map(product => (
                    <li key={product.id}>
                        <h2>{product.title}</h2>
                        <img src={product.img_url} alt={product.title} width="100" />
                        <p>Category: {product.category}</p>
                        <p>Price: {product.price}</p>
                        <p>Description: {product.description}</p>
                        <p>Color: {product.color}</p>
                        <p>Size: {product.size}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ProductList;
```

### 2. **ProductDetail Component**

This component fetches and displays details for a single product. Make sure to use React Router to pass the product ID as a URL parameter.

```jsx
// src/components/ProductDetail.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const ProductDetail = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/products/${id}/`)
            .then(response => response.json())
            .then(data => {
                setProduct(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err);
                setLoading(false);
            });
    }, [id]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error loading product details!</p>;
    if (!product) return <p>Product not found!</p>;

    return (
        <div>
            <h1>{product.title}</h1>
            <img src={product.img_url} alt={product.title} width="200" />
            <p>Category: {product.category}</p>
            <p>Price: {product.price}</p>
            <p>Description: {product.description}</p>
            <p>Color: {product.color}</p>
            <p>Size: {product.size}</p>
        </div>
    );
};

export default ProductDetail;
```

### 3. **App Component**

Update `App.js` to include routing for the components:

```jsx
// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<ProductList />} />
                <Route path="/products/:id" element={<ProductDetail />} />
            </Routes>
        </Router>
    );
}

export default App;
```

### Summary

- **`ProductList.js`**: Uses `fetch` to retrieve and display a list of products.
- **`ProductDetail.js`**: Uses `fetch` to retrieve and display details for a single product based on the ID from the URL parameters.
- **`App.js`**: Sets up routing using React Router.

With these components, you should be able to fetch and display product data from your Django REST API using the `fetch` API. If you encounter any issues or need further adjustments, let me know!






import React, { useState, useEffect } from 'react';


export default function Product_list() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/products/')
            .then(response => response.json())
            .then(data => {
                setProducts(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error loading products!</p>;

    return (
        <div>
            <h1>Product List</h1>
            <ul>
                {products.map(product => (
                    <li key={product.id}>
                        <h2>{product.title}</h2>
                        <img src={product.img_url} alt={product.title} width="100" />
                        <p>Category: {product.category}</p>
                        <p>Price: {product.price}</p>
                        <p>Description: {product.description}</p>
                        <p>Color: {product.color}</p>
                        <p>Size: {product.size}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Product_list from './components/Product_list';
import ProductDetail from './components/ProductDetail';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Product_list />} />
                <Route path="/products/:id" element={<ProductDetail />} />
            </Routes>
        </Router>
    );
}

export default App;
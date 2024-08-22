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
        <>
        <h1 className='text-3xl p-[70px] font-bold text-yellow-300 text-center'>
                Product Detail Page
            </h1>
        <div className="p-6 mb-10 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4">
            <h1 className="text-2xl font-bold">{product.title}</h1>
            <img src={product.img_url.startsWith('http') ? product.img_url : `https:${product.img_url}`} alt={product.title} className="w-full h-auto rounded-lg" />
            <p className="text-lg"><strong>Category:</strong> {product.category}</p>
            <p className="text-lg"><strong>Price:</strong> ₹{product.price}</p>
            <p className="text-lg"><strong>MPR:</strong> ₹{product.MPR}</p>
            <p className="text-lg"><strong>Bought:</strong> {product.bought}</p>
            <p className="text-lg"><strong>Description:</strong> {product.description}</p>
            <p className="text-lg"><strong>Color:</strong> {product.color}</p>
            <p className="text-lg"><strong>Size:</strong> {product.size}</p>
        </div>
        </>
    );
};

export default ProductDetail;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

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
    <div className="bg-cover bg-center bg-no-repeat h-screen" style={{ backgroundImage: 'url((link unavailable))' }}>
      <h1 className="p-10 text-center text-3xl font-bold text-purple-600">Product List</h1>
      <div className="flex flex-wrap justify-center">
        {products.map(product => (
          <div key={product.id} className="m-4 p-4 border border-gray-200 rounded-md bg-white">
            <img src={product.img_url} alt={product.title} className="w-full h-80 object-cover" />
            <br></br>
            <h2 className="text-2xl text-yellow-600 font-bold">{product.title}</h2>
            <br></br>
            <p><span className='font-bold'>Category:</span> {product.category}</p>
            <p><span className='font-bold'>Price:</span> {product.price}</p>
            <p><span className='font-bold'>Description:</span>  {product.description}</p>
            <p><span className='font-bold'>Color:</span> {product.color}</p>
            <p><span className='font-bold text-red-500 text-xl'>Size: </span> {product.size}</p>
            <Link to={`/products/${product.id}`}>
              <button className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
                View Details
              </button>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

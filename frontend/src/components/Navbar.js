import React from 'react';
import './Navbar.css'; // Assume you create a CSS file for each component for styles

function Navbar() {
  return (
    <nav className="navbar">
      <h1>MyApp</h1>
      <ul className="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  );
}

export default Navbar;

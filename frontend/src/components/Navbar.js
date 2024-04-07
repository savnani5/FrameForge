import React from 'react';
import './Navbar.css'; // Assume you create a CSS file for each component for styles

function Navbar() {
  return (
    <nav className="navbar">
      <h1>Frameforge</h1>
      <ul className="nav-links">
        <li><a href="/">Video</a></li>
        <li><a href="/image">Image</a></li>
        <li><a href="/audio">Audio</a></li>
        <li><a href="/text">Text</a></li>
      </ul>
    </nav>
  );
}

export default Navbar;

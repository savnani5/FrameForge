// components/NavigationBar.js

import React from 'react';
import { NavLink } from 'react-router-dom';

const NavigationBar = () => {
  return (
    <nav className="navbar">
      <NavLink to="/video" activeClassName="active-link">Video</NavLink>
      <NavLink to="/audio" activeClassName="active-link">Audio</NavLink>
      <NavLink to="/text" activeClassName="active-link">Text</NavLink>
      <NavLink to="/image" activeClassName="active-link">Image</NavLink>
    </nav>
  );
};

export default NavigationBar;

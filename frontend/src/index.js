import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import Odometer from 'react-odometerjs';
import 'odometer/themes/odometer-theme-minimal.css';

import HopeLogo from './images/hope-logo.svg';
import AWLogo from './images/aw-logo-black.png';
import DuckDuckGoLogo from './images/duckduckgo.svg';
import Bottle from './images/bottle.svg';

function App() {
  const [bottles, setBottles] = useState(0);
  const [emissions, setEmissions] = useState(0);

  useEffect(() => {
    setInterval(fetchBottles, 5000);
    setInterval(fetchEmissions, 5000);
  });

  const fetchBottles = async () => {
    try {
      const bottleRes = await fetch("https://8ndi1e.deta.dev/total_bottles");
      const bottleJSON = await bottleRes.json();
      setBottles(bottleJSON);
    } catch {}
  }

  const fetchEmissions = async () => {
    try {
      const emissionRes = await fetch("https://8ndi1e.deta.dev/total_emissions");
      const emissionJSON = await emissionRes.json();
      setEmissions(emissionJSON);
    } catch {
    }
  }

  return (
    <div className="app">
      <img className="bottle" src={Bottle} alt="Bottle" />
      <div className="left-container">
        <div className="header">
          <span>At AW22, we have saved:</span>
        </div>
        <div className="odometer-wrapper">
          <Odometer value={bottles} animation='count' duration={10000} />
          <span className="odometer-label">plastic bottles</span>
        </div>
        <div className="odometer-wrapper">
          <Odometer value={emissions} animation='count' duration={10000} format='(,ddd)' />
          <span className="odometer-label">g - CO₂</span>
        </div>
      </div>
      <div className="right-container">
        <div className="logo-wrapper">
          <img className="logo" src={HopeLogo} alt="Hope Logo" />
          <p className="x">X</p>
          <img className="logo" src={AWLogo} alt="Advertising Week Logo" />
        </div>
        <p></p>
        <div className="powered-by-wrapper">
          <p className="powered-by">Powered by:</p>
          <img className="logo" src={DuckDuckGoLogo} alt="Duck Duck Go Logo" />
          <p className="tagline">Tap into customers who don't use Google search.</p>
        </div>
      </div>
    </div>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

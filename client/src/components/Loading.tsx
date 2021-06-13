import React from 'react';
import '../App.css';
import loadingImg from '../assets/images/spinner.svg';

const Loading = () => {
  return (
    <div className="loading-popup">
      <div className="loading-container">
        <img src={loadingImg} className="loading-image" alt="loading" />
      </div>
    </div>
  )
}

export default Loading;

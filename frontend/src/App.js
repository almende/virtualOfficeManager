import React from 'react';
import logo from './logo.svg';
import './App.css';
import SimpleTable from './components/Table';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {SimpleTable()}
      </header>
    </div>
  );
}

export default App;

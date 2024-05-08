import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { AppProvider } from './store/store'
import { BrowserRouter, Routes, Route } from 'react-router-dom';


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <AppProvider>
      <BrowserRouter>
            <Routes>
              <Route path="/*" element={<App />} />
            </Routes>
      </BrowserRouter>
    </AppProvider>
  </React.StrictMode>
)


import './App.css';
import { Route, Routes, BrowserRouter as Router } from 'react-router-dom';
import Navbar from './components/public/Navbar';
import Main from './components/public/Main';
import Footer from './components/public/Footer';
import About from './components/public/About';
import Projects from './components/public/Projects';

function App() {
  return (
    <div className="App">
      <Router>
      <Navbar />
      <Routes>
        <Route index element={<Main/>}></Route>
        <Route path={'/about'}  element={<About/>}></Route>
        {/* <Route path={'/projects'}  element={<Projects/>}></Route> */}
      </Routes>
      <Footer />

      </Router>
    </div>
  );
}

export default App;

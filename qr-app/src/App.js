import './App.css';
import './fonts.css'
import Header from './components/Header';
import Footer from './components/Footer';
import QRCodeGen from "./components/QRCodeGen";

function App() {
  return (
    <div className="bg-gray-50">
      <Header />
      <main>
        <QRCodeGen />
      </main>
      <Footer />
    </div>
  );
}

export default App;

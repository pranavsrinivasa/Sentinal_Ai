import ButtonGradient from "./assets/svg/ButtonGradient";
import Benefits from "./components/Benefits";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import Create from "./components/Create";
import MasterAgent from "./components/Master";
import Structure from './components/Structure'

const App = () => {
  return (
    <>
      <div className="pt-[4.75rem] lg:pt-[5.25rem] overflow-hidden">
        <Header />
        <Hero />
        <Benefits />
        <Upload />
        <Create />
        <Structure/>
        <Chat />
        <MasterAgent />
        <Footer />
      </div>

      <ButtonGradient />
    </>
  );
};

export default App;

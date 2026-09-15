import Nav from "./components/Nav"
import Hero from "./components/Hero"
import Manifesto from "./components/Manifesto"
import ServicesShowcase from "./components/ServicesShowcase"
import BeforeAfter from "./components/BeforeAfter"
import Process from "./components/Process"
import Contact from "./components/Contact"
import Footer from "./components/Footer"

function App() {
  return (
    <div className="bg-carbon text-white">
      <Nav />
      <main>
        <Hero />
        <Manifesto />
        <ServicesShowcase />
        <BeforeAfter />
        <Process />
        <Contact />
      </main>
      <Footer />
    </div>
  )
}

export default App

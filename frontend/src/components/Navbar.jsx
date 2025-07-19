// src/components/Navbar.jsx
const Navbar = () => {
  return (
    <nav className="bg-primary text-white px-6 py-4 flex justify-between items-center shadow-md">
      <h1 className="text-2xl font-title">FitMentor</h1>
      <ul className="flex space-x-6 font-sans">
        <li><a href="#home" className="hover:text-accent">Inícioteste</a></li>
        <li><a href="#services" className="hover:text-accent">Serviços</a></li>
        <li><a href="#contact" className="hover:text-accent">Contato</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;

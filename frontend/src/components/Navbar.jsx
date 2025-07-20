// src/components/Navbar.jsx
const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center shadow-md">
      <h1 className="text-2xl font-bold">Consultoria online</h1>
      <ul className="flex space-x-6 font-sans">
        <li><a href="/" className="hover:text-yellow-300">Início</a></li>
        <li><a href="services" className="hover:text-yellow-300">Serviços</a></li>
        <li><a href="contact" className="hover:text-yellow-300">Contato</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;

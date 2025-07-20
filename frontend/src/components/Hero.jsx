// src/components/Hero.jsx
const Hero = () => {
  return (
    <section className="bg-gray-100 text-blue-800 py-20 px-6 text-center">
      <h2 className="text-4xl font-bold mb-4">Seu treino, sua jornada.</h2>
      <p className="text-lg max-w-xl mx-auto mb-8 font-sans">
        Consultoria personalizada para transformar sua saúde e conquistar seus objetivos com flexibilidade e acompanhamento profissional.
      </p>

      {/* Container com flex e gap */}
      <div className="flex justify-center gap-4">
        <a
          href="login"
          className="bg-blue-400 text-white px-6 py-3 rounded-full font-semibold shadow-md hover:bg-blue-300 transition"
        >
          Fazer Login
        </a>
        <a
          href="register"
          className="bg-yellow-400 text-white px-6 py-3 rounded-full font-semibold shadow-md hover:bg-yellow-300 transition"
        >
          Registrar-se
        </a>
      </div>
    </section>
  );
};

export default Hero;

// src/components/Hero.jsx
const Hero = () => {
  return (
    <section className="bg-light text-primary py-20 px-6 text-center">
      <h2 className="text-4xl font-title mb-4">Seu treino, sua jornada.</h2>
      <p className="text-lg max-w-xl mx-auto mb-8 font-sans">
        Consultoria personalizada para transformar sua saúde e conquistar seus objetivos com flexibilidade e acompanhamento profissional.
      </p>
      <a
        href="#contact"
        className="bg-accent text-white px-6 py-3 rounded-full font-semibold shadow-md hover:bg-opacity-90 transition"
      >
        Comece Agora
      </a>
    </section>
  );
};

export default Hero;

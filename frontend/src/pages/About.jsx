import "./About.css";

function About() {
  return (
    <main className="about-page">

      <section className="about-header">

        <h1>
          About TripWise
        </h1>

        <p>
          Plan Less. Explore More.
        </p>

      </section>


      <section className="about-content">

        <h2>
          Travel planning, made simpler.
        </h2>

        <p>
          TripWise is designed to help travelers
          create personalised trips without
          spending hours researching destinations,
          budgets and activities.
        </p>

        <p>
          Tell us where you want to go, when you
          want to travel, your budget and what
          interests you. TripWise brings everything
          together into a simple travel plan.
        </p>


        <h2>
          Our Goal
        </h2>

        <p>
          We want travelers to spend less time
          planning and more time experiencing
          the places they visit.
        </p>


        <div className="about-slogan">
          Plan Less. Explore More.
        </div>

      </section>

    </main>
  );
}

export default About;
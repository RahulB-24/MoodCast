import React from "react";
import { Particles } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";

export default function ParticleBackground() {
  const particlesInit = async (engine) => {
    await loadSlim(engine);
  };

  return (
    <Particles
      id="tsparticles"
      init={particlesInit}
      options={{
        fullScreen: {
          enable: true,
          zIndex: -1
        },
        particles: {
          number: {
            value: 40,
            density: {
              enable: true,
              area: 800
            }
          },
          color: { value: "#ffffff" },
          opacity: { value: 0.25 },
          size: { value: 2 },
          move: {
            enable: true,
            speed: 0.4,
            random: true,
            direction: "none",
            outModes: { default: "out" }
          }
        }
      }}
    />
  );
}

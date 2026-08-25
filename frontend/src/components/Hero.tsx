import React, { useState } from 'react';

interface HeroProps {
  onNavigateLogin: () => void;
  onPlanTrip: (prompt: string) => void;
}

export const Hero: React.FC<HeroProps> = ({ onNavigateLogin, onPlanTrip }) => {
  const [promptText, setPromptText] = useState(
    "Plan a 7-day trip to Tokyo from Hyderabad with a moderate budget starting March 24, 2026."
  );

  return (
    <section className="relative min-h-svh w-full overflow-hidden">
      {/* Background Video */}
      <video
        className="absolute inset-0 w-full h-full object-cover z-0"
        src="https://pollen-batch-41236914.figma.site/_components/v2/f0ee2dae7671c170c34f12e31c4cb41418976c98/769c564298c132f7919405cd9f17c1b1231f341d.769c5642.mp4"
        autoPlay
        muted
        loop
        playsInline
      />

      {/* Top Gradient Overlay */}
      <div
        className="absolute inset-x-0 top-0 h-[687px] pointer-events-none z-[1]"
        style={{
          background: 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 100%)',
        }}
      />

      {/* Content Wrapper */}
      <div className="relative z-[2] max-w-[1360px] mx-auto">
        {/* Navigation Bar */}
        <nav className="flex items-center justify-between px-20 pt-6 pb-4 max-md:px-6 max-md:pt-5">
          {/* Left wordmark */}
          <span 
            onClick={onNavigateLogin}
            className="font-typewriter text-[32px] max-md:text-[28px] font-bold text-black leading-none select-none cursor-pointer"
          >
            wandor
          </span>
        </nav>

        {/* Hero Body */}
        <div className="flex flex-col items-center px-6 pt-16 pb-24 text-center">
          <h1 className="font-sans text-[clamp(40px,6vw,68px)] font-medium text-wandor-text leading-[1.05] tracking-[-0.04em] max-w-[820px] mb-5">
            Where will you go next?
          </h1>
          <p className="font-sans text-xl font-medium text-wandor-muted leading-relaxed max-w-[500px] mb-10">
            Tell our AI where you're going and what you love. We'll create a personalized itinerary for you.
          </p>

          {/* Liquid Glass Prompt Card */}
          <div className="relative w-[701px] max-md:w-[calc(100vw-48px)] min-h-[208px] bg-white/[0.06] border-[3px] border-white rounded-[44px] shadow-[0_0_4px_0_rgba(0,0,0,0.15)] overflow-hidden backdrop-blur-[20px]">
            <textarea
              value={promptText}
              onChange={(e) => setPromptText(e.target.value)}
              className="absolute left-[29px] top-[24px] w-[640px] max-md:w-[calc(100%-58px)] h-[90px] bg-transparent border-none outline-none font-sans text-xl max-md:text-[17px] font-medium text-wandor-prompt text-left leading-relaxed resize-none overflow-y-auto focus:ring-0 focus:outline-none"
              placeholder="Describe your dream trip..."
            />

            {/* Plan My Trip Button inside card */}
            <button 
              onClick={() => onPlanTrip(promptText)}
              className="absolute bottom-[21px] right-[21px] w-[156px] h-14 bg-black border-none rounded-[44px] shadow-[0_0_2px_0_rgba(0,0,0,0.05)] cursor-pointer flex items-center justify-center font-sans text-base font-medium text-[#fafafa] uppercase tracking-[0.02em] transition-all hover:bg-[#333] active:scale-95"
            >
              Plan My Trip
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

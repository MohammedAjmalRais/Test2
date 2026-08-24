import React, { useState } from 'react';

interface LoginProps {
  onNavigateHome: () => void;
}

export const Login: React.FC<LoginProps> = ({ onNavigateHome }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  // Validation / Error States
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<{ email?: string; password?: string }>({});
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleLoginSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);
    setFieldErrors({});

    let hasErrors = false;
    const newErrors: { email?: string; password?: string } = {};

    // Basic email validation
    if (!email) {
      newErrors.email = 'Email address is required.';
      hasErrors = true;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Please enter a valid email address.';
      hasErrors = true;
    }

    // Basic password validation
    if (!password) {
      newErrors.password = 'Password is required.';
      hasErrors = true;
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters.';
      hasErrors = true;
    }

    if (hasErrors) {
      setFieldErrors(newErrors);
      setErrorMsg('Please resolve the errors below to continue.');
      return;
    }

    // Simulate API request
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      if (email === 'demo@wandor.ai' && password === 'password123') {
        setSuccessMsg('Successfully signed in! Redirecting to your dashboard...');
        setTimeout(() => {
          onNavigateHome();
        }, 1500);
      } else {
        setErrorMsg('Invalid email or password. Use demo@wandor.ai and password123 to login.');
      }
    }, 1800);
  };

  return (
    <div className="paper-texture min-h-svh w-full relative overflow-hidden flex flex-col z-0 select-text font-body text-[#111111]">
      {/* Organic Watercolor Background Patches */}
      <div className="absolute top-[8%] left-[6%] w-[480px] h-[480px] rounded-full bg-[#E8DDC7]/25 blur-[110px] pointer-events-none -z-10" />
      <div className="absolute bottom-[12%] right-[8%] w-[520px] h-[520px] rounded-full bg-[#D9CBB2]/20 blur-[130px] pointer-events-none -z-10" />
      <div className="absolute top-[40%] left-[30%] w-[380px] h-[380px] rounded-full bg-[#C9B99D]/15 blur-[100px] pointer-events-none -z-10" />



      {/* TOP NAVIGATION */}
      <nav className="relative z-10 flex items-center justify-between px-20 pt-6 pb-4 max-md:px-6 max-md:pt-5 w-full">
        {/* Left wordmark */}
        <span 
          onClick={onNavigateHome} 
          className="font-typewriter text-[32px] max-md:text-[28px] font-bold text-[#111111] leading-none select-none cursor-pointer tracking-tight"
        >
          wandor
        </span>
      </nav>

      {/* MAIN CONTAINER */}
      <main className="flex-grow flex items-center justify-center px-20 py-8 max-md:px-6 max-md:py-6 max-w-[1450px] w-full mx-auto relative z-10">
        <div className="grid grid-cols-12 gap-12 max-lg:gap-6 items-center w-full">
          
          {/* LEFT COLUMN: VINTAGE TRAVEL PANORAMA (Cropped from mockup) */}
          <div className="col-span-7 max-md:col-span-12 relative rounded-[28px] overflow-hidden h-[640px] max-md:h-[280px] shadow-[0_8px_30px_rgba(40,32,20,0.04)] border border-[#DED7CA]">
            <img
              src="/illustration.jpg"
              alt="Travel destinations landscape"
              className="w-full h-full object-cover select-none pointer-events-none"
            />
          </div>

          {/* RIGHT COLUMN: PREMIUM FORM CARD */}
          <div className="col-span-5 max-md:col-span-12 flex items-center justify-center">
            <div className="bg-[#FBF8F1] border border-[#DED7CA] rounded-[28px] w-full shadow-[0_12px_40px_rgba(45,35,25,0.06)] flex flex-col relative overflow-hidden">
              
              {/* Main Card Content */}
              <div className="p-11 max-md:p-6 flex flex-col gap-6">
                {/* Card Header Info */}
                <div className="flex justify-between items-center select-none">
                  <span className="text-[#A85D3B] text-[20px] font-bold">✦</span>
                  <div className="text-[11px] font-semibold text-[#8A847A] tracking-wider uppercase">
                    SECURE ACCESS
                  </div>
                </div>

                {/* Login Heading */}
                <div>
                  <h1 className="font-display text-[44px] max-md:text-[34px] font-semibold text-[#111111] leading-tight">
                    Welcome.
                  </h1>
                  <p className="text-[15px] font-medium text-[#6F6A62] mt-2 leading-relaxed">
                    Continue planning your next adventure.
                  </p>
                </div>

                {/* Error Box (Subtle Cream Notification Box) */}
                {errorMsg && (
                  <div className="bg-[#F3E3DA] border border-[#D7B7A7] text-[#6F3E32] rounded-xl px-4 py-3.5 text-xs flex gap-2.5 items-start">
                    <span className="text-sm leading-none mt-0.5">⚠️</span>
                    <div>
                      <p className="font-semibold">Unable to sign in</p>
                      <p className="opacity-90 mt-0.5">{errorMsg}</p>
                    </div>
                  </div>
                )}

                {/* Success Box */}
                {successMsg && (
                  <div className="bg-[#E7ECE4] border border-[#C6D2C0] text-[#3D4F3A] rounded-xl px-4 py-3.5 text-xs flex gap-2.5 items-start">
                    <span className="text-sm leading-none mt-0.5">✓</span>
                    <div>
                      <p className="font-semibold">Success</p>
                      <p className="opacity-90 mt-0.5">{successMsg}</p>
                    </div>
                  </div>
                )}

                {/* Form Fields */}
                <form onSubmit={handleLoginSubmit} className="flex flex-col gap-4">
                  
                  {/* Email Address */}
                  <div className="flex flex-col gap-1.5">
                    <div className="flex justify-between items-center">
                      <label className="text-[13px] font-semibold text-[#111111]">
                        Email address
                      </label>
                      {fieldErrors.email && (
                        <span className="text-[11px] font-medium text-[#A84F3B]">
                          {fieldErrors.email}
                        </span>
                      )}
                    </div>
                    <input
                      type="email"
                      placeholder="Enter your email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      disabled={isLoading}
                      className={`w-full h-[52px] bg-[#F7F3EA] border rounded-xl px-4 text-sm outline-none transition-all placeholder:text-[#A6A096] ${
                        fieldErrors.email ? 'border-[#A84F3B]' : 'border-[#D8D1C5] focus:border-[#111111]'
                      }`}
                    />
                  </div>

                  {/* Password */}
                  <div className="flex flex-col gap-1.5">
                    <div className="flex justify-between items-center">
                      <label className="text-[13px] font-semibold text-[#111111]">
                        Password
                      </label>
                      {fieldErrors.password && (
                        <span className="text-[11px] font-medium text-[#A84F3B]">
                          {fieldErrors.password}
                        </span>
                      )}
                    </div>
                    <div className="relative w-full">
                      <input
                        type={showPassword ? 'text' : 'password'}
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        disabled={isLoading}
                        className={`w-full h-[52px] bg-[#F7F3EA] border rounded-xl pl-4 pr-10 text-sm outline-none transition-all placeholder:text-[#A6A096] ${
                          fieldErrors.password ? 'border-[#A84F3B]' : 'border-[#D8D1C5] focus:border-[#111111]'
                        }`}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-xs font-semibold text-[#77716A] hover:text-[#111111] transition-colors cursor-pointer select-none"
                      >
                        {showPassword ? 'Hide' : 'Show'}
                      </button>
                    </div>
                  </div>

                  {/* Remember / Forgot password */}
                  <div className="flex items-center justify-between text-[12px] font-semibold select-none pt-1">
                    <label className="flex items-center gap-2 cursor-pointer text-[#6F6A62] hover:text-[#111111] transition-colors">
                      <input
                        type="checkbox"
                        checked={rememberMe}
                        onChange={(e) => setRememberMe(e.target.checked)}
                        disabled={isLoading}
                        className="w-4 h-4 rounded border-[#D8D1C5] text-[#111111] focus:ring-0 focus:ring-offset-0 cursor-pointer accent-[#111111]"
                      />
                      Remember me
                    </label>
                    <a
                      href="#forgot"
                      onClick={(e) => {
                        e.preventDefault();
                        alert('A recovery code link has been sent to your email.');
                      }}
                      className="text-[#111111] hover:underline"
                    >
                      Forgot password?
                    </a>
                  </div>

                  {/* Primary login button */}
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full h-[52px] bg-[#111111] hover:bg-[#2A2926] disabled:bg-[#4a4944] text-[#F7F3EA] text-sm font-semibold rounded-full mt-2 transition-all duration-200 ease-out active:scale-95 flex items-center justify-center gap-2 cursor-pointer shadow-sm"
                  >
                    {isLoading ? (
                      <>
                        <svg className="animate-spin h-4 w-4 text-[#F7F3EA]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Signing in...
                      </>
                    ) : (
                      'Continue your journey'
                    )}
                  </button>
                </form>

                {/* Divider */}
                <div className="flex items-center gap-3 select-none">
                  <div className="flex-grow h-[1px] bg-[#DDD6CA]" />
                  <span className="text-[11px] text-[#77716A] font-semibold uppercase tracking-wider">
                    or continue with
                  </span>
                  <div className="flex-grow h-[1px] bg-[#DDD6CA]" />
                </div>

                {/* Social Login Buttons */}
                <div className="flex flex-col gap-2.5">
                  {/* Google */}
                  <button
                    onClick={() => {
                      setIsLoading(true);
                      setTimeout(() => {
                        setIsLoading(false);
                        setSuccessMsg('Successfully connected via Google!');
                        setTimeout(() => onNavigateHome(), 1200);
                      }, 1200);
                    }}
                    disabled={isLoading}
                    className="w-full h-[50px] bg-[#FBF8F1] border border-[#D8D1C5] hover:bg-[#F2EDE4] active:scale-98 rounded-xl flex items-center justify-center text-sm font-semibold text-[#111111] transition-all cursor-pointer"
                  >
                    <svg className="w-5 h-5 mr-3 flex-shrink-0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22c-.87-2.6-2.86-4.53-5.71-4.53z" fill="#FBBC05" />
                      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335" />
                    </svg>
                    Continue with Google
                  </button>

                  {/* Apple */}
                  <button
                    onClick={() => {
                      setIsLoading(true);
                      setTimeout(() => {
                        setIsLoading(false);
                        setSuccessMsg('Successfully connected via Apple ID!');
                        setTimeout(() => onNavigateHome(), 1200);
                      }, 1200);
                    }}
                    disabled={isLoading}
                    className="w-full h-[50px] bg-[#FBF8F1] border border-[#D8D1C5] hover:bg-[#F2EDE4] active:scale-98 rounded-xl flex items-center justify-center text-sm font-semibold text-[#111111] transition-all cursor-pointer"
                  >
                    <svg className="w-5 h-5 mr-3 flex-shrink-0 fill-[#111111]" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 4.17c.66-.81 1.11-1.93.99-3.06-1 .04-2.22.67-2.94 1.49-.63.73-1.18 1.87-1.03 2.97 1.12.09 2.27-.58 2.98-1.4" />
                  </svg>
                  Continue with Apple
                </button>
              </div>

              {/* Sign up Link */}
              <div className="text-center text-xs font-semibold text-[#6F6A62] select-none mt-2">
                New to Wandor?{' '}
                <a
                  href="#signup"
                  onClick={(e) => {
                    e.preventDefault();
                    alert('Registration form overlay mock triggered.');
                  }}
                  className="text-[#111111] hover:underline font-bold"
                >
                  Create an account
                </a>
              </div>
            </div>

            {/* Premium Card Footer with Separate Background and Top Border */}
            <div className="bg-[#F5EFE6] border-t border-[#DED7CA] py-4.5 px-10 flex items-center justify-center gap-2 text-[11px] text-[#8A847A] font-semibold select-none">
              Your travel plans stay private and secure.
            </div>

            </div>
          </div>

        </div>
      </main>
    </div>
  );
};

export default Login;

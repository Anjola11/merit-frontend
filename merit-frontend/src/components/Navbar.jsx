import { useState } from "react";
import { MdArrowDropDown } from "react-icons/md";
import { motion } from "framer-motion";


const Navbar = () => {
  const [isDropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setDropdownOpen(!isDropdownOpen);
  };

  return (
    <header className="bg-violet-700 text-white shadow-lg ">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <div className="text-xl font-bold">
            <a href="/">Merit.com</a>{''}
          </div>

          {/* Nav Links */}
          <nav className="hidden md:flex space-x-8 items-center">
            <a href="/" className="text-white hover:text-gray-900">
              Home
            </a>
            <a href="http://127.0.0.1:5000/merit.ai" className="text-white hover:text-gray-900">
              Merit AI
            </a>

            {/* Service Dropdown */}
            <div className="relative">
              <button
                onClick={toggleDropdown}
                className="flex items-center text-white hover:text-gray-900 focus:outline-none"
              >
                Service <MdArrowDropDown color="#ffffff" className="ml-1 " />
              </button>

              {/* Dropdown Menu */}
              {isDropdownOpen && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="absolute mt-2 w-48 bg-white shadow-lg rounded-md z-10 overflow-hidden"
                >
                  <a
                    href="/service/aggregate-calculator"
                    className="block px-4 py-3 text-base text-gray-700 hover:bg-gray-100"
                  >
                    Aggregate calculator
                  </a>

                  <a
                    href="/universities-list"
                    className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                  >
                    Find dream school
                  </a>
                </motion.div>
              )}
            </div>

            <a href="/about" className="text-white hover:text-gray-900">
              About
            </a>
          </nav>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={toggleDropdown}
              className="text-gray-700 focus:outline-none"
            >
              <MdArrowDropDown size={28} color="#ffffff" />
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isDropdownOpen && (
          <div className="md:hidden">
            <a
              href="/"
              className="block py-2 px-4 text-white hover:bg-gray-100"
            >
              Home
            </a>
            <div className="block py-2 px-4  text-white hover:bg-gray-100">
              <span>Service</span>
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mt-2 space-y-2"
              >
                <a
                  href="/service/aggregate-calculator"
                  className="block  hover:bg-gray-100"
                >
                  Aggregate calculator
                </a>

                <a
                  href="/universities-list"
                  className="block  hover:bg-gray-100"
                >
                  Find dream school
                </a>
              </motion.div>
            </div>
            <a
              href="/about"
              className="block py-2 px-4 text-white hover:bg-gray-100"
            >
              About
            </a>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;

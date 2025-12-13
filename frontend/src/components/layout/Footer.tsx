import React from 'react';
import { Link } from 'react-router-dom';
import { Facebook, Twitter, Mail, Phone, ExternalLink } from 'lucide-react';

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  // Government links
  const govtLinks = [
    { name: 'Home', url: '/' },
    { name: 'About Us', url: '/about' },
    { name: 'Help', url: '/help' },
    { name: 'Terms & Conditions', url: '/terms' },
    { name: 'Privacy Policy', url: '/privacy' },
    { name: 'Disclaimer', url: '/disclaimer' },
    { name: 'Contact Us', url: '/contact' },
    { name: 'Sitemap', url: '/sitemap' },
  ];

  // Important links
  const importantLinks = [
    { name: 'Digital India', url: 'https://digitalindia.gov.in/', external: true },
    { name: 'MyGov', url: 'https://www.mygov.in/', external: true },
    { name: 'National Portal of India', url: 'https://www.india.gov.in/', external: true },
    { name: 'Make in India', url: 'https://www.makeinindia.com/', external: true },
  ];

  return (
    <footer className="bg-[#0a4b78] text-white">
      {/* Main Footer Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Quick Links */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-semibold mb-4 border-b border-white/20 pb-2">Quick Links</h3>
            <ul className="space-y-2">
              {govtLinks.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.url} 
                    className="text-sm text-white/80 hover:text-white flex items-center"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 border-b border-white/20 pb-2">Important Links</h3>
            <ul className="space-y-2">
              {importantLinks.map((link) => (
                <li key={link.name}>
                  <a 
                    href={link.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-sm text-white/80 hover:text-white flex items-center"
                  >
                    {link.name}
                    {link.external && <ExternalLink className="ml-1 h-3 w-3" />}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 border-b border-white/20 pb-2">Contact Us</h3>
            <div className="space-y-3">
              <div className="flex items-start">
                <Mail className="h-5 w-5 mt-0.5 mr-2 flex-shrink-0" />
                <a href="mailto:cybersop@gov.in" className="text-sm text-white/80 hover:text-white">cybersop[at]gov.in</a>
              </div>
              <div className="flex items-start">
                <Phone className="h-5 w-5 mt-0.5 mr-2 flex-shrink-0" />
                <span className="text-sm">Toll Free: 1800-123-4567</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 border-b border-white/20 pb-2">Follow Us</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-white hover:text-blue-300">
                <Facebook className="h-6 w-6" />
              </a>
              <a href="#" className="text-white hover:text-blue-400">
                <Twitter className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-white/20 text-center text-sm text-white/80">
          <p>© {currentYear} Cyber SOP Assistant. All Rights Reserved.</p>
          <p className="mt-1">This website belongs to Ministry of Electronics & Information Technology, Government of India.</p>
          
          <div className="flex flex-wrap justify-center gap-4 mt-4">
            <a href="#" className="hover:underline">Accessibility Statement</a>
            <span>|</span>
            <a href="#" className="hover:underline">Copyright Policy</a>
            <span>|</span>
            <a href="#" className="hover:underline">Hyperlinking Policy</a>
          </div>
        </div>
      </div>

      {/* National Portal of India Footer */}
      <div className="bg-[#0a4b78] border-t border-white/10 py-3">
        <div className="container mx-auto px-4 text-center text-xs text-white/60">
          <p>This website follows the <a href="https://www.goidirectory.gov.in/" target="_blank" rel="noopener noreferrer" className="text-blue-200 hover:underline">Government of India Web Guidelines and Policies</a></p>
          <p className="mt-1">Designed & Developed by <a href="https://www.meity.gov.in/" target="_blank" rel="noopener noreferrer" className="text-blue-200 hover:underline">Ministry of Electronics & Information Technology</a></p>
        </div>
      </div>
    </footer>
  );
};

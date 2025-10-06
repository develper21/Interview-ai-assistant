'use client';
import React, { useState } from 'react';
import { User, AtSign, Key, Save } from 'lucide-react';

const ProfilePage = () => {
  const [userName, setUserName] = useState('Rajesh Kumar');
  const [apiKey, setApiKey] = useState('');

  const handleSaveChanges = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Save changes to Supabase
    console.log('Saving changes:', { userName, apiKey });
    alert('Changes saved successfully! (Demo)');
  };

  return (
    <div className="space-y-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold">Profile & Settings</h1>

      <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700">
        <form onSubmit={handleSaveChanges} className="space-y-6">
          {/* User Name */}
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">Full Name</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg outline-none"
              />
            </div>
          </div>
          
          {/* Email Address */}
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">Email Address</label>
            <div className="relative">
              <AtSign className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="email"
                value="rajesh.k@example.com"
                readOnly
                className="w-full pl-10 pr-4 py-3 bg-gray-900 border border-gray-700 rounded-lg outline-none cursor-not-allowed"
              />
            </div>
          </div>

          {/* Gemini API Key */}
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">Gemini API Key</label>
            <div className="relative">
              <Key className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="password"
                placeholder="Apni Gemini API key yahan paste karein"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg outline-none"
              />
            </div>
            <p className="text-xs text-gray-500 mt-2">Aapki key hamare database mein securely save ki jayegi.</p>
          </div>

          {/* Save Button */}
          <button
            type="submit"
            className="w-full flex items-center justify-center gap-2 py-3 px-4 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-all duration-300"
          >
            <Save size={20} />
            Save Changes
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfilePage;

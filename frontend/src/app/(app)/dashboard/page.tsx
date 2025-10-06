import React from 'react';
import Link from 'next/link';
import { Plus, Clock } from 'lucide-react';

const DashboardPage = () => {
  // Mock data for past sessions
  const pastSessions = [
    { id: 1, role: 'Frontend Developer', date: 'Oct 04, 2025', duration: '30 min' },
    { id: 2, role: 'Product Manager', date: 'Sep 28, 2025', duration: '45 min' },
    { id: 3, role: 'Data Scientist', date: 'Sep 15, 2025', duration: '60 min' },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <p className="mt-2 text-gray-400">Welcome back! Apne agle interview ke liye taiyar ho jao.</p>
      </div>

      {/* Start New Session Card */}
      <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700">
        <h2 className="text-2xl font-semibold">Start a New Session</h2>
        <p className="mt-2 text-gray-400">Naya interview session shuru karne ke liye click karein.</p>
        <Link href="/session">
          <button className="mt-6 inline-flex items-center gap-2 px-6 py-3 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-all duration-300 transform hover:scale-105">
            <Plus size={20} />
            Start New Interview
          </button>
        </Link>
      </div>

      {/* Past Sessions */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">Past Sessions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {pastSessions.map((session) => (
            <div key={session.id} className="bg-gray-800 p-6 rounded-2xl border border-gray-700 hover:border-indigo-500 transition-colors duration-300">
              <h3 className="font-bold text-lg">{session.role}</h3>
              <p className="text-sm text-gray-400 mt-1">{session.date}</p>
              <div className="flex items-center gap-2 mt-4 text-gray-300">
                <Clock size={16} />
                <span>{session.duration}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

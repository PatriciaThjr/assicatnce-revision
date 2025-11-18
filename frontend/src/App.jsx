import React from 'react';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-800">Assistance de Révision</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Section Matières */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Matières</h2>
            <div className="space-y-2">
              <button className="w-full text-left p-3 bg-blue-50 rounded hover:bg-blue-100">
                Mathématiques
              </button>
              <button className="w-full text-left p-3 bg-green-50 rounded hover:bg-green-100">
                Physique-Chimie
              </button>
              <button className="w-full text-left p-3 bg-purple-50 rounded hover:bg-purple-100">
                Français
              </button>
            </div>
          </div>

          {/* Section Quiz */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Quiz Rapide</h2>
            <div className="bg-yellow-50 p-4 rounded-lg">
              <p className="font-medium">Quelle est la capitale de la France ?</p>
              <div className="mt-3 space-y-2">
                <button className="w-full p-2 bg-white border rounded hover:bg-gray-50">Londres</button>
                <button className="w-full p-2 bg-white border rounded hover:bg-gray-50">Berlin</button>
                <button className="w-full p-2 bg-white border rounded hover:bg-gray-50">Paris</button>
              </div>
            </div>
          </div>

          {/* Section Progression */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Ma Progression</h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-1">
                  <span>Mathématiques</span>
                  <span>65%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full w-2/3"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between mb-1">
                  <span>Français</span>
                  <span>40%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-green-600 h-2 rounded-full w-2/5"></div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;
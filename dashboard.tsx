import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, PieChart, Pie, LineChart, Line, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  ResponsiveContainer, Cell, AreaChart, Area
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

const Dashboard = () => {
  const [deviceData, setDeviceData] = useState([]);
  const [regionData, setRegionData] = useState([]);
  const [browserData, setBrowserData] = useState([]);
  const [eventTypeData, setEventTypeData] = useState([]);
  const [bounceRateData, setBounceRateData] = useState({});
  const [sessionDuration, setSessionDuration] = useState({});
  const [devicePerformance, setDevicePerformance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetching data simulation
  useEffect(() => {
    // In a real application, this would be an API call
    // For demonstration, we'll use hardcoded data from our SQL queries
    
    setDeviceData([
      { name: 'Desktop', value: 39139 },
      { name: 'Mobile', value: 38968 },
      { name: 'Tablet', value: 39014 }
    ]);
    
    setRegionData([
      { name: 'Europe', value: 6638 },
      { name: 'North America', value: 6750 },
      { name: 'Asia', value: 6700 },
      { name: 'Africa', value: 6650 }
    ]);
    
    setBrowserData([
      { name: 'Chrome', value: 929.65, sessions: 10765 },
      { name: 'Safari', value: 934.22, sessions: 10768 },
      { name: 'Firefox', value: 927.31, sessions: 10789 },
      { name: 'Edge', value: 926.97, sessions: 10781 }
    ]);
    
    setEventTypeData([
      { name: 'form_submit', value: 19631, percentage: 16.76 },
      { name: 'click', value: 19585, percentage: 16.72 },
      { name: 'page_view', value: 19547, percentage: 16.69 },
      { name: 'keydown', value: 19503, percentage: 16.65 },
      { name: 'hover', value: 19494, percentage: 16.64 }
    ]);
    
    setBounceRateData({
      singlePageSessions: 3693,
      totalSessions: 9531,
      bounceRate: 38.75
    });
    
    setSessionDuration({
      average: 929.53,
      median: 930
    });
    
    setDevicePerformance([
      { name: 'Desktop', duration: 933.61, users: 6822, sessions: 11317 },
      { name: 'Mobile', duration: 928.15, users: 6822, sessions: 11335 },
      { name: 'Tablet', duration: 926.82, users: 6860, sessions: 11324 }
    ]);
    
    setLoading(false);
  }, []);

  if (loading) return <div className="flex justify-center items-center h-64">Loading dashboard data...</div>;
  if (error) return <div className="text-red-500">Error loading data: {error}</div>;

  return (
    <div className="p-4 bg-gray-50">
      <h1 className="text-2xl font-bold mb-6 text-center">Events Database Analytics Dashboard</h1>
      
      {/* Key Metrics Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Total Sessions</h2>
          <p className="text-3xl font-bold text-blue-600">{bounceRateData.totalSessions.toLocaleString()}</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Bounce Rate</h2>
          <p className="text-3xl font-bold text-orange-500">{bounceRateData.bounceRate.toFixed(1)}%</p>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">Avg Session Duration</h2>
          <p className="text-3xl font-bold text-green-600">{Math.floor(sessionDuration.average / 60)}m {Math.round(sessionDuration.average % 60)}s</p>
        </div>
      </div>
      
      {/* Device Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">Traffic by Device Type</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={deviceData}
                  cx="50%"
                  cy="50%"
                  labelLine={true}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({name, percent}) => `${name}: ${(percent * 100).toFixed(1)}%`}
                >
                  {deviceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`${value.toLocaleString()} events`, 'Count']} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">User Distribution by Region</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value) => [`${value.toLocaleString()} users`, 'Unique Users']} />
                <Legend />
                <Bar dataKey="value" name="Unique Users" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      {/* Event Types */}
      <div className="bg-white p-4 rounded shadow mb-8">
        <h2 className="text-lg font-semibold mb-4">Event Type Distribution</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={eventTypeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [value.toLocaleString(), name]} 
                labelFormatter={(label) => `Event: ${label}`}
              />
              <Legend />
              <Bar dataKey="value" name="Event Count" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Browser Performance */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">Session Duration by Browser</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={browserData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[900, 950]} />
                <Tooltip 
                  formatter={(value) => [`${value.toFixed(1)} seconds`, 'Avg. Duration']} 
                />
                <Legend />
                <Bar dataKey="value" name="Avg Session Duration" fill="#0088FE" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">Device Performance Comparison</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={devicePerformance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[900, 950]} />
                <Tooltip 
                  formatter={(value) => [`${value.toFixed(1)} seconds`, 'Avg. Duration']} 
                />
                <Legend />
                <Bar dataKey="duration" name="Avg Session Duration" fill="#FF8042" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      
      {/* Bounce Rate Visualization */}
      <div className="bg-white p-4 rounded shadow mb-8">
        <h2 className="text-lg font-semibold mb-4">Bounce Rate Analysis</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={[
                  { name: 'Bounced Sessions', value: bounceRateData.singlePageSessions },
                  { name: 'Engaged Sessions', value: bounceRateData.totalSessions - bounceRateData.singlePageSessions }
                ]}
                cx="50%"
                cy="50%"
                labelLine={true}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label={({name, percent}) => `${name}: ${(percent * 100).toFixed(1)}%`}
              >
                <Cell fill="#FF8042" />
                <Cell fill="#00C49F" />
              </Pie>
              <Tooltip formatter={(value) => [`${value.toLocaleString()} sessions`, 'Count']} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Insights Section */}
      <div className="bg-white p-6 rounded shadow">
        <h2 className="text-xl font-bold mb-4">Key Insights & Recommendations</h2>
        
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-red-600">Critical Issues</h3>
          <ul className="list-disc pl-5 mt-2">
            <li className="mb-2"><span className="font-medium">High Bounce Rate (38.7%)</span>: Nearly 4 out of 10 users leave after viewing just one page.</li>
            <li className="mb-2"><span className="font-medium">Device Performance Gaps</span>: Tablet and mobile users have lower session durations compared to desktop users.</li>
          </ul>
        </div>
        
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-green-600">Recommendations</h3>
          <ul className="list-disc pl-5 mt-2">
            <li className="mb-2"><span className="font-medium">Optimize First-Page Experience</span>: Enhance landing page clarity and value proposition.</li>
            <li className="mb-2"><span className="font-medium">Improve Mobile & Tablet Experience</span>: Prioritize mobile/tablet optimization.</li>
            <li className="mb-2"><span className="font-medium">Streamline Conversion Paths</span>: Focus on creating more direct paths to conversion.</li>
            <li className="mb-2"><span className="font-medium">Enhance User Engagement</span>: Implement personalized content recommendations based on user behavior.</li>
            <li className="mb-2"><span className="font-medium">Implement Retention Strategies</span>: Create re-engagement campaigns for users who haven't returned.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
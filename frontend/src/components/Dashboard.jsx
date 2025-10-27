import React, { useState, useEffect } from 'react';
import { ArrowLeft, Calendar, Users, Briefcase, Wallet, Clock, CheckCircle, RefreshCw, AlertCircle } from 'lucide-react';
import { apiService } from '../services/api';
import MetricCard from './MetricCard';
import TrendChart from './TrendChart';

export default function Dashboard({ district, onBack }) {
  const [snapshot, setSnapshot] = useState(null);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMetric, setSelectedMetric] = useState('people_benefited');

  useEffect(() => {
    loadData();
  }, [district]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [snapshotData, trendData] = await Promise.all([
        apiService.getDistrictSnapshot(district.district_code),
        apiService.getDistrictTrend(district.district_code, 6),
      ]);
      setSnapshot(snapshotData);
      setTrends(trendData.trends);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
          <p className="text-red-800 font-semibold mb-4">{error}</p>
          <button
            onClick={loadData}
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!snapshot) return null;

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={onBack}
            className="flex items-center space-x-2 text-gray-600 hover:text-blue-600 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Change District</span>
          </button>
          <div className="flex items-center space-x-2 text-gray-600">
            <Calendar className="w-5 h-5" />
            <span className="text-sm">
              {monthNames[snapshot.current.month - 1]} {snapshot.current.year}
            </span>
          </div>
        </div>
        <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
          {snapshot.district.district_name}
        </h1>
        <p className="text-gray-600">{snapshot.district.state}</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <MetricCard
          title="People Benefited"
          value={snapshot.current.people_benefited}
          icon={Users}
          color="blue"
          change={snapshot.comparison?.people_benefited}
          metricKey="people_benefited"
          comparison={snapshot.comparison}
        />
        <MetricCard
          title="Workdays Created"
          value={snapshot.current.workdays_created}
          icon={Briefcase}
          color="green"
          change={snapshot.comparison?.workdays_created}
          metricKey="workdays_created"
          comparison={snapshot.comparison}
        />
        <MetricCard
          title="Wages Paid"
          value={parseInt(snapshot.current.wages_paid)}
          unit="₹"
          icon={Wallet}
          color="orange"
          change={snapshot.comparison?.wages_paid}
          metricKey="wages_paid"
          comparison={snapshot.comparison}
        />
        <MetricCard
          title="On-Time Payments"
          value={parseFloat(snapshot.current.payments_on_time_percent)}
          unit="%"
          icon={Clock}
          color="purple"
          change={snapshot.comparison?.payments_on_time_percent}
          metricKey="payments_on_time_percent"
          comparison={snapshot.comparison}
        />
        <MetricCard
          title="Works Completed"
          value={snapshot.current.works_completed}
          icon={CheckCircle}
          color="pink"
          change={snapshot.comparison?.works_completed}
          metricKey="works_completed"
          comparison={snapshot.comparison}
        />
      </div>

      {/* Metric Selector for Chart */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Select Metric for Trend Chart</h2>
        <div className="grid grid-cols-4 gap-4">
          {[
            { key: 'people_benefited', label: 'People Benefited', color: 'bg-blue-500' },
            { key: 'workdays_created', label: 'Workdays', color: 'bg-green-500' },
            { key: 'wages_paid', label: 'Wages Paid', color: 'bg-orange-500' },
            { key: 'payments_on_time_percent', label: 'On-Time %', color: 'bg-purple-500' },
          ].map(({ key, label, color }) => (
            <button
              key={key}
              onClick={() => setSelectedMetric(key)}
              className={`py-3 px-4 rounded-lg font-semibold transition-all ${
                selectedMetric === key
                  ? `${color} text-white shadow-lg`
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Trend Chart */}
      <TrendChart trends={trends} selectedMetric={selectedMetric} />

      {/* Info Box */}
      <div className="bg-gradient-to-r from-blue-500 to-green-500 rounded-xl shadow-md p-6 text-white">
        <h3 className="text-xl font-bold mb-2">About MGNREGA</h3>
        <p className="text-sm opacity-90">
          Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) provides 100 days of
          guaranteed wage employment to every rural household. This dashboard tracks performance
          metrics including people benefited, workdays created, wages paid, payment timeliness,
          and completed works in your district.
        </p>
      </div>
    </div>
  );
}


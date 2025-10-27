import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';

const metricsConfig = {
  people_benefited: {
    label: 'People Benefited',
    color: '#3b82f6',
    dataKey: 'people_benefited',
  },
  workdays_created: {
    label: 'Workdays Created',
    color: '#10b981',
    dataKey: 'workdays_created',
  },
  wages_paid: {
    label: 'Wages Paid',
    color: '#f59e0b',
    dataKey: 'wages_paid',
  },
  payments_on_time_percent: {
    label: 'On-Time Payments %',
    color: '#8b5cf6',
    dataKey: 'payments_on_time_percent',
  },
};

export default function TrendChart({ trends, selectedMetric = 'people_benefited' }) {
  const metric = metricsConfig[selectedMetric];

  const formatYAxis = (value) => {
    if (selectedMetric === 'payments_on_time_percent') {
      return `${value}%`;
    }
    if (value >= 10000000) {
      return `${(value / 10000000).toFixed(1)}Cr`;
    }
    if (value >= 100000) {
      return `${(value / 100000).toFixed(1)}L`;
    }
    if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}K`;
    }
    return value;
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-800">{label}</p>
          <p className="text-sm" style={{ color: metric.color }}>
            {metric.label}: {metric.dataKey === 'wages_paid' ? `₹${payload[0].value.toLocaleString()}` : formatYAxis(payload[0].value)}
          </p>
        </div>
      );
    }
    return null;
  };

  if (!trends || trends.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-8 text-center text-gray-500">
        No trend data available
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={trends}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="month_year"
            stroke="#6b7280"
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <YAxis
            stroke="#6b7280"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={formatYAxis}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey={metric.dataKey}
            stroke={metric.color}
            strokeWidth={3}
            dot={{ fill: metric.color, strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}


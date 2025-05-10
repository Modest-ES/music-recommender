import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

// Mapping of short labels to full names
const featureNames = {
  А: 'Акустичность',
  Т: 'Танцевальность',
  Э: 'Энергичность',
  И: 'Инструментальность',
  Р: 'Разговорность',
  Ж: 'Живость',
  П: 'Позитивность'
};

export function RadarChart({ features }) {
  const textColor = '#ffffff';
  const gridColor = 'rgba(255, 255, 255, 0.1)';
  const tickColor = 'rgba(255, 255, 255, 0.7)';

  const data = {
    labels: Object.keys(features), // Uses the short labels (A, D, E, etc.)
    datasets: [
      {
        label: 'Параметры аудио',
        data: Object.values(features),
        backgroundColor: 'rgba(29, 185, 84, 0.2)',
        borderColor: 'rgba(29, 185, 84, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(29, 185, 84, 1)'
      }
    ]
  };

  const options = {
    scales: {
      r: {
        angleLines: {
          display: true,
          color: gridColor
        },
        grid: {
          color: gridColor
        },
        pointLabels: {
          color: textColor,
          font: {
            size: 10
          }
        },
        ticks: {
          color: tickColor,
          backdropColor: 'transparent',
          stepSize: 0.5,
          showLabelBackdrop: false
        },
        suggestedMin: 0,
        suggestedMax: 1
      }
    },
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          // Customize the tooltip labels
          title: (context) => {
            const label = context[0].label; // Gets the short label (A, D, E, etc.)
            return featureNames[label] || label; // Returns full name if available
          },
          label: (context) => {
            return `${context.formattedValue}`; // Just show the value
          }
        },
        titleColor: textColor,
        bodyColor: textColor,
        backgroundColor: 'rgba(24, 24, 24, 0.9)',
        borderColor: 'rgba(29, 185, 84, 0.5)',
        borderWidth: 1,
        padding: 10,
        cornerRadius: 6
      }
    },
    maintainAspectRatio: false
  };

  return (
    <div style={{ width: '150px', height: '150px' }}>
      <Radar data={data} options={options} />
    </div>
  );
}
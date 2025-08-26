<template>
  <div id="app">
    <h1>Crimson Cycle</h1>

    <!-- Status Message Display -->
    <div v-if="statusMessage" class="status-message" :class="statusType">
      {{ statusMessage }}
    </div>

    <!-- Form for adding new periods -->
    <form @submit.prevent="addPeriod" class="period-form">
      <h2>Add New Period</h2>
      <div class="form-group">
        <label for="start-date">Start Date:</label>
        <input type="date" id="start-date" v-model="newPeriod.start_date" required>
      </div>
      <div class="form-group">
        <label for="end-date">End Date:</label>
        <input type="date" id="end-date" v-model="newPeriod.end_date" required>
      </div>
      <button type="submit">Add Period</button>
    </form>

    <!-- Calendar View -->
    <div class="calendar-container">
      <h2>Calendar</h2>
      <div class="calendar">
        <div class="header">
          <button @click="prevMonth">&lt;</button>
          <span>{{ currentMonthName }} {{ currentYear }}</span>
          <button @click="nextMonth">&gt;</button>
        </div>
        <div class="days">
          <div v-for="day in weekdays" :key="day" class="day-name">{{ day }}</div>
          <div v-for="day in calendarDays" :key="day.date" class="day" :class="day.classes">
            {{ day.day }}
          </div>
        </div>
      </div>
       <div class="legend">
        <div><span class="legend-color period"></span> Period</div>
        <div><span class="legend-color estimated"></span> Estimated Next Period</div>
      </div>
    </div>

    <!-- List of all period entries -->
    <div class="periods-list">
      <h2>Recorded Periods</h2>
      <ul>
        <li v-for="period in periods" :key="period.start_date">
          <span>Start: {{ period.start_date }} | End: {{ period.end_date }}</span>
          <button @click="deletePeriod(period.start_date)" class="delete-btn">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // Array to store period data fetched from the backend
      periods: [],
      // Object to hold data for the new period being added
      newPeriod: {
        start_date: '',
        end_date: ''
      },
      // For displaying status messages to the user
      statusMessage: '',
      statusType: 'success', // can be 'success' or 'error'
      // Calendar-related data
      currentDate: new Date(),
      weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    };
  },
  computed: {
    // The following computed properties are for the calendar
    currentMonth() {
      return this.currentDate.getMonth();
    },
    currentYear() {
      return this.currentDate.getFullYear();
    },
    currentMonthName() {
      return this.currentDate.toLocaleString('default', { month: 'long' });
    },
    // This generates the days for the calendar grid
    calendarDays() {
      const days = [];
      const firstDay = new Date(this.currentYear, this.currentMonth, 1);
      const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);

      // Add blank days for the start of the month
      for (let i = 0; i < firstDay.getDay(); i++) {
        days.push({ date: `blank-${i}` });
      }

      // Add actual days of the month
      for (let i = 1; i <= lastDay.getDate(); i++) {
        const date = new Date(this.currentYear, this.currentMonth, i);
        const dateString = date.toISOString().split('T')[0];
        days.push({
          day: i,
          date: dateString,
          classes: this.getDayClasses(date)
        });
      }
      return days;
    },
    // Calculates the estimated next period
    estimatedNextPeriod() {
        if (this.periods.length < 2) return null;

        let cycleLengths = [];
        // Sort periods by start date to calculate cycles correctly
        const sortedPeriods = [...this.periods].sort((a, b) => new Date(a.start_date) - new Date(b.start_date));

        for (let i = 1; i < sortedPeriods.length; i++) {
            const startDate1 = new Date(sortedPeriods[i-1].start_date);
            const startDate2 = new Date(sortedPeriods[i].start_date);
            const diffTime = Math.abs(startDate2 - startDate1);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            cycleLengths.push(diffDays);
        }

        if(cycleLengths.length === 0) return null;

        const avgCycleLength = cycleLengths.reduce((a, b) => a + b, 0) / cycleLengths.length;
        const lastPeriod = sortedPeriods[sortedPeriods.length - 1];
        const lastStartDate = new Date(lastPeriod.start_date);

        const estimatedStartDate = new Date(lastStartDate.setDate(lastStartDate.getDate() + avgCycleLength));

        // Assume the period length is the same as the last recorded one
        const lastPeriodLength = (new Date(lastPeriod.end_date) - new Date(lastPeriod.start_date)) / (1000 * 60 * 60 * 24);
        const estimatedEndDate = new Date(new Date(estimatedStartDate).setDate(estimatedStartDate.getDate() + lastPeriodLength));

        return {
            start: estimatedStartDate,
            end: estimatedEndDate
        };
    }
  },
  methods: {
    // Fetches all periods from the backend
    async fetchPeriods() {
      try {
        const response = await axios.get('/api/periods');
        this.periods = response.data;
      } catch (error) {
        this.showStatus('Error fetching periods', 'error');
      }
    },
    // Adds a new period
    async addPeriod() {
      if (new Date(this.newPeriod.end_date) < new Date(this.newPeriod.start_date)) {
        this.showStatus('End date cannot be before start date.', 'error');
        return;
      }
      try {
        await axios.post('/api/periods', this.newPeriod);
        this.showStatus('Period added successfully', 'success');
        this.newPeriod.start_date = '';
        this.newPeriod.end_date = '';
        this.fetchPeriods(); // Refresh the list
      } catch (error) {
        this.showStatus('Error adding period', 'error');
      }
    },
    // Deletes a period
    async deletePeriod(startDate) {
      try {
        await axios.delete(`/api/periods/${startDate}`);
        this.showStatus('Period deleted successfully', 'success');
        this.fetchPeriods(); // Refresh the list
      } catch (error) {
        this.showStatus('Error deleting period', 'error');
      }
    },
    // Shows a status message for a few seconds
    showStatus(message, type) {
      this.statusMessage = message;
      this.statusType = type;
      setTimeout(() => {
        this.statusMessage = '';
      }, 3000);
    },
    // Calendar navigation
    prevMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
    },
    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
    },
    // Determines CSS classes for a calendar day
    getDayClasses(date) {
      const classes = [];
      const dateStr = date.toISOString().split('T')[0];

      // Check for recorded periods
      if (this.periods.some(p => dateStr >= p.start_date && dateStr <= p.end_date)) {
        classes.push('period');
      }

      // Check for estimated next period
      if (this.estimatedNextPeriod) {
          const estStart = new Date(this.estimatedNextPeriod.start);
          estStart.setHours(0,0,0,0);
          const estEnd = new Date(this.estimatedNextPeriod.end);
          estEnd.setHours(0,0,0,0);
          if (date >= estStart && date <= estEnd) {
              classes.push('estimated');
          }
      }
      return classes.join(' ');
    }
  },
  // This is a Vue lifecycle hook that runs when the component is mounted
  mounted() {
    this.fetchPeriods();
  }
};
</script>

<style>
/* General styling */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Form styling */
.period-form {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  margin-right: 0.5rem;
}
input[type="date"] {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}
button {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #36a374;
}

/* List styling */
.periods-list {
  margin-top: 2rem;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}
.delete-btn {
  background-color: #e74c3c;
}
.delete-btn:hover {
  background-color: #c0392b;
}

/* Status message styling */
.status-message {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}
.success {
  background-color: #d4edda;
  color: #155724;
}
.error {
  background-color: #f8d7da;
  color: #721c24;
}

/* Calendar styling */
.calendar-container {
  margin-top: 2rem;
}
.calendar {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f7f7f7;
  padding: 0.5rem;
}
.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #eee;
}
.day-name, .day {
  background-color: white;
  padding: 0.5rem;
  text-align: center;
}
.day.period {
  background-color: #ffcccc; /* Light red for period days */
}
.day.estimated {
  background-color: #cceeff; /* Light blue for estimated days */
}
.legend {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}
.legend-color {
  display: inline-block;
  width: 1em;
  height: 1em;
  vertical-align: middle;
  margin-right: 0.5em;
}
.legend-color.period {
  background-color: #ffcccc;
}
.legend-color.estimated {
  background-color: #cceeff;
}
</style>

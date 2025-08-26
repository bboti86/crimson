<template>
  <div id="app">
    <div class="top-section">
      <img src="https://github.com/bboti86/crimson/blob/main/crimson_logo.png?raw=true" alt="Crimson Cycle Logo" class="logo">
      <p>Your secure, private cycle tracker.</p>
    </div>

    <!-- Status Message Display -->
    <div v-if="statusMessage" class="status-message" :class="statusType">
      {{ statusMessage }}
    </div>

    <!-- Form for adding new periods -->
    <div class="middle-section period-form">
      <form @submit.prevent="addPeriod">
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
    </div>

    <!-- Calendar View -->
    <div class="calendar-container">
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
        <div><span class="legend-color estimated"></span> Estimated Period</div>
      </div>
    </div>

    <!-- List of all period entries -->
    <div class="bottom-section periods-list">
      <h2>Recorded Periods</h2>
      <ul>
        <li v-for="period in periods.historical" :key="period.start_date">
          <span>Start: {{ period.start_date }} | End: {{ period.end_date }}</span>
          <span @click="deletePeriod(period.start_date)" class="delete-icon">
            &#x2715;
          </span>
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
      // Object to store period data fetched from the backend
      periods: {
        historical: [],
        estimated: []
      },
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
        // Ensure periods object has the correct structure on error
        this.periods = { historical: [], estimated: [] };
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
        this.fetchPeriods(); // Refresh the list and get new estimations
      } catch (error) {
        this.showStatus('Error adding period', 'error');
      }
    },
    // Deletes a period
    async deletePeriod(startDate) {
      try {
        await axios.delete(`/api/periods/${startDate}`);
        this.showStatus('Period deleted successfully', 'success');
        this.fetchPeriods(); // Refresh the list and get new estimations
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

      // Check for recorded historical periods
      if (this.periods.historical.some(p => dateStr >= p.start_date && dateStr <= p.end_date)) {
        classes.push('period');
      }

      // Check for estimated future periods
      if (this.periods.estimated.some(p => dateStr >= p.start_date && dateStr <= p.end_date)) {
        classes.push('estimated');
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
body {
  background-color: #F8F0E3;
  font-family: 'Georgia', serif;
  color: #3C393A;
}

#app {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  text-align: center;
}

/* Top Section */
.logo {
  width: 200px;
  height: 200px;
  margin-bottom: 1rem;
}
.top-section p {
  font-size: 1rem;
  margin-bottom: 2rem;
}

/* Containers */
.period-form, .periods-list, .calendar-container {
  background-color: #FCF5EF;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

/* Form styling */
.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
label {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}
input[type="date"] {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #EED9C4;
  background-color: #FFFFFF;
  box-sizing: border-box; /* Ensures padding doesn't affect width */
}
button[type="submit"] {
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: #A3438E;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
  transition: background-color 0.3s;
}
button[type="submit"]:hover {
  background-color: #8e3a7a;
}

/* List styling */
.periods-list h2 {
  font-size: 1.5rem;
  font-weight: normal;
  margin-bottom: 1.5rem;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #EED9C4;
}
li:last-child {
  border-bottom: none;
}
.delete-icon {
  color: #A3438E;
  cursor: pointer;
  font-size: 1.2rem;
  transition: color 0.3s, transform 0.3s;
}
.delete-icon:hover {
  color: #8e3a7a;
  transform: scale(1.1);
}

/* Status message styling */
.status-message {
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  color: #fff;
}
.success {
  background-color: #A3438E;
}
.error {
  background-color: #c0392b;
}

/* Calendar styling */
.calendar {
  border-radius: 8px;
  overflow: hidden;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #EED9C4;
}
.header button {
  background: none;
  border: none;
  color: #A3438E;
  font-size: 1.5rem;
  cursor: pointer;
}
.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}
.day-name, .day {
  padding: 0.5rem;
  text-align: center;
}
.day-name {
  font-weight: bold;
}
.day {
  border-radius: 50%;
  line-height: 2rem;
  height: 2rem;
  width: 2rem;
  margin: auto;
}
.day.period {
  background-color: #A3438E;
  color: white;
}
.day.estimated {
  background-color: #EED9C4;
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
  border-radius: 50%;
}
.legend-color.period {
  background-color: #A3438E;
}
.legend-color.estimated {
  background-color: #EED9C4;
}

@media (prefers-color-scheme: dark) {
  body {
    background-color: #1a1a1a;
    color: white;
  }
  .period-form, .periods-list, .calendar-container {
    background-color: #2a2a2a;
    box-shadow: none;
  }
  input[type="date"] {
    background-color: #3a3a3a;
    color: white;
    border-color: #4a4a4a;
  }
  li {
    border-bottom-color: #3a3a3a;
  }
  .header {
    border-bottom-color: #3a3a3a;
  }
  .day.estimated {
    background-color: #4a4a4a;
  }
  .legend-color.estimated {
    background-color: #4a4a4a;
  }
}
</style>

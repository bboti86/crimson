<template>
  <div id="app">
    <div class="top-section">
      <h1>Crimson Cycle</h1>
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

    <!-- List of all period entries -->
    <div class="bottom-section periods-list">
      <h2>Recorded Periods</h2>
      <ul>
        <li v-for="period in periods" :key="period.start_date">
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
      // Array to store period data fetched from the backend
      periods: [],
      // Object to hold data for the new period being added
      newPeriod: {
        start_date: '',
        end_date: ''
      },
      // For displaying status messages to the user
      statusMessage: '',
      statusType: 'success' // can be 'success' or 'error'
    };
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
.top-section h1 {
  font-size: 3rem;
  font-weight: normal;
  margin-bottom: 0.5rem;
}
.top-section p {
  font-size: 1rem;
  margin-bottom: 2rem;
}

/* Containers */
.period-form, .periods-list {
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
</style>

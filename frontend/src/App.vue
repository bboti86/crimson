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

    <div class="main-content">
      <div class="left-column">
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
      </div>

      <div class="right-column">
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
    </div>

    <footer class="app-footer">
      <button @click="showDisclaimerModal = true">Disclaimer</button>
      <button @click="showPrivacyModal = true">Privacy Policy</button>
      <button @click="showTermsModal = true">Terms & Conditions</button>
    </footer>

    <!-- Modals -->
    <Modal :show="showDisclaimerModal" @close="showDisclaimerModal = false">
      <h3>About Our Period Estimates</h3>
      <p>Our period estimates are calculated based on a simple but reliable method: averaging the length of your past menstrual cycles. While this approach provides a good prediction, it's important to understand that it is an estimate and not an exact forecast. Your next period may arrive a few days earlier or later than predicted.</p>
      <p>There are several factors that can affect the accuracy of these predictions, including:</p>
      <ul>
        <li><strong>Irregular Cycles:</strong> If your cycles vary significantly in length from month to month, the average calculation will be less accurate.</li>
        <li><strong>Lifestyle Changes:</strong> Factors such as stress, changes in diet, travel, or changes in sleep patterns can all impact your cycle length and make it difficult to predict.</li>
        <li><strong>Underlying Health Conditions:</strong> Certain health conditions can cause irregular cycles that are difficult to track with a simple average.</li>
        <li><strong>Limited Data:</strong> The more cycles you log, the more accurate the average calculation becomes. Estimates made with only a few data points will be less reliable.</li>
      </ul>
      <p>This app is for informational purposes only and should not be used for contraception or to diagnose any health conditions. If you have concerns about your cycle, please consult a healthcare professional.</p>
    </Modal>

    <Modal :show="showPrivacyModal" @close="showPrivacyModal = false">
      <h3>Privacy and Data Protection</h3>
      <p>This document outlines the privacy and data protection principles for the <strong>Crimson Cycle</strong> web application.</p>
      <h4>Data Ownership and Control</h4>
      <p><strong>Crimson Cycle</strong> is a self-hosted application. This means that you, the user, are the sole host, owner, and controller of your data. The application developers do not collect, store, or have any access to your personal or health data. All information you enter remains exclusively on the server you are hosting the application on.</p>
      <h4>No Developer Data Collection</h4>
      <p>The developers of <strong>Crimson Cycle</strong> do not track, monitor, or collect any data from your use of the application. The source code is provided for you to run in your own environment, giving you complete control and privacy. There are no third-party analytics, tracking scripts, or data transmission to external servers built into this application.</p>
      <h4>Use of Cookies</h4>
      <p><strong>Crimson Cycle</strong> is designed to be completely private. It <strong>does not use or create any cookies</strong> to store information in your browser. All application data is handled on the server you are hosting, ensuring no data is left behind in your browser's local storage.</p>
      <h4>Your Responsibility for Security</h4>
      <p>As the owner and operator of your self-hosted instance of <strong>Crimson Cycle</strong>, you are entirely responsible for the security of the server and the data it contains. To ensure the privacy and security of your information, it is essential that you operate the application behind a secure <strong>reverse proxy</strong> (such as Traefik or NGINX) and implement an <strong>authentication provider</strong> (such as Authentik, OAuth2 Proxy, or Keycloak).</p>
      <p>These security measures are <strong>not included</strong> with the application and are necessary to protect your data from unauthorized access. Failure to implement proper security controls could expose your data to the public internet.</p>
    </Modal>

    <Modal :show="showTermsModal" @close="showTermsModal = false">
      <h3>Terms and Conditions</h3>
      <p>Welcome to <strong>Crimson Cycle</strong>. By using this application, you agree to these terms and conditions.</p>
      <h4>Acceptance of Terms</h4>
      <p>By deploying and using this self-hosted application, you acknowledge and agree to these Terms and Conditions. This is a non-commercial, open-source project provided for your personal use.</p>
      <h4>Responsibility and Data Ownership</h4>
      <p>The <strong>Crimson Cycle</strong> application is designed to be hosted by you, the end-user. You are solely responsible for the operation, maintenance, and security of your instance. The developers and contributors of this application do not own, manage, or have any access to your data. All data is stored locally on your server, and you are its sole owner.</p>
      <h4>Disclaimer of Warranties</h4>
      <p><strong>Crimson Cycle</strong> is provided "as is," without warranty of any kind, express or implied. The developers make no guarantees regarding its functionality, security, or accuracy. You assume all risks associated with your use of the application.</p>
      <h4>Limitation of Liability</h4>
      <p>In no event shall the developers or contributors be liable for any damages, including but not limited to direct, indirect, special, incidental, or consequential damages, arising out of your use or inability to use the application, even if advised of the possibility of such damages.</p>
      <h4>Security Responsibility</h4>
      <p>The application is provided as a core functional component. It does not include built-in security features such as user authentication or protection from public exposure. To ensure the security and privacy of your data, <strong>you are required to implement these measures yourself.</strong> This includes, but is not limited to, using a <strong>reverse proxy</strong> and an <strong>authentication provider</strong> to restrict access to your instance. Your failure to do so is at your own risk.</p>
      <h4>Changes to Terms</h4>
      <p>These terms may be updated from time to time. Your continued use of the application after any changes signifies your acceptance of the new terms.</p>
    </Modal>
  </div>
</template>

<script>
import axios from 'axios';
import Modal from './components/Modal.vue';

export default {
  components: {
    Modal,
  },
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
      weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      // Modal visibility state
      showDisclaimerModal: false,
      showPrivacyModal: false,
      showTermsModal: false,
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

@media (min-width: 1024px) {
  #app {
    max-width: 1200px;
  }
  .main-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: start;
  }
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

/* Footer and Modal Buttons */
.app-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #EED9C4;
}
.app-footer button {
  background: none;
  border: none;
  color: #A3438E;
  cursor: pointer;
  margin: 0 1rem;
  font-size: 0.9rem;
}
@media (prefers-color-scheme: dark) {
  .app-footer {
    border-top-color: #3a3a3a;
  }
}
</style>

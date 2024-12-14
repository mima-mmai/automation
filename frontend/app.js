import './style.css'

// API base URL
const API_BASE = 'http://localhost:6462/v1';

// Utility function to fetch data from API
async function fetchFromAPI(endpoint) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`);
    return await response.json();
  } catch (error) {
    console.error(`Error fetching from ${endpoint}:`, error);
    return null;
  }
}

// Update DOM elements with API data
async function updateDateTime() {
  const dateData = await fetchFromAPI('/get_date');
  if (dateData) {
    document.getElementById('current-date').textContent = dateData.date;
  }
}

async function updateGreeting() {
  const greetingData = await fetchFromAPI('/say_hello');
  if (greetingData) {
    document.getElementById('greeting').textContent = greetingData.message;
  }
}

async function updateProjects() {
  const projectsData = await fetchFromAPI('/get_py_projects');
  const projectsList = document.getElementById('projects-list');
  projectsList.innerHTML = '';
  
  if (projectsData && projectsData.projects) {
    projectsData.projects.forEach(project => {
      const li = document.createElement('li');
      li.textContent = project;
      projectsList.appendChild(li);
    });
  }
}

async function updateTodoList() {
  try {
    const response = await fetch(`${API_BASE}/get_todolist`);
    const todoHtml = await response.text();
    document.getElementById('todo-content').innerHTML = todoHtml;
  } catch (error) {
    console.error('Error fetching todo list:', error);
  }
}

async function updateAutomationProjects() {
  const automationData = await fetchFromAPI('/get_automation');
  const automationList = document.getElementById('automation-list');
  automationList.innerHTML = '';
  
  if (automationData && automationData.automation_projects) {
    automationData.automation_projects.forEach(project => {
      const card = document.createElement('div');
      card.className = 'project-card';
      card.innerHTML = `
        <h3>${project.name}</h3>
        <p>${project.description}</p>
        <span class="status ${project.status.toLowerCase()}">${project.status}</span>
      `;
      automationList.appendChild(card);
    });
  }
}

// Initialize the app
function initApp() {
  // Initial data load
  updateDateTime();
  updateGreeting();
  updateProjects();
  updateTodoList();
  updateAutomationProjects();
  
  // Set up refresh button
  document.getElementById('refresh-btn').addEventListener('click', () => {
    updateDateTime();
    updateGreeting();
    updateProjects();
    updateTodoList();
    updateAutomationProjects();
  });
  
  // Update date every minute
  setInterval(updateDateTime, 60000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);
